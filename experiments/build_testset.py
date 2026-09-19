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
units = pd.read_csv(os.path.join(ROOT, "data", "units.csv"), keep_default_na=False)
for c in ("thread_idx", "comment_idx", "n_lines"):
    units[c] = pd.to_numeric(units[c], errors="coerce").fillna(0).astype(int)
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
    # human reference = the first direct reply to the post by a responder (thread 1, comment 1), any length;
    # fall back to the earliest responder comment. A later comment can be a thank-you, not a reply.
    cands = units[(units.post_id == p.post_id) & (units.unit_type == "comment") & (units.speaker_role == "responder")
                  & (units.n_lines >= 1)].sort_values(["thread_idx", "comment_idx"])
    direct = cands[(cands.thread_idx == 1) & (cands.comment_idx == 1)]
    ref_unit = direct.unit_id.iloc[0] if len(direct) else (cands.unit_id.iloc[0] if len(cands) else p.ref_unit)
    ref = pl[(pl.unit_id == ref_unit) & (pl.annotation_status != "blank")].sort_values("line_idx")
    records.append(dict(
        post_id=p.post_id, subreddit=p.subreddit, focal_point=p.focal_point_title, risk_cue=int(p.risk_cue),
        title=title, body=" ".join(body_lines.text).strip(), n_body_sentences=int(len(body_lines)),
        human_reply=" ".join(ref.text).strip(), human_reply_unit=ref_unit, human_reply_is_first_direct=int(len(direct) > 0),
        human_reply_lines=[dict(idx=int(r.line_idx), text=r.text, labels=[x for x in r.labels.split("|") if x]) for _, r in ref.iterrows()],
    ))
out = os.path.join(DATA, "testset.jsonl")
with open(out, "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("wrote %d test posts to %s" % (len(records), out))
print("references that are the first direct reply:", sum(r["human_reply_is_first_direct"] for r in records), "of", len(records))
print("risk-cue posts:", sum(r["risk_cue"] for r in records), "| by subreddit:", test.groupby("subreddit").size().to_dict())
print("median body sentences:", int(pd.Series([r["n_body_sentences"] for r in records]).median()),
      "| median human reply words:", int(pd.Series([len(r["human_reply"].split()) for r in records]).median()))
