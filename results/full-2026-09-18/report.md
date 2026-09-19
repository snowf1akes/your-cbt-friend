# your-cbt-friend experiment: full

Model: claude-opus-5, effort: default. Test posts: 53. Sources: bare = Claude with a one-line instruction; skill = Claude with the your-cbt-friend skill in the system prompt; human = first human reply, labeled by the same annotator model; human_gold = the same human reply with the team's adjudicated labels.

## 1. Reply shape and structural checks

| source | n_replies | words_per_reply | sentences_per_reply | labels_per_reply | pct_sentences_labeled | pct_ends_with_question | pct_validation | pct_summarizing | pct_restructuring | pct_recommendation | recommendations_per_reply | pct_clinical_referral | pct_referral_on_risk_posts | n_risk_posts | pct_self_disclosure | harmful_instances | pct_replies_with_harmful | em_dashes_per_reply | pct_markdown |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bare | 53 | 430.2 | 25.7 | 28.1 | 78.2 | 7.5 | 96.2 | 30.2 | 90.6 | 98.1 | 9.0 | 77.4 | 80.0 | 5 | 52.8 | 2 | 1.9 | 5.3 | 73.6 |
| skill | 53 | 161.8 | 7.9 | 10.2 | 91.0 | 96.2 | 98.1 | 47.2 | 79.2 | 100.0 | 2.6 | 69.8 | 80.0 | 5 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| human | 53 | 85.5 | 6.2 | 6.7 | 75.9 | 13.2 | 54.7 | 0.0 | 32.1 | 60.4 | 1.4 | 18.9 | 0.0 | 5 | 54.7 | 6 | 7.5 | 0.0 | 1.9 |
| human_gold | 53 | 85.5 | 6.2 | 7.5 | 82.5 | 13.2 | 39.6 | 3.8 | 32.1 | 71.7 | 2.2 | 18.9 | 0.0 | 5 | 62.3 | 1 | 1.9 | 0.0 | 1.9 |

em_dashes_per_reply and pct_markdown (bold, bullets, headings) are style signals: human Reddit replies rarely have either.

## 2. Technique profile: label instances per 100 sentences, and % of replies containing the label

| label | bare per100 | skill per100 | human per100 | human_gold per100 | bare %replies | skill %replies | human %replies | human_gold %replies |
|---|---|---|---|---|---|---|---|---|
| Self-Disclosure | 6.7 | 0.0 | 30.5 | 41.7 | 52.8 | 0.0 | 54.7 | 62.3 |
| Recommendation | 35.0 | 33.3 | 22.0 | 35.0 | 98.1 | 100.0 | 60.4 | 71.7 |
| Restructuring | 17.4 | 18.3 | 10.7 | 16.6 | 90.6 | 79.2 | 32.1 | 32.1 |
| Focal Point (Request) | 0.7 | 13.1 | 4.6 | 2.7 | 17.0 | 96.2 | 26.4 | 15.1 |
| Validation | 5.0 | 12.6 | 8.8 | 6.3 | 96.2 | 98.1 | 54.7 | 39.6 |
| Psychoeducation | 12.5 | 8.3 | 2.7 | 1.8 | 79.2 | 49.1 | 13.2 | 9.4 |
| Clinical Referral | 7.0 | 11.4 | 3.7 | 3.3 | 77.4 | 69.8 | 18.9 | 18.9 |
| Cognitive Conceptualization | 7.3 | 7.1 | 8.2 | 1.8 | 83.0 | 41.5 | 30.2 | 7.5 |
| Summarizing | 1.8 | 6.2 | 0.0 | 0.6 | 30.2 | 47.2 | 0.0 | 3.8 |
| Social Support | 4.6 | 4.0 | 5.2 | 2.7 | 54.7 | 26.4 | 22.6 | 11.3 |
| Grounding Technique | 2.5 | 3.1 | 4.6 | 4.8 | 30.2 | 18.9 | 7.5 | 7.5 |
| Journal / Thought Record | 1.0 | 3.6 | 0.0 | 0.3 | 22.6 | 28.3 | 0.0 | 1.9 |
| Encouraging Self-Compassion | 2.4 | 1.7 | 0.9 | 1.5 | 47.2 | 9.4 | 5.7 | 3.8 |
| Reflection | 1.2 | 2.4 | 1.8 | 0.3 | 24.5 | 18.9 | 7.5 | 1.9 |
| Acceptance | 2.2 | 2.1 | 0.6 | 0.0 | 32.1 | 17.0 | 3.8 | 0.0 |
| Bad Advice | 0.0 | 0.0 | 1.8 | 0.3 | 0.0 | 0.0 | 7.5 | 1.9 |
| Body Mindfulness | 0.4 | 0.2 | 1.2 | 0.3 | 9.4 | 1.9 | 3.8 | 1.9 |
| Gratitude | 0.4 | 0.5 | 0.6 | 0.6 | 5.7 | 1.9 | 3.8 | 3.8 |
| Goal Setting | 0.6 | 0.2 | 0.0 | 0.0 | 11.3 | 1.9 | 0.0 | 0.0 |
| Cognitive Distortion | 0.1 | 0.2 | 0.3 | 0.0 | 1.9 | 1.9 | 1.9 | 0.0 |
| Non-Expert Diagnosis | 0.1 | 0.0 | 0.0 | 0.0 | 1.9 | 0.0 | 0.0 | 0.0 |
| Focal Point (Complaint) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Focal Point (Statement) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Incorrect Information | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Confirmation Bias | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## 3. Distance of each condition's label distribution from the human replies (Jensen-Shannon divergence, bits; 0 = identical)

