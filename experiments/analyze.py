"""
analyze.py -- compare the reply conditions (bare Claude, Claude + your-cbt-friend skill) against the human
first replies, using the codebook labels assigned by annotate_replies.py.

Outputs in runs/<run>/:
  report.md         technique profiles per condition, harmful labels, structural checks, paired differences
  side_by_side.md   every test post with the bare reply, the skill reply and the human reply
  summary.json      the numbers behind the report

Usage:  python experiments/analyze.py --run pilot
"""
import argparse, json, math, os, re, sys
from collections import Counter, defaultdict

from paths import DATA, RUNS, LABEL_NAMES

HARMFUL = ["Bad Advice", "Incorrect Information", "Non-Expert Diagnosis"]
CORE = ["Validation", "Summarizing", "Restructuring", "Recommendation", "Clinical Referral", "Encouraging Self-Compassion",
        "Grounding Technique", "Journal / Thought Record", "Social Support", "Psychoeducation", "Cognitive Conceptualization",
        "Self-Disclosure", "Focal Point (Request)", "Acceptance", "Reflection"]


def md_table(rows, cols):
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        out.append("| " + " | ".join(("%.1f" % v if isinstance(v, float) else str(v)) for v in (r.get(c, "") for c in cols)) + " |")
    return "\n".join(out)


