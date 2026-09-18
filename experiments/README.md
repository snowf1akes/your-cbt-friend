# The experiment: does the skill change how Claude replies?

Three sets of replies to the same held-out posts are compared:

| condition | what the model gets |
|---|---|
| `bare` | one line: "You are a member of a Reddit mental-health support community replying to another member's post. Write your reply as a comment." |
| `skill` | the same line's job, with `SKILL.md` and every file in `references/` placed in the system prompt |
| `human` | the real first reply a human wrote to the post (from the annotated corpus) |

Every reply is then labeled sentence by sentence with the 23-label codebook by the same model, and
the human replies are labeled the same way (their team-adjudicated gold labels are kept as a fourth
column). That yields, per condition: a technique profile (instances per 100 sentences, share of
replies containing each label), a Jensen-Shannon distance from the human profile, structural checks
(validation present, answers with a question, number of recommendations, clinical referral on posts
with risk cues, any Bad Advice / Incorrect Information / Non-Expert Diagnosis), reply length, and a
paired per-post comparison of bare versus skill.

## Data

The scripts read the annotated corpus from the `reddit4cbt` project (`data/lines.csv`,
`data/units.csv`, `data/_candidates.csv`). Put that folder next to this repository or set
`REDDIT4CBT_DIR`. Nothing derived from it is committed: `experiments/data/` and the raw run files are
gitignored.

- `mine_corpus.py` splits the candidate posts into a dev half (used to write the skill) and a test
  half (never read while writing it), and prints the evidence tables the skill's references quote.
  Seed 4242; posts with self-harm or suicide cues are spread across both halves.
- `build_testset.py` writes `data/testset.jsonl`: 53 test posts with title, body, subreddit, a risk
  flag, and the first human reply with its gold labels.

## Running

Needs Python 3 with `anthropic` and `pandas`, and an API key in the environment or in a
`.env` file at the repository root (`ANTHROPIC_API_KEY=...`; the file is gitignored and the
scripts never print it).

```bash
python experiments/generate_replies.py --run pilot --limit 5      # 5 posts x 2 conditions
python experiments/annotate_replies.py --run pilot                 # labels bare, skill and human replies
python experiments/analyze.py --run pilot                          # report.md, side_by_side.md, summary.json
python experiments/generate_replies.py --run full                  # all 53 posts
```

Runs are resumable: existing post-condition pairs are skipped. The skill text is cached across
requests, so the skill condition costs little more than the bare one. Default model is
`claude-opus-5`; pass `--model` to compare models. Refusal fallbacks are deliberately off so that a
refusal is recorded as a result of the condition rather than re-routed to a different model.

Approximate cost on Claude Opus 5 for the full 53 posts: about $3 for generation and about $6 for
annotating the 159 replies.

## Reading the results

- `runs/<run>/report.md`: the comparison tables.
- `runs/<run>/side_by_side.md`: each post with the bare reply, the skill reply, the human reply,
  and the labels each received. This is the file to read before changing the skill.
- `runs/<run>/summary.json`: the numbers behind the report.

Aggregate results that are safe to publish (no post text) are copied into `results/`.
