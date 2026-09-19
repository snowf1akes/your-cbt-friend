# your-cbt-friend experiment: pilot2

Model: claude-opus-5, effort: default. Test posts: 53. Sources: bare = Claude with a one-line instruction; skill = Claude with the your-cbt-friend skill in the system prompt; human = first human reply, labeled by the same annotator model; human_gold = the same human reply with the team's adjudicated labels.

## 1. Reply shape and structural checks

| source | n_replies | words_per_reply | sentences_per_reply | labels_per_reply | pct_sentences_labeled | pct_ends_with_question | pct_validation | pct_summarizing | pct_restructuring | pct_recommendation | recommendations_per_reply | pct_clinical_referral | pct_referral_on_risk_posts | n_risk_posts | pct_self_disclosure | harmful_instances | pct_replies_with_harmful | em_dashes_per_reply | pct_markdown |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bare | 10 | 441.1 | 27.0 | 28.3 | 74.1 | 10.0 | 100.0 | 50.0 | 90.0 | 100.0 | 7.3 | 90.0 | 100.0 | 1 | 50.0 | 0 | 0.0 | 5.1 | 70.0 |
| skill | 10 | 158.6 | 7.5 | 10.2 | 96.0 | 100.0 | 100.0 | 50.0 | 90.0 | 100.0 | 2.6 | 70.0 | 100.0 | 1 | 0.0 | 0 | 0.0 | 0.0 | 0.0 |
| human | 10 | 93.8 | 7.5 | 8.9 | 88.0 | 0.0 | 60.0 | 0.0 | 50.0 | 80.0 | 1.8 | 20.0 | 0.0 | 1 | 70.0 | 2 | 20.0 | 0.0 | 10.0 |
| human_gold | 10 | 93.8 | 7.5 | 8.2 | 86.7 | 0.0 | 50.0 | 10.0 | 50.0 | 80.0 | 1.9 | 20.0 | 0.0 | 1 | 80.0 | 0 | 0.0 | 0.0 | 10.0 |

em_dashes_per_reply and pct_markdown (bold, bullets, headings) are style signals: human Reddit replies rarely have either.

## 2. Technique profile: label instances per 100 sentences, and % of replies containing the label

| label | bare per100 | skill per100 | human per100 | human_gold per100 | bare %replies | skill %replies | human %replies | human_gold %replies |
|---|---|---|---|---|---|---|---|---|
| Self-Disclosure | 11.5 | 0.0 | 34.7 | 37.3 | 50.0 | 0.0 | 70.0 | 80.0 |
| Recommendation | 27.0 | 34.7 | 24.0 | 25.3 | 100.0 | 100.0 | 80.0 | 80.0 |
| Restructuring | 18.1 | 20.0 | 16.0 | 21.3 | 90.0 | 90.0 | 50.0 | 50.0 |
| Focal Point (Request) | 1.5 | 16.0 | 5.3 | 1.3 | 30.0 | 100.0 | 40.0 | 10.0 |
| Psychoeducation | 13.3 | 5.3 | 4.0 | 2.7 | 90.0 | 20.0 | 20.0 | 10.0 |
| Clinical Referral | 6.7 | 13.3 | 4.0 | 4.0 | 90.0 | 70.0 | 20.0 | 20.0 |
| Validation | 3.7 | 13.3 | 8.0 | 6.7 | 100.0 | 100.0 | 60.0 | 50.0 |
| Cognitive Conceptualization | 6.7 | 12.0 | 5.3 | 1.3 | 90.0 | 70.0 | 30.0 | 10.0 |
| Summarizing | 1.9 | 6.7 | 0.0 | 1.3 | 50.0 | 50.0 | 0.0 | 10.0 |
| Journal / Thought Record | 0.0 | 5.3 | 0.0 | 0.0 | 0.0 | 40.0 | 0.0 | 0.0 |
| Social Support | 4.4 | 5.3 | 5.3 | 1.3 | 60.0 | 40.0 | 30.0 | 10.0 |
| Grounding Technique | 4.8 | 4.0 | 1.3 | 1.3 | 40.0 | 30.0 | 10.0 | 10.0 |
| Acceptance | 3.3 | 0.0 | 1.3 | 0.0 | 70.0 | 0.0 | 10.0 | 0.0 |
| Bad Advice | 0.0 | 0.0 | 2.7 | 0.0 | 0.0 | 0.0 | 20.0 | 0.0 |
| Encouraging Self-Compassion | 0.7 | 0.0 | 2.7 | 2.7 | 20.0 | 0.0 | 20.0 | 10.0 |
| Gratitude | 0.0 | 0.0 | 2.7 | 2.7 | 0.0 | 0.0 | 10.0 | 10.0 |
| Reflection | 0.7 | 0.0 | 1.3 | 0.0 | 20.0 | 0.0 | 10.0 | 0.0 |
| Body Mindfulness | 0.4 | 0.0 | 0.0 | 0.0 | 10.0 | 0.0 | 0.0 | 0.0 |
| Focal Point (Complaint) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Focal Point (Statement) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Cognitive Distortion | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Non-Expert Diagnosis | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Incorrect Information | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Confirmation Bias | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Goal Setting | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## 3. Distance of each condition's label distribution from the human replies (Jensen-Shannon divergence, bits; 0 = identical)

The second column drops Self-Disclosure before comparing: humans anchor replies in their own experience, which the skill forbids the model to fabricate, so that label should not count against it.

| source | JS divergence vs human | JS divergence vs human, excluding Self-Disclosure |
|---|---|---|
| bare | 0.1 | 0.1 |
| skill | 0.3 | 0.1 |
| human_gold | 0.1 | 0.1 |

## 4. Paired comparison per post (same post, bare vs skill)

| label | bare mean/reply | skill mean/reply | posts skill>bare | posts skill<bare | n_posts |
|---|---|---|---|---|---|
| Validation | 1.0 | 1.0 | 0 | 0 | 10 |
| Summarizing | 0.5 | 0.5 | 3 | 3 | 10 |
| Restructuring | 4.9 | 1.5 | 0 | 9 | 10 |
| Recommendation | 7.3 | 2.6 | 0 | 9 | 10 |
| Clinical Referral | 1.8 | 1.0 | 0 | 5 | 10 |
| Encouraging Self-Compassion | 0.2 | 0.0 | 0 | 2 | 10 |
| Grounding Technique | 1.3 | 0.3 | 1 | 3 | 10 |
| Journal / Thought Record | 0.0 | 0.4 | 4 | 0 | 10 |
| Social Support | 1.2 | 0.4 | 1 | 6 | 10 |
| Psychoeducation | 3.6 | 0.4 | 0 | 9 | 10 |
| Cognitive Conceptualization | 1.8 | 0.9 | 1 | 6 | 10 |
| Self-Disclosure | 3.1 | 0.0 | 0 | 5 | 10 |
| Focal Point (Request) | 0.4 | 1.2 | 8 | 0 | 10 |
| Acceptance | 0.9 | 0.0 | 0 | 7 | 10 |
| Reflection | 0.2 | 0.0 | 0 | 2 | 10 |
| Bad Advice | 0.0 | 0.0 | 0 | 0 | 10 |
| Incorrect Information | 0.0 | 0.0 | 0 | 0 | 10 |
| Non-Expert Diagnosis | 0.0 | 0.0 | 0 | 0 | 10 |

## 5. Refusals and errors

0 of 20 requests refused or errored.
