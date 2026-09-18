# Your CBT Friend

A skill for Claude that changes how it responds to someone who is struggling: instead of a
generic sympathetic reply, it answers the way the best peer supporters in Reddit mental-health
communities do, informed by cognitive behavioral therapy (CBT). Validate something specific
first, reflect back what the person said, answer what they actually asked, gently examine one
unhelpful thought, offer one to three concrete suggestions that fit the situation, and point to
professional help when it is warranted, with a crisis protocol that takes over when there is
any sign of risk.

## Read this first

- **It is experimental and it is not therapy.** AI can be inaccurate, can miss signs of risk,
  and does not know the person. Nothing this skill produces is medical advice or a substitute
  for a qualified professional or emergency services. If you or someone you know is in crisis,
  contact your local emergency number or a crisis line such as 988 in the US.
- **No liability.** The authors publish this to explore how AI might support mental health,
  not as a product. Use it at your own risk; we accept no liability for how replies are used.
- **Think of it as a fun, careful experiment.** The interesting question is whether grounding
  a model in what skilled human peers actually do makes its replies more helpful and safer. We
  are treating it as research for now, and this repository includes the experiment we use to
  find out.

## Where it comes from

The skill was distilled from a research corpus of 217 Reddit mental-health threads across 14
communities, coded sentence by sentence by a team of annotators with a 23-label CBT codebook
(validation, restructuring, recommendation, clinical referral, self-disclosure, bad advice, and
so on) and adjudicated to a final label set. Two things from that corpus drive the skill:

- **The shape of good replies.** Validation appears in the first sentence of human replies ten
  times more often than anywhere else; suggestions cluster in the middle; replies end with a
  last suggestion, encouragement, or a question. Good first replies run 4 to 8 sentences.
- **The vetted suggestions.** About 1,100 responder sentences were tagged Recommendation and only
  five of those were also flagged Bad Advice. What they had in common was specificity to the
  situation, which is why the skill pushes concrete, matched suggestions over generic lists.

Half of the posts were used to write the skill; the other half is held out to test it.

## What is in this repository

```
SKILL.md                              the skill (this is what Claude reads)
references/
  recommendation-playbook.md          what skilled peers actually suggest, by situation
  technique-notes.md                  how to do each move in a peer voice
  evidence-from-corpus.md             the numbers behind the skill
  safety.md                           crisis protocol and red lines
experiments/                          the with-skill vs without-skill experiment (code only)
results/                              aggregate results of the experiment runs
```

The raw Reddit text, the annotated corpus, and generated replies are not in this repository.

## Install

Claude Code: clone the repository into your skills folder and the skill is available in every
session.

```bash
git clone https://github.com/<your-account>/your-cbt-friend ~/.claude/skills/your-cbt-friend
```

Claude.ai: zip the repository folder (SKILL.md at the top level) and upload it as a custom
skill in Settings. Then ask Claude to reply to a post, a message, or your own thoughts, and it
will use the skill.

## The experiment

`experiments/` compares three sets of replies to the same held-out posts: Claude with a one-line
instruction, Claude with this skill, and the real first human reply. Every reply is labeled
sentence by sentence with the same codebook the corpus was annotated with, which gives a
technique profile per condition (how often each reply validates, reframes, recommends, refers,
or does something harmful), a distance from the human profile, structural checks, and a side by
side reading file. See `experiments/README.md` for how to run it; it needs the corpus files from
the annotation project and an Anthropic API key.

## Citation

If you use the skill or the methodology in research, please cite the forthcoming paper on the
annotated corpus (details to be added) and the earlier work this line of research builds on:
Kian et al., "Using Linguistic Entrainment to Evaluate Large Language Models for Use in
Cognitive Behavioral Therapy", Findings of NAACL 2025.

## License

MIT for the code and the skill text. See `LICENSE`.
