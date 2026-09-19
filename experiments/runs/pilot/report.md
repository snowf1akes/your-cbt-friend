# your-cbt-friend experiment: pilot

Model: claude-opus-5, effort: default. Test posts: 53. Sources: bare = Claude with a one-line instruction; skill = Claude with the your-cbt-friend skill in the system prompt; human = first human reply, labeled by the same annotator model; human_gold = the same human reply with the team's adjudicated labels.

## 1. Reply shape and structural checks

| source | n_replies | words_per_reply | sentences_per_reply | labels_per_reply | pct_sentences_labeled | pct_ends_with_question | pct_validation | pct_summarizing | pct_restructuring | pct_recommendation | recommendations_per_reply | pct_clinical_referral | pct_referral_on_risk_posts | n_risk_posts | pct_self_disclosure | harmful_instances | pct_replies_with_harmful |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bare | 5 | 384.2 | 24.4 | 29.4 | 82.0 | 0.0 | 100.0 | 40.0 | 100.0 | 100.0 | 9.0 | 60.0 | nan | 0 | 80.0 | 0 | 0.0 |
| skill | 5 | 244.2 | 9.8 | 15.2 | 93.9 | 100.0 | 100.0 | 60.0 | 80.0 | 100.0 | 3.6 | 100.0 | nan | 0 | 0.0 | 0 | 0.0 |
| human | 5 | 47.6 | 3.4 | 5.4 | 94.1 | 0.0 | 40.0 | 0.0 | 0.0 | 80.0 | 1.6 | 20.0 | nan | 0 | 60.0 | 2 | 40.0 |
| human_gold | 5 | 47.6 | 3.4 | 5.0 | 94.1 | 0.0 | 40.0 | 0.0 | 20.0 | 100.0 | 2.2 | 20.0 | nan | 0 | 60.0 | 0 | 0.0 |

## 2. Technique profile: label instances per 100 sentences, and % of replies containing the label

| label | bare per100 | skill per100 | human per100 | human_gold per100 | bare %replies | skill %replies | human %replies | human_gold %replies |
|---|---|---|---|---|---|---|---|---|
| Recommendation | 36.9 | 36.7 | 47.1 | 64.7 | 100.0 | 100.0 | 80.0 | 100.0 |
| Self-Disclosure | 18.9 | 0.0 | 41.2 | 41.2 | 80.0 | 0.0 | 60.0 | 60.0 |
| Social Support | 5.7 | 4.1 | 17.6 | 5.9 | 40.0 | 40.0 | 40.0 | 20.0 |
| Psychoeducation | 11.5 | 16.3 | 0.0 | 0.0 | 100.0 | 80.0 | 0.0 | 0.0 |
| Restructuring | 14.8 | 16.3 | 0.0 | 5.9 | 100.0 | 80.0 | 0.0 | 20.0 |
| Clinical Referral | 5.7 | 16.3 | 11.8 | 11.8 | 60.0 | 100.0 | 20.0 | 20.0 |
| Focal Point (Request) | 2.5 | 14.3 | 11.8 | 0.0 | 40.0 | 100.0 | 40.0 | 0.0 |
| Cognitive Conceptualization | 5.7 | 14.3 | 5.9 | 5.9 | 60.0 | 80.0 | 20.0 | 20.0 |
| Bad Advice | 0.0 | 0.0 | 11.8 | 0.0 | 0.0 | 0.0 | 40.0 | 0.0 |
| Validation | 4.1 | 10.2 | 11.8 | 11.8 | 100.0 | 100.0 | 40.0 | 40.0 |
| Grounding Technique | 4.9 | 10.2 | 0.0 | 0.0 | 40.0 | 80.0 | 0.0 | 0.0 |
| Summarizing | 1.6 | 8.2 | 0.0 | 0.0 | 40.0 | 60.0 | 0.0 | 0.0 |
| Journal / Thought Record | 0.0 | 4.1 | 0.0 | 0.0 | 0.0 | 40.0 | 0.0 | 0.0 |
| Acceptance | 1.6 | 4.1 | 0.0 | 0.0 | 40.0 | 40.0 | 0.0 | 0.0 |
| Encouraging Self-Compassion | 3.3 | 0.0 | 0.0 | 0.0 | 60.0 | 0.0 | 0.0 | 0.0 |
| Body Mindfulness | 2.5 | 0.0 | 0.0 | 0.0 | 40.0 | 0.0 | 0.0 | 0.0 |
| Goal Setting | 0.8 | 0.0 | 0.0 | 0.0 | 20.0 | 0.0 | 0.0 | 0.0 |
| Focal Point (Complaint) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Focal Point (Statement) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Cognitive Distortion | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Reflection | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Non-Expert Diagnosis | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Incorrect Information | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Confirmation Bias | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Gratitude | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## 3. Distance of each condition's label distribution from the human replies (Jensen-Shannon divergence, bits; 0 = identical)

| source | JS divergence vs human (same annotator) |
|---|---|
| bare | 0.2 |
| skill | 0.4 |
| human_gold | 0.1 |

## 4. Paired comparison per post (same post, bare vs skill)

| label | bare mean/reply | skill mean/reply | posts skill>bare | posts skill<bare | n_posts |
|---|---|---|---|---|---|
| Validation | 1.0 | 1.0 | 0 | 0 | 5 |
| Summarizing | 0.4 | 0.8 | 2 | 1 | 5 |
| Restructuring | 3.6 | 1.6 | 0 | 4 | 5 |
| Recommendation | 9.0 | 3.6 | 0 | 5 | 5 |
| Clinical Referral | 1.4 | 1.6 | 2 | 1 | 5 |
| Encouraging Self-Compassion | 0.8 | 0.0 | 0 | 3 | 5 |
| Grounding Technique | 1.2 | 1.0 | 2 | 1 | 5 |
| Journal / Thought Record | 0.0 | 0.4 | 2 | 0 | 5 |
| Social Support | 1.4 | 0.4 | 0 | 1 | 5 |
| Psychoeducation | 2.8 | 1.6 | 1 | 4 | 5 |
| Cognitive Conceptualization | 1.4 | 1.4 | 2 | 2 | 5 |
| Self-Disclosure | 4.6 | 0.0 | 0 | 4 | 5 |
| Focal Point (Request) | 0.6 | 1.4 | 4 | 0 | 5 |
| Acceptance | 0.4 | 0.4 | 1 | 1 | 5 |
| Reflection | 0.0 | 0.0 | 0 | 0 | 5 |
| Bad Advice | 0.0 | 0.0 | 0 | 0 | 5 |
| Incorrect Information | 0.0 | 0.0 | 0 | 0 | 5 |
| Non-Expert Diagnosis | 0.0 | 0.0 | 0 | 0 | 5 |

## 5. Refusals and errors

0 of 10 requests refused or errored.
