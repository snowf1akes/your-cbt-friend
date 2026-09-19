"""
plot_results.py -- figures for a run: technique profile (label instances per 100 sentences) for bare,
skill and human replies, and reply shape (words and suggestions per reply).

Usage:  python experiments/plot_results.py --run full   -> runs/<run>/figures/*.png
"""
import argparse, json, os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from paths import RUNS

# validated default palette: skill = blue, bare = orange, human = aqua
COLORS = {"skill": "#2a78d6", "bare": "#eb6834", "human": "#1baf7a", "human_gold": "#8a8a85"}
LABELS = {"bare": "Claude, one-line instruction", "skill": "Claude + your-cbt-friend", "human": "human first reply (same annotator)",
          "human_gold": "human first reply (team gold labels)"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e6e1"
plt.rcParams.update({"font.family": "Arial", "font.size": 9, "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2})


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#bdbdb8")
    ax.spines["left"].set_color("#bdbdb8")
    ax.tick_params(length=0)
    ax.set_axisbelow(True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--sources", default="bare,skill,human")
    ap.add_argument("--top", type=int, default=12)
    args = ap.parse_args()
    run_dir = os.path.join(RUNS, args.run)
    S = json.load(open(os.path.join(run_dir, "summary.json"), encoding="utf-8"))
    stats, profiles = S["stats"], S["profiles"]
    sources = [s for s in args.sources.split(",") if s in stats]
    out = os.path.join(run_dir, "figures")
    os.makedirs(out, exist_ok=True)
    n = {s: stats[s]["n_replies"] for s in sources}

    # ---- figure 1: technique profile
    labels = sorted(profiles[sources[0]], key=lambda l: -max(profiles[s][l] for s in sources))[:args.top]
    labels = labels[::-1]
    fig, ax = plt.subplots(figsize=(7.4, 0.42 * len(labels) + 1.4), dpi=200)
    fig.patch.set_facecolor("white")
    y = np.arange(len(labels))
    h = 0.8 / len(sources)
    for i, s in enumerate(sources):
        vals = [profiles[s][l] for l in labels]
        ax.barh(y + (i - (len(sources) - 1) / 2) * h, vals, height=h * 0.92, color=COLORS[s], label="%s (n=%d)" % (LABELS[s], n[s]), zorder=3)
        for yi, v in zip(y, vals):
            if v >= 1:
                ax.text(v + 0.4, yi + (i - (len(sources) - 1) / 2) * h, "%.0f" % v, va="center", fontsize=6.5, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=8.5)
    ax.set_xlabel("label instances per 100 sentences", fontsize=8.5, color=INK2)
    ax.xaxis.grid(True, color=GRID, zorder=0)
    style(ax)
    ax.legend(frameon=False, fontsize=7.5, loc="lower right")
    ax.set_title("What each kind of reply does, sentence by sentence", fontsize=10, loc="left", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "fig_technique_profile.png"), facecolor="white")
    plt.close(fig)

    # ---- figure 2: reply shape
    metrics = [("words_per_reply", "words per reply"), ("recommendations_per_reply", "suggestions per reply"),
               ("pct_clinical_referral", "% with a therapy referral"), ("pct_ends_with_question", "% ending with a question")]
    fig, axes = plt.subplots(1, len(metrics), figsize=(1.9 * len(metrics) + 0.6, 2.9), dpi=200)
    fig.patch.set_facecolor("white")
    for ax, (key, title) in zip(axes, metrics):
        vals = [stats[s][key] for s in sources]
        ax.bar(range(len(sources)), vals, color=[COLORS[s] for s in sources], width=0.62, zorder=3)
        for i, v in enumerate(vals):
            ax.text(i, v + max(vals) * 0.02, ("%.0f" % v) if v >= 10 else ("%.1f" % v), ha="center", fontsize=7.5, color=INK)
        ax.set_xticks(range(len(sources)))
        ax.set_xticklabels([s.replace("human", "human") for s in sources], fontsize=8)
        ax.set_title(title, fontsize=8.5, loc="left", color=INK)
        ax.set_ylim(0, max(vals) * 1.18 if max(vals) > 0 else 1)
        ax.yaxis.grid(True, color=GRID, zorder=0)
        style(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "fig_reply_shape.png"), facecolor="white")
    plt.close(fig)
    print("wrote figures to", out)


if __name__ == "__main__":
    main()
