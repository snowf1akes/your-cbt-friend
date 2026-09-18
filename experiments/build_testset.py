"""
build_testset.py -- assemble the held-out TEST posts for the your-cbt-friend experiment.

For every post in the test half of the split (see mine_corpus.py): the OP title and body (sentence lines
re-joined), the subreddit, a self-harm/suicide cue flag, and the first human responder reply with its
gold codebook labels per sentence. Nothing from these posts was used to write the skill.

Output: data/testset.jsonl  (one JSON object per post; contains raw Reddit text -> gitignored)
Usage:  python experiments/build_testset.py
"""
import json, os
import pandas as pd

from paths import CORPUS as ROOT, DATA
lines = pd.read_csv(os.path.join(ROOT, "data", "lines.csv"), keep_default_na=False)
split = pd.read_csv(os.path.join(DATA, "split.csv"), keep_default_na=False)
for c in ("line_idx", "n_body_lines", "risk_cue"):
    if c in lines.columns:
        lines[c] = pd.to_numeric(lines[c], errors="coerce").fillna(0).astype(int)
    if c in split.columns:
        split[c] = pd.to_numeric(split[c], errors="coerce").fillna(0).astype(int)

test = split[split.split == "test"].sort_values(["subreddit", "post_id"])
records = []
for _, p in test.iterrows():
    pl = lines[lines.post_id == p.post_id]
    title = " ".join(pl[pl.unit_type == "title"].sort_values("line_idx").text).strip()
    body_lines = pl[(pl.unit_type == "op_body") & (pl.annotation_status != "blank")].sort_values("line_idx")
    ref = pl[(pl.unit_id == p.ref_unit) & (pl.annotation_status != "blank")].sort_values("line_idx")
    records.append(dict(
        post_id=p.post_id, subreddit=p.subreddit, focal_point=p.focal_point_title, risk_cue=int(p.risk_cue),
        title=title, body=" ".join(body_lines.text).strip(), n_body_sentences=int(len(body_lines)),
        human_reply=" ".join(ref.text).strip(), human_reply_unit=p.ref_unit,
        human_reply_lines=[dict(idx=int(r.line_idx), text=r.text, labels=[x for x in r.labels.split("|") if x]) for _, r in ref.iterrows()],
    ))
out = os.path.join(DATA, "testset.jsonl")
with open(out, "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote %d test posts to %s" % (len(records), out))
print("risk-cue posts:", sum(r["risk_cue"] for r in records), "| by subreddit:", test.groupby("subreddit").size().to_dict())
print("median body sentences:", int(pd.Series([r["n_body_sentences"] for r in records]).median()),
      "| median human reply words:", int(pd.Series([len(r["human_reply"].split()) for r in records]).median()))
