"""Shared paths for the experiment scripts.

CORPUS is the reddit4cbt annotation project (lines.csv, units.csv, posts.csv). It is not part of this
repository; set REDDIT4CBT_DIR if it is not a sibling folder of this repo.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))                 # experiments/
REPO = os.path.dirname(HERE)                                       # repository root: SKILL.md lives here
CORPUS = os.environ.get("REDDIT4CBT_DIR") or os.path.normpath(os.path.join(REPO, "..", "reddit4cbt"))
DATA = os.path.join(HERE, "data")                                  # split, test set (gitignored)
RUNS = os.path.join(HERE, "runs")                                  # generated replies, annotations, reports
CODEBOOK = os.path.join(HERE, "codebook", "codebook.md")                 # local copy (not committed unless the team decides to publish it)
if not os.path.exists(CODEBOOK):
    CODEBOOK = os.path.join(CORPUS, "skills", "cbt-annotator", "references", "codebook.md")
LABEL_NAMES = ['Focal Point (Complaint)', 'Focal Point (Request)', 'Focal Point (Statement)', 'Psychoeducation', 'Cognitive Distortion', 'Restructuring', 'Reflection', 'Summarizing', 'Cognitive Conceptualization', 'Clinical Referral', 'Recommendation', 'Journal / Thought Record', 'Grounding Technique', 'Non-Expert Diagnosis', 'Incorrect Information', 'Bad Advice', 'Self-Disclosure', 'Social Support', 'Confirmation Bias', 'Validation', 'Encouraging Self-Compassion', 'Goal Setting', 'Body Mindfulness', 'Acceptance', 'Gratitude']
