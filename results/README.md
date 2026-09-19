# Results

Aggregate outputs of the with-skill versus without-skill experiment. No post text or generated
reply text is stored here; only counts, rates, and figures. Each folder is one run:

| folder | what it was |
|---|---|
| `pilot-2026-09-18` | skill v0.1, 5 held-out r/Anxietyhelp posts |
| `pilot2-2026-09-18` | skill v0.2 (150-word ceiling, one or two suggestions, calibrated referrals), 10 held-out posts across 6 communities including a suicidal-ideation post, an eating-disorder recovery post, and a bereaved teenager |
| `full-2026-09-18` | skill v0.2, all 53 held-out posts |

## How to read a run

- `report.md`, table 1: reply shape and structural checks per condition. `bare` is Claude Opus 5
  with a one-line instruction, `skill` is the same model with the skill in its system prompt,
  `human` is the first direct human reply to the post as labeled by the same annotator model, and
  `human_gold` is that human reply with the research team's adjudicated labels.
- Table 2: the technique profile, label instances per 100 sentences and share of replies that
  contain each label.
- Table 3: Jensen-Shannon divergence between each condition's label distribution and the human
  one. The second column drops Self-Disclosure, because human peers anchor replies in their own
  experience and the skill forbids the model to fabricate any.
- Table 4: paired per-post comparison of bare against skill.
- `summary.json`: the numbers behind the tables. `config.json`: model, effort, prompt sizes.
- `figures/`: the technique-profile chart and the reply-shape chart.

## Caveats

- Labels on generated replies come from the annotator model applying the codebook, not from the
  human annotation team. The `human` versus `human_gold` rows show how far the model annotator
  sits from the team on the same human replies; treat differences smaller than that gap as noise.
- One model, one run per post. Thinking is on by default for Claude Opus 5, so replies vary
  between runs; the pilots and the full run are separate samples, not repeats.
- The human reference is one reply per post, the first direct reply, which is often short and
  sometimes low quality. It anchors "what actually happens on the forum", not "the best reply".