def js_divergence(p, q):
    keys = set(p) | set(q)
    sp, sq = sum(p.values()) or 1, sum(q.values()) or 1
    P = {k: p.get(k, 0) / sp for k in keys}
    Q = {k: q.get(k, 0) / sq for k in keys}
    M = {k: (P[k] + Q[k]) / 2 for k in keys}
    kl = lambda A, B: sum(A[k] * math.log2(A[k] / B[k]) for k in keys if A[k] > 0)
    return 0.5 * kl(P, M) + 0.5 * kl(Q, M)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    args = ap.parse_args()
    run_dir = os.path.join(RUNS, args.run)
    posts = {json.loads(l)["post_id"]: json.loads(l) for l in open(os.path.join(DATA, "testset.jsonl"), encoding="utf-8")}
    replies = {}
    for l in open(os.path.join(run_dir, "replies.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        replies[(r["post_id"], r["condition"])] = r
    ann = {}
    for l in open(os.path.join(run_dir, "annotations.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if not r.get("error"):
            ann[(r["post_id"], r["source"])] = r
    sources = [s for s in ("bare", "skill", "human") if any(k[1] == s for k in ann)]
    # human gold labels as a fourth column
    gold = {}
    for pid, p in posts.items():
        if (pid, "human") in ann:
            gold[(pid, "human_gold")] = dict(post_id=pid, source="human_gold", sentences=[x["text"] for x in p["human_reply_lines"]],
                                             labels=[x["labels"] for x in p["human_reply_lines"]])
    ann.update(gold)
    if gold:
        sources.append("human_gold")

    def raw_text(pid, s):
        if s in ("human", "human_gold"):
            return posts[pid]["human_reply"]
        return replies.get((pid, s), {}).get("text", "")

    stats, profiles = {}, {}
    for s in sources:
        recs = [r for (pid, src), r in ann.items() if src == s]
        texts = [raw_text(r["post_id"], s) for r in recs]
        em_dashes = sum(t.count("—") for t in texts) / max(1, len(texts))
        markdown = sum(1 for t in texts if re.search(r"\*\*|^\s*(?:[-*•]|\d+[.)])\s+|^#{1,3}\s", t, re.M)) / max(1, len(texts)) * 100.0
        n_sent = sum(len(r["sentences"]) for r in recs)
        n_words = sum(len(" ".join(r["sentences"]).split()) for r in recs)
        cnt = Counter(l for r in recs for labs in r["labels"] for l in labs)
        has = Counter(l for r in recs for l in {x for labs in r["labels"] for x in labs})
        n_lab_sent = sum(1 for r in recs for labs in r["labels"] if labs)
        risk_ids = [pid for pid, p in posts.items() if p["risk_cue"] and (pid, s) in ann]
        risk_ref = sum(1 for pid in risk_ids if any("Clinical Referral" in labs for labs in ann[(pid, s)]["labels"]))
        ends_q = sum(1 for r in recs if r["sentences"] and r["sentences"][-1].strip().endswith("?"))
        stats[s] = dict(source=s, n_replies=len(recs), sentences_per_reply=n_sent / max(1, len(recs)), words_per_reply=n_words / max(1, len(recs)),
                        pct_sentences_labeled=100.0 * n_lab_sent / max(1, n_sent), labels_per_reply=sum(cnt.values()) / max(1, len(recs)),
                        pct_ends_with_question=100.0 * ends_q / max(1, len(recs)),
                        pct_validation=100.0 * has["Validation"] / max(1, len(recs)), pct_summarizing=100.0 * has["Summarizing"] / max(1, len(recs)),
                        pct_restructuring=100.0 * has["Restructuring"] / max(1, len(recs)), pct_recommendation=100.0 * has["Recommendation"] / max(1, len(recs)),
                        recommendations_per_reply=cnt["Recommendation"] / max(1, len(recs)),
                        pct_clinical_referral=100.0 * has["Clinical Referral"] / max(1, len(recs)),
                        pct_referral_on_risk_posts=(100.0 * risk_ref / len(risk_ids)) if risk_ids else float("nan"), n_risk_posts=len(risk_ids),
                        pct_self_disclosure=100.0 * has["Self-Disclosure"] / max(1, len(recs)),
                        harmful_instances=sum(cnt[h] for h in HARMFUL), pct_replies_with_harmful=100.0 * sum(1 for r in recs if any(h in labs for labs in r["labels"] for h in HARMFUL)) / max(1, len(recs)),
                        em_dashes_per_reply=em_dashes, pct_markdown=markdown,
                        n_sentences=n_sent, counts=dict(cnt), replies_with=dict(has))
        profiles[s] = {l: 100.0 * cnt[l] / max(1, n_sent) for l in LABEL_NAMES}

    rep = ["# your-cbt-friend experiment: %s" % args.run, ""]
    cfg = json.load(open(os.path.join(run_dir, "config.json"), encoding="utf-8")) if os.path.exists(os.path.join(run_dir, "config.json")) else {}
    rep += ["Model: %s, effort: %s. Test posts: %d. Sources: bare = Claude with a one-line instruction; skill = Claude with the "
            "your-cbt-friend skill in the system prompt; human = first human reply, labeled by the same annotator model; "
            "human_gold = the same human reply with the team's adjudicated labels." % (cfg.get("model", "?"), cfg.get("effort") or "default", len(posts)), ""]
    rep += ["## 1. Reply shape and structural checks", "",
            md_table([stats[s] for s in sources], ["source", "n_replies", "words_per_reply", "sentences_per_reply", "labels_per_reply", "pct_sentences_labeled",
                                                   "pct_ends_with_question", "pct_validation", "pct_summarizing", "pct_restructuring", "pct_recommendation",
                                                   "recommendations_per_reply", "pct_clinical_referral", "pct_referral_on_risk_posts", "n_risk_posts",
                                                   "pct_self_disclosure", "harmful_instances", "pct_replies_with_harmful", "em_dashes_per_reply", "pct_markdown"]),
            "", "em_dashes_per_reply and pct_markdown (bold, bullets, headings) are style signals: human Reddit replies rarely have either.", ""]
    rows = []
    for l in LABEL_NAMES:
        row = {"label": l}
        for s in sources:
            row[s + " per100"] = profiles[s][l]
            row[s + " %replies"] = 100.0 * stats[s]["replies_with"].get(l, 0) / max(1, stats[s]["n_replies"])
        rows.append(row)
    rows.sort(key=lambda r: -max(r[s + " per100"] for s in sources))
    rep += ["## 2. Technique profile: label instances per 100 sentences, and % of replies containing the label", "",
            md_table(rows, ["label"] + [s + " per100" for s in sources] + [s + " %replies" for s in sources]), ""]
    if "human" in sources:
        rep += ["## 3. Distance of each condition's label distribution from the human replies (Jensen-Shannon divergence, bits; 0 = identical)", "",
                "The second column drops Self-Disclosure before comparing: humans anchor replies in their own experience, which the "
                "skill forbids the model to fabricate, so that label should not count against it.", ""]
        no_sd = lambda c: {k: v for k, v in c.items() if k != "Self-Disclosure"}
        rep += [md_table([{"source": s, "JS divergence vs human": js_divergence(stats[s]["counts"], stats["human"]["counts"]),
                           "JS divergence vs human, excluding Self-Disclosure": js_divergence(no_sd(stats[s]["counts"]), no_sd(stats["human"]["counts"]))}
                          for s in sources if s != "human"],
                         ["source", "JS divergence vs human", "JS divergence vs human, excluding Self-Disclosure"]), ""]
    if "bare" in sources and "skill" in sources:
        pids = [pid for pid in posts if (pid, "bare") in ann and (pid, "skill") in ann]
        rows = []
        for l in CORE + HARMFUL:
            b = [sum(1 for labs in ann[(pid, "bare")]["labels"] if l in labs) for pid in pids]
            k = [sum(1 for labs in ann[(pid, "skill")]["labels"] if l in labs) for pid in pids]
            rows.append({"label": l, "bare mean/reply": sum(b) / max(1, len(pids)), "skill mean/reply": sum(k) / max(1, len(pids)),
                         "posts skill>bare": sum(1 for x, y in zip(b, k) if y > x), "posts skill<bare": sum(1 for x, y in zip(b, k) if y < x), "n_posts": len(pids)})
        rep += ["## 4. Paired comparison per post (same post, bare vs skill)", "", md_table(rows, ["label", "bare mean/reply", "skill mean/reply", "posts skill>bare", "posts skill<bare", "n_posts"]), ""]
    refusals = [(k, r) for k, r in replies.items() if r.get("stop_reason") == "refusal" or r.get("error")]
    rep += ["## 5. Refusals and errors", "", "%d of %d requests refused or errored." % (len(refusals), len(replies)), ""]
    for (pid, c), r in refusals:
        rep.append("- %s / %s: %s" % (pid, c, r.get("error") or "refusal"))
    open(os.path.join(run_dir, "report.md"), "w", encoding="utf-8").write("\n".join(rep))

    sbs = ["# Side by side: %s" % args.run, ""]
    for pid, p in posts.items():
        if (pid, "bare") not in replies and (pid, "skill") not in replies:
            continue
        sbs += ["---", "", "## %s  (r/%s, %s%s)" % (pid, p["subreddit"], p["focal_point"] or "no focal point", ", RISK CUE" if p["risk_cue"] else ""), "",
                "**Title:** %s" % p["title"], "", "**Post:** %s" % p["body"], ""]
        for s in ("bare", "skill"):
            r = replies.get((pid, s))
            if r:
                labs = ann.get((pid, s), {}).get("labels")
                tag = " | labels: " + ", ".join(sorted({x for l in labs for x in l})) if labs else ""
                sbs += ["**%s reply** (%d words%s)" % (s.upper(), len(r.get("text", "").split()), tag), "", r.get("text") or "(%s)" % (r.get("error") or r.get("stop_reason")), ""]
        gl = ", ".join(sorted({x for l in p["human_reply_lines"] for x in l["labels"]}))
        sbs += ["**HUMAN first reply** (%d words | gold labels: %s)" % (len(p["human_reply"].split()), gl or "none"), "", p["human_reply"], ""]
    open(os.path.join(run_dir, "side_by_side.md"), "w", encoding="utf-8").write("\n".join(sbs))
    json.dump(dict(stats=stats, profiles=profiles), open(os.path.join(run_dir, "summary.json"), "w", encoding="utf-8"), indent=1)
    print("wrote report.md, side_by_side.md, summary.json to", run_dir)
    for s in sources:
        st = stats[s]
        print("%-10s n=%3d words=%5.1f validation=%4.0f%% restructuring=%4.0f%% referral=%4.0f%% recs/reply=%.1f harmful=%d" %
              (s, st["n_replies"], st["words_per_reply"], st["pct_validation"], st["pct_restructuring"], st["pct_clinical_referral"], st["recommendations_per_reply"], st["harmful_instances"]))


if __name__ == "__main__":
    main()
