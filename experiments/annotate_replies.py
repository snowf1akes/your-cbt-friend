"""
annotate_replies.py -- label every generated reply (and the human reference reply) with the 23-label
codebook, sentence by sentence, using the codebook text as the annotation instructions and a JSON schema
that only allows the 25 label names.

Each reply is split into sentences the way the annotation sheets were (one sentence per line), numbered,
and sent together with the OP post for context. Human replies are annotated with the same model so the
comparison to the generated replies is apples to apples; their gold labels are kept separately.

Usage:
  python experiments/annotate_replies.py --run pilot [--model claude-opus-5] [--workers 4]
Output: runs/<run>/annotations.jsonl (resumable)
"""
import argparse, concurrent.futures as cf, json, os, re, sys, threading, time

import anthropic

from paths import DATA, RUNS, CODEBOOK, LABEL_NAMES
from generate_replies import PRICE, load_env
INSTRUCTIONS = """You are annotating a Reddit mental-health thread for a research project, following the codebook below exactly.
You will be given the original post (for context only; do not label it) and one responder comment split into
numbered sentences. Label every sentence of the comment with zero, one, or several labels from this fixed list:
%s

Rules that matter most:
- Apply the codebook's project-specific definitions, not textbook CBT. When unsure, re-check the label's Yes/No list.
- Mandatory double tags: Clinical Referral -> also Recommendation; Bad Advice -> also Recommendation;
  Encouraging Self-Compassion -> also Recommendation when it is a recommendation to the seeker;
  Journal / Thought Record -> also Recommendation when recommended.
- Validation: first instance in the comment only. Journal / Thought Record: first instance only.
- Focal Point labels apply only when the comment itself raises a new question or topic (e.g. asks the poster something).
- Self-Disclosure only for genuine first-person disclosure of the commenter's own experience, feelings, identity or history.
- Non-Expert Diagnosis only when a diagnosis is asserted without any hedge.
- Most sentences carry zero or one label. Do not invent labels for neutral sentences.
Return JSON with one entry per numbered sentence, in order, with the exact label strings.""" % "\n".join("- " + n for n in LABEL_NAMES)

SCHEMA = {"type": "object", "properties": {"lines": {"type": "array", "items": {
    "type": "object", "properties": {"idx": {"type": "integer"}, "labels": {"type": "array", "items": {"type": "string", "enum": LABEL_NAMES}}},
    "required": ["idx", "labels"], "additionalProperties": False}}}, "required": ["lines"], "additionalProperties": False}


def split_sentences(text):
    out = []
    for para in re.split(r"\n+", text.strip()):
        para = para.strip()
        if not para:
            continue
        para = re.sub(r"^[-*•]\s+|^\d+[.)]\s+", "", para)          # list bullets -> plain sentences
        for s in re.split(r"(?<=[.!?…])\s+(?=[^\s])", para):
            s = s.strip()
            if s:
                out.append(s)
    return out


def annotate(client, model, system, post, sentences):
    numbered = "\n".join("%d. %s" % (i + 1, s) for i, s in enumerate(sentences))
    user = ("ORIGINAL POST (context only)\nSubreddit: r/%s\nTitle: %s\n%s\n\nRESPONDER COMMENT, numbered sentences:\n%s\n\n"
            "Label each of the %d sentences." % (post["subreddit"], post["title"], post["body"], numbered, len(sentences)))
    t0 = time.time()
    resp = client.messages.create(
        model=model, max_tokens=4000,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}})
    text = next((b.text for b in resp.content if b.type == "text"), "{}")
    data = json.loads(text)
    by_idx = {int(e["idx"]): [l for l in e["labels"] if l in LABEL_NAMES] for e in data.get("lines", [])}
    labels = [sorted(set(by_idx.get(i + 1, []))) for i in range(len(sentences))]
    u = resp.usage
    return labels, dict(input=u.input_tokens, output=u.output_tokens, cache_read=getattr(u, "cache_read_input_tokens", 0) or 0,
                        cache_write=getattr(u, "cache_creation_input_tokens", 0) or 0), round(time.time() - t0, 1), resp.stop_reason


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--skip-human", action="store_true")
    args = ap.parse_args()
    load_env()
    client = anthropic.Anthropic(max_retries=6)
    system = INSTRUCTIONS + "\n\n<codebook>\n" + open(CODEBOOK, encoding="utf-8").read() + "\n</codebook>"
    run_dir = os.path.join(RUNS, args.run)
    posts = {json.loads(l)["post_id"]: json.loads(l) for l in open(os.path.join(DATA, "testset.jsonl"), encoding="utf-8")}
    items = []
    for l in open(os.path.join(run_dir, "replies.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if not r.get("error") and r.get("text"):
            items.append(dict(post_id=r["post_id"], source=r["condition"], text=r["text"]))
    if not args.skip_human:
        for pid in sorted({i["post_id"] for i in items}):
            items.append(dict(post_id=pid, source="human", text=posts[pid]["human_reply"]))
    out_path = os.path.join(run_dir, "annotations.jsonl")
    done = set()
    if os.path.exists(out_path):
        for l in open(out_path, encoding="utf-8"):
            r = json.loads(l)
            if not r.get("error"):
                done.add((r["post_id"], r["source"]))
    todo = [i for i in items if (i["post_id"], i["source"]) not in done]
    print("annotating %d replies (%d already done) with %s" % (len(todo), len(done), args.model))
    lock = threading.Lock()
    totals = dict(input=0, output=0, cache_read=0, cache_write=0)

    def work(item):
        sentences = split_sentences(item["text"])
        rec = dict(post_id=item["post_id"], source=item["source"], sentences=sentences, model=args.model)
        try:
            labels, usage, secs, stop = annotate(client, args.model, system, posts[item["post_id"]], sentences)
            rec.update(labels=labels, usage=usage, seconds=secs, stop_reason=stop)
        except (anthropic.APIStatusError, anthropic.APIConnectionError, json.JSONDecodeError) as e:
            rec["error"] = str(e)[:200]
        return rec

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex, open(out_path, "a", encoding="utf-8") as f:
        for rec in ex.map(work, todo):
            with lock:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                f.flush()
                if rec.get("error"):
                    print("  ERROR %s/%s: %s" % (rec["post_id"], rec["source"], rec["error"]))
                else:
                    for k in totals:
                        totals[k] += rec["usage"][k]
                    print("  ok %s/%s sentences=%d labels=%d" % (rec["post_id"], rec["source"], len(rec["sentences"]), sum(len(x) for x in rec["labels"])))
    pi, po, pw, pr = PRICE.get(args.model, (5, 25, 6.25, 0.5))
    cost = (totals["input"] * pi + totals["output"] * po + totals["cache_write"] * pw + totals["cache_read"] * pr) / 1e6
    print("\ndone | tokens in=%d out=%d cache_read=%d cache_write=%d | est. cost $%.2f | output %s" %
          (totals["input"], totals["output"], totals["cache_read"], totals["cache_write"], cost, out_path))


if __name__ == "__main__":
    main()
