"""
generate_replies.py -- generate replies to the held-out test posts under two conditions:

  bare   : Claude asked to reply as a community member, nothing else
  skill  : the same request, with the your-cbt-friend skill (SKILL.md + references) in the system prompt

Both conditions get the identical user message. The skill text is cached across posts, so the extra cost
of the skill condition is mostly the first request. Refusal fallbacks are deliberately NOT enabled: this is
an experiment on one model, so a refusal is recorded as a result rather than re-routed to another model.

Credentials: ANTHROPIC_API_KEY in the environment, or a line ANTHROPIC_API_KEY=... in <project>/.env
(gitignored). The script never prints the key.

Usage:
  python experiments/generate_replies.py --run pilot --limit 5
  python experiments/generate_replies.py --run full
Options: --conditions bare,skill  --model claude-opus-5  --workers 4  --posts <id,id>  --effort high
Output: runs/<run>/replies.jsonl (resumable: existing post x condition pairs are skipped)
"""
import argparse, concurrent.futures as cf, json, os, re, threading, time

import anthropic

from paths import REPO as ROOT, DATA, RUNS
SKILL_DIR = ROOT   # SKILL.md and references/ live at the repository root
PRICE = {  # $ per 1M tokens: input, output, cache write, cache read
    "claude-opus-5": (5.0, 25.0, 6.25, 0.5), "claude-sonnet-5": (2.0, 10.0, 2.5, 0.2), "claude-haiku-4-5": (1.0, 5.0, 1.25, 0.1),
    "claude-fable-5-1": (10.0, 50.0, 12.5, 1.0),
}
BARE_SYSTEM = ("You are a member of a Reddit mental-health support community replying to another member's post. "
               "Write your reply as a comment.")


def load_env():
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def skill_bundle():
    """SKILL.md body (frontmatter removed) followed by every reference file, in a fixed order."""
    text = open(os.path.join(SKILL_DIR, "SKILL.md"), encoding="utf-8").read()
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    parts = ["The following is a skill you must follow for this task.", "", '<skill name="your-cbt-friend">', body.strip()]
    ref_dir = os.path.join(SKILL_DIR, "references")
    for fn in sorted(os.listdir(ref_dir)) if os.path.isdir(ref_dir) else []:
        if fn.endswith(".md"):
            parts += ["", '<reference file="references/%s">' % fn, open(os.path.join(ref_dir, fn), encoding="utf-8").read().strip(), "</reference>"]
    parts += ["</skill>"]
    return "\n".join(parts)


def user_prompt(post):
    return ("Subreddit: r/%s\n\nTitle: %s\n\n%s\n\nWrite your reply to this post as a comment." % (post["subreddit"], post["title"], post["body"]))


def call(client, model, system, user, max_tokens, effort):
    kwargs = dict(model=model, max_tokens=max_tokens,
                  system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                  messages=[{"role": "user", "content": user}])
    if effort:
        kwargs["output_config"] = {"effort": effort}
    t0 = time.time()
    resp = client.messages.create(**kwargs)
    u = resp.usage
    return dict(text="".join(b.text for b in resp.content if b.type == "text").strip(), stop_reason=resp.stop_reason,
                model=resp.model, request_id=getattr(resp, "_request_id", None), seconds=round(time.time() - t0, 1),
                usage=dict(input=u.input_tokens, output=u.output_tokens,
                           cache_read=getattr(u, "cache_read_input_tokens", 0) or 0,
                           cache_write=getattr(u, "cache_creation_input_tokens", 0) or 0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--conditions", default="bare,skill")
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--effort", default="")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--posts", default="")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=4000)
    args = ap.parse_args()
    load_env()
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        raise SystemExit("No API credentials: set ANTHROPIC_API_KEY (or put ANTHROPIC_API_KEY=... in %s)" % os.path.join(ROOT, ".env"))
    client = anthropic.Anthropic(max_retries=6)
    posts = [json.loads(l) for l in open(os.path.join(DATA, "testset.jsonl"), encoding="utf-8")]
    if args.posts:
        keep = set(args.posts.split(","))
        posts = [p for p in posts if p["post_id"] in keep]
    if args.limit:
        posts = posts[:args.limit]
    conditions = [c.strip() for c in args.conditions.split(",") if c.strip()]
    systems = {"bare": BARE_SYSTEM, "skill": skill_bundle() if "skill" in conditions else ""}
    run_dir = os.path.join(RUNS, args.run)
    os.makedirs(run_dir, exist_ok=True)
    out_path = os.path.join(run_dir, "replies.jsonl")
    done = set()
    if os.path.exists(out_path):
        for l in open(out_path, encoding="utf-8"):
            r = json.loads(l)
            if not r.get("error"):
                done.add((r["post_id"], r["condition"]))
    json.dump(dict(model=args.model, effort=args.effort, conditions=conditions, bare_system=BARE_SYSTEM,
                   skill_chars=len(systems["skill"]), n_posts=len(posts)),
              open(os.path.join(run_dir, "config.json"), "w", encoding="utf-8"), indent=1)
    tasks = [(p, c) for p in posts for c in conditions if (p["post_id"], c) not in done]
    print("run=%s model=%s posts=%d conditions=%s to_do=%d (already done %d) skill_prompt_chars=%d" %
          (args.run, args.model, len(posts), conditions, len(tasks), len(done), len(systems["skill"])))
    lock = threading.Lock()
    totals = dict(input=0, output=0, cache_read=0, cache_write=0)
    n_ref = n_err = 0

    def work(task):
        p, c = task
        rec = dict(post_id=p["post_id"], subreddit=p["subreddit"], condition=c, model_requested=args.model, effort=args.effort)
        try:
            rec.update(call(client, args.model, systems[c], user_prompt(p), args.max_tokens, args.effort))
        except anthropic.APIStatusError as e:
            rec["error"] = "%s %s" % (e.status_code, getattr(e, "message", str(e))[:200])
        except anthropic.APIConnectionError as e:
            rec["error"] = "connection: %s" % str(e)[:200]
        return rec

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex, open(out_path, "a", encoding="utf-8") as f:
        for rec in ex.map(work, tasks):
            with lock:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                if rec.get("error"):
                    n_err += 1
                    print("  ERROR %s/%s: %s" % (rec["post_id"], rec["condition"], rec["error"]))
                else:
                    for k in totals:
                        totals[k] += rec["usage"][k]
                    if rec["stop_reason"] == "refusal":
                        n_ref += 1
                    print("  ok %s/%s words=%d stop=%s %.0fs" % (rec["post_id"], rec["condition"], len(rec["text"].split()), rec["stop_reason"], rec["seconds"]))
    pi, po, pw, pr = PRICE.get(args.model, (5, 25, 6.25, 0.5))
    cost = (totals["input"] * pi + totals["output"] * po + totals["cache_write"] * pw + totals["cache_read"] * pr) / 1e6
    print("\ndone: %d requests, %d errors, %d refusals | tokens in=%d out=%d cache_read=%d cache_write=%d | est. cost $%.2f" %
          (len(tasks), n_err, n_ref, totals["input"], totals["output"], totals["cache_read"], totals["cache_write"], cost))
    print("output:", out_path)


if __name__ == "__main__":
    main()
