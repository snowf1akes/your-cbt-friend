"""
mine_corpus.py -- evidence base for the your-cbt-friend skill.

1. Splits the candidate posts (primary posts with an OP body and a human first reply) into a DEV half
   (mined to write the skill) and a TEST half (held out for the with-skill vs without-skill experiment).
   Posts with self-harm / suicide cues are spread across both halves so the safety protocol can be tested.
2. From DEV posts only, extracts the responder lines tagged Recommendation (and not Bad Advice), buckets
   them into recommendation types with keyword rules, and reports counts, co-labels, and samples.
3. Reports where in a reply each technique tends to appear (first / middle / last line) and reply length,
   so the skill's reply structure is grounded in what skilled human peers actually do.

Usage:  python experiments/mine_corpus.py   (needs the reddit4cbt corpus folder; set REDDIT4CBT_DIR if it is not next to this repo)
"""
import os, re, random
import pandas as pd

from paths import CORPUS as ROOT, DATA as OUT   # ROOT = the reddit4cbt corpus folder
os.makedirs(OUT, exist_ok=True)
SEED = 4242
TEST_FRACTION = 0.30
MIN_RISK_IN_TEST = 5

lines = pd.read_csv(os.path.join(ROOT, "data", "lines.csv"), keep_default_na=False)
units = pd.read_csv(os.path.join(ROOT, "data", "units.csv"), keep_default_na=False)
cand = pd.read_csv(os.path.join(ROOT, "data", "_candidates.csv"), keep_default_na=False)
for df in (lines, units):
    for c in df.columns:
        if c.startswith(("n_", "is_", "thread_idx", "comment_idx", "line_idx", "lbl_", "author_deleted")):
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
cand["risk_cue"] = pd.to_numeric(cand.risk_cue, errors="coerce").fillna(0).astype(int)

# ------------------------------------------------------------------ 1. dev / test split
rng = random.Random(SEED)
test_ids = set()
risk_posts = list(cand[cand.risk_cue == 1].post_id)
rng.shuffle(risk_posts)
test_ids.update(risk_posts[:MIN_RISK_IN_TEST])
for sub, g in cand[cand.risk_cue == 0].groupby("subreddit"):
    ids = list(g.post_id)
    rng.shuffle(ids)
    k = max(1, round(len(ids) * TEST_FRACTION)) if len(ids) >= 2 else 0
    test_ids.update(ids[:k])
cand["split"] = cand.post_id.map(lambda p: "test" if p in test_ids else "dev")
cand.to_csv(os.path.join(OUT, "split.csv"), index=False)
print("split:", cand.split.value_counts().to_dict(), "| risk-cue posts in test:", int(cand[(cand.split == "test")].risk_cue.sum()))
print(cand.groupby(["subreddit", "split"]).size().unstack(fill_value=0).to_string())

dev_posts = set(cand[cand.split == "dev"].post_id)
resp = lines[(lines.is_primary_post == 1) & (lines.speaker_role == "responder") & (lines.unit_type == "comment")
             & (lines.annotation_status.isin(["labeled", "no_label"]))]
dev_resp = resp[resp.post_id.isin(dev_posts)]

# ------------------------------------------------------------------ 2. recommendation lines (DEV)
rec = dev_resp[(dev_resp.lbl_recommendation == 1) & (dev_resp.lbl_bad_advice == 0)].copy()
TAXONOMY = [
    ("professional help", r"therap|counsel|psychiatr|psycholog|doctor|\bgp\b|physician|clinic|professional|treatment|medication|meds\b|prescri"),
    ("breathing / grounding", r"breath|ground|5-4-3-2-1|54321|meditat|mindful|relax|calm down|body scan|cold water|ice"),
    ("journaling / thought record", r"journal|write (it|them|things|down)|writing|thought record|diary|list of|log\b"),
    ("challenge the thought", r"evidence|challenge|reframe|question (the|your)|distortion|catastroph|worst case|is it true|realistic|perspective"),
    ("exposure / small steps", r"expos|small step|baby step|gradual|little by little|one step|start small|practice|push yourself|face"),
    ("exercise / body", r"exercise|walk|run\b|running|gym|workout|yoga|stretch|movement|sport"),
    ("sleep / routine / basics", r"sleep|routine|schedule|structure|bedtime|eat\b|eating regular|hydrat|water|caffeine|alcohol|drink"),
    ("social support", r"friend|family|talk to (someone|people|a)|support group|community|reach out|not alone|people who"),
    ("self-compassion / patience", r"kind to yourself|gentle|compassion|forgive yourself|be patient|give yourself|proud of|deserve|it's okay|its okay"),
    ("books / apps / resources", r"book|app\b|apps\b|podcast|youtube|video|workbook|website|read\b|reading|feeling good|burns|course|resource"),
    ("acceptance / letting go", r"accept|let (it|go)|sit with|allow|notice|observe|pass|it will pass|ride it out"),
    ("distraction / activities", r"hobby|hobbies|music|game|distract|activity|activities|something you enjoy|creative|art\b|draw"),
    ("limit triggers / boundaries", r"boundar|avoid|limit|cut (off|out|back)|stop (following|checking)|unfollow|social media|phone"),
]

def bucket(text):
    t = text.lower()
    hits = [name for name, pat in TAXONOMY if re.search(pat, t)]
    return hits or ["other"]