The second column drops Self-Disclosure before comparing: humans anchor replies in their own experience, which the skill forbids the model to fabricate, so that label should not count against it.

| source | JS divergence vs human | JS divergence vs human, excluding Self-Disclosure |
|---|---|---|
| bare | 0.145 | 0.096 |
| skill | 0.229 | 0.086 |
| human_gold | 0.055 | 0.075 |

## 4. Paired comparison per post (same post, bare vs skill)

| label | bare mean/reply | skill mean/reply | posts skill>bare | posts skill<bare | n_posts |
|---|---|---|---|---|---|
| Validation | 1.3 | 1.0 | 2 | 12 | 53 |
| Summarizing | 0.5 | 0.5 | 15 | 8 | 53 |
| Restructuring | 4.5 | 1.5 | 4 | 42 | 53 |
| Recommendation | 9.0 | 2.6 | 3 | 49 | 53 |
| Clinical Referral | 1.8 | 0.9 | 1 | 30 | 53 |
| Encouraging Self-Compassion | 0.6 | 0.1 | 1 | 20 | 53 |
| Grounding Technique | 0.6 | 0.2 | 1 | 13 | 53 |
| Journal / Thought Record | 0.2 | 0.3 | 7 | 5 | 53 |
| Social Support | 1.2 | 0.3 | 2 | 26 | 53 |
| Psychoeducation | 3.2 | 0.7 | 0 | 38 | 53 |
| Cognitive Conceptualization | 1.9 | 0.6 | 3 | 36 | 53 |
| Self-Disclosure | 1.7 | 0.0 | 0 | 28 | 53 |
| Focal Point (Request) | 0.2 | 1.0 | 44 | 0 | 53 |
| Acceptance | 0.6 | 0.2 | 6 | 16 | 53 |
| Reflection | 0.3 | 0.2 | 5 | 9 | 53 |
| Bad Advice | 0.0 | 0.0 | 0 | 0 | 53 |
| Incorrect Information | 0.0 | 0.0 | 0 | 0 | 53 |
| Non-Expert Diagnosis | 0.0 | 0.0 | 0 | 1 | 53 |

## 5. Refusals and errors

0 of 106 requests refused or errored.

## 6. Annotator check: model labels versus the team's labels on the same human replies

Reply-level presence of each label (53 human replies). This bounds how far to trust differences between conditions: a gap between bare and skill that is smaller than the annotator's own disagreement with the team is noise.

| label | replies with label (model annotator) | replies with label (team) | pct agreement | kappa (reply level) |
|---|---|---|---|---|
| Recommendation | 32 | 38 | 88.7 | 0.75 |
| Self-Disclosure | 29 | 33 | 88.7 | 0.77 |
| Validation | 29 | 21 | 84.9 | 0.70 |
| Restructuring | 17 | 17 | 88.7 | 0.74 |
| Focal Point (Request) | 14 | 8 | 84.9 | 0.55 |
| Cognitive Conceptualization | 16 | 4 | 77.4 | 0.32 |
| Clinical Referral | 10 | 10 | 92.5 | 0.75 |
| Social Support | 12 | 6 | 88.7 | 0.61 |
| Psychoeducation | 7 | 5 | 88.7 | 0.44 |
| Grounding Technique | 4 | 4 | 100.0 | 1.00 |
| Reflection | 4 | 1 | 94.3 | 0.38 |
| Bad Advice | 4 | 1 | 90.6 | -0.03 |
| Encouraging Self-Compassion | 3 | 2 | 94.3 | 0.37 |
| Gratitude | 2 | 2 | 100.0 | 1.00 |
| Body Mindfulness | 2 | 1 | 98.1 | 0.66 |
| Summarizing | 0 | 2 | 96.2 | 0.00 |
| Acceptance | 2 | 0 | 96.2 | 0.00 |
| Cognitive Distortion | 1 | 0 | 98.1 | 0.00 |
| Journal / Thought Record | 0 | 1 | 98.1 | 0.00 |