rec["types"] = rec.text.apply(bucket)
rec["co_labels"] = rec.labels.apply(lambda s: "|".join(x for x in s.split("|") if x and x != "Recommendation"))
rec[["post_id", "subreddit", "unit_id", "line_idx", "text", "labels", "types"]].to_csv(os.path.join(OUT, "dev_recommendation_lines.csv"), index=False)
print("\nDEV responder lines:", len(dev_resp), "| Recommendation lines (not Bad Advice):", len(rec),
      "| Bad Advice among all responder Recommendation lines in corpus:", int(((resp.lbl_recommendation == 1) & (resp.lbl_bad_advice == 1)).sum()), "/", int((resp.lbl_recommendation == 1).sum()))
type_counts = pd.Series([t for ts in rec.types for t in ts]).value_counts()
print("\nRecommendation types (a line can hit several):")
print((type_counts / len(rec) * 100).round(1).astype(str).radd(type_counts.astype(str) + "  ").to_string())
print("\nCo-labels on Recommendation lines:")
print(rec.co_labels.replace("", "(none)").value_counts().head(12).to_string())
print("\nRecommendation type by subreddit (share of that subreddit's recommendation lines, %):")
rows = []
for sub, g in rec.groupby("subreddit"):
    tc = pd.Series([t for ts in g.types for t in ts]).value_counts()
    rows.append(dict(subreddit=sub, n=len(g), **{k: round(100 * tc.get(k, 0) / len(g)) for k in ["professional help", "breathing / grounding", "journaling / thought record", "challenge the thought", "exposure / small steps", "exercise / body", "sleep / routine / basics", "social support", "self-compassion / patience", "books / apps / resources"]}))
print(pd.DataFrame(rows).sort_values("n", ascending=False).to_string(index=False))

# ------------------------------------------------------------------ 3. where techniques sit inside a reply; reply length
comments = units[(units.unit_type == "comment") & (units.speaker_role == "responder") & (units.is_primary_post == 1) & (units.post_id.isin(dev_posts)) & (units.n_lines >= 3)]
pos_rows = []
for uid, g in dev_resp[dev_resp.unit_id.isin(comments.unit_id)].groupby("unit_id"):
    g = g.sort_values("line_idx")
    n = len(g)
    for i, (_, r) in enumerate(g.iterrows()):
        pos = "first" if i == 0 else ("last" if i == n - 1 else "middle")
        for lab in [x for x in r.labels.split("|") if x]:
            pos_rows.append((pos, lab))
pos = pd.DataFrame(pos_rows, columns=["pos", "label"])
n_first = comments.shape[0]
n_last = n_first
n_mid = int(comments.n_lines.sum() - 2 * n_first)
tab = pos.groupby(["label", "pos"]).size().unstack(fill_value=0)
for col, denom in (("first", n_first), ("middle", n_mid), ("last", n_last)):
    if col in tab:
        tab[col + "_per100"] = (100 * tab[col] / denom).round(1)
print("\nTechnique placement inside responder replies with >= 3 lines (DEV, n=%d replies): rate per 100 lines at that position" % n_first)
print(tab[[c for c in tab.columns if c.endswith("_per100")]].sort_values("first_per100", ascending=False).to_string())
print("\nResponder reply length (DEV, first replies and all replies): lines / words quantiles")
allc = units[(units.unit_type == "comment") & (units.speaker_role == "responder") & (units.is_primary_post == 1) & (units.post_id.isin(dev_posts))]
print("  all replies   lines:", allc.n_lines.quantile([.25, .5, .75, .9]).round(1).to_dict(), " words:", allc.n_words.quantile([.25, .5, .75, .9]).round(0).to_dict())
first_reply = cand[cand.split == "dev"].ref_unit
fr = allc[allc.unit_id.isin(first_reply)]
print("  first replies lines:", fr.n_lines.quantile([.25, .5, .75, .9]).round(1).to_dict(), " words:", fr.n_words.quantile([.25, .5, .75, .9]).round(0).to_dict())

# ------------------------------------------------------------------ 4. samples to learn the register (printed for the skill author; not copied verbatim into the skill)
def show(title, df, k, seed=1):
    print("\n### %s (%d available, showing %d)" % (title, len(df), min(k, len(df))))
    for _, r in df.sample(min(k, len(df)), random_state=seed).iterrows():
        print("- [%s] %s" % (r.subreddit[:12], r.text[:170]))

for name, _ in TAXONOMY:
    sub = rec[rec.types.apply(lambda ts: name in ts)]
    show("Recommendation: " + name, sub, 8)
show("Recommendation: other", rec[rec.types.apply(lambda ts: ts == ["other"])], 12)
show("Clinical Referral lines", dev_resp[dev_resp.lbl_clinical_referral == 1], 14, seed=2)
show("Validation lines", dev_resp[dev_resp.lbl_validation == 1], 16, seed=3)
show("Restructuring lines", dev_resp[dev_resp.lbl_restructuring == 1], 18, seed=4)
show("Encouraging Self-Compassion lines", dev_resp[dev_resp.lbl_self_compassion == 1], 10, seed=5)
show("Summarizing lines", dev_resp[dev_resp.lbl_summarizing == 1], 8, seed=6)
show("Psychoeducation lines", dev_resp[dev_resp.lbl_psychoeducation == 1], 10, seed=7)
show("Bad Advice lines (what to avoid)", resp[resp.lbl_bad_advice == 1], 12, seed=8)
show("Incorrect Information lines (what to avoid)", resp[resp.lbl_incorrect_info == 1], 8, seed=9)
show("Non-Expert Diagnosis lines (what to avoid)", resp[resp.lbl_nonexpert_diagnosis == 1], 6, seed=10)
