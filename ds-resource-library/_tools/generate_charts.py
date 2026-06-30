"""
Generate the visual assets (PNG charts) embedded in each topic's NOTES.md.

Headless (Agg backend) so it runs anywhere. Saves charts into each topic's
`assets/` folder. Re-run any time to regenerate.

Run:  python _tools/generate_charts.py
Deps: numpy, pandas, scikit-learn, matplotlib
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RNG = np.random.default_rng(42)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10, "axes.grid": True,
                     "grid.alpha": 0.3, "axes.spines.top": False,
                     "axes.spines.right": False})

BLUE, ORANGE, GREEN, RED = "#4C72B0", "#DD8452", "#55A868", "#C44E52"


def save(fig, topic: str, name: str) -> None:
    out_dir = ROOT / topic / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  saved {path.relative_to(ROOT)}")


# --------------------------------------------------------------------------- #
# 01 · Python — vectorization speedup (illustrative, representative numbers)
# --------------------------------------------------------------------------- #
def chart_python():
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    labels = ["Python\nloop", "list\ncomprehension", "NumPy\nvectorized"]
    times = [1200, 800, 12]  # ms, illustrative
    bars = ax.bar(labels, times, color=[RED, ORANGE, GREEN])
    ax.set_ylabel("time (ms, log scale)")
    ax.set_yscale("log")
    ax.set_title("Vectorization: same result, ~100x faster")
    for b, t in zip(bars, times):
        ax.text(b.get_x() + b.get_width() / 2, t, f"{t} ms", ha="center", va="bottom")
    save(fig, "01-python-for-data-science", "vectorization.png")


# --------------------------------------------------------------------------- #
# 03 · Statistics — Central Limit Theorem + a confidence interval
# --------------------------------------------------------------------------- #
def chart_statistics():
    # CLT: means of samples from a skewed (exponential) population look normal.
    pop = RNG.exponential(scale=2.0, size=200_000)
    means = [RNG.choice(pop, size=40).mean() for _ in range(5000)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    a1.hist(pop, bins=60, color=BLUE, alpha=0.8)
    a1.set_title("Population (skewed)")
    a1.set_xlabel("value")
    a2.hist(means, bins=50, color=GREEN, alpha=0.85)
    a2.axvline(np.mean(means), color=RED, lw=2, label="mean of means")
    a2.set_title("Sample means (n=40) → ~Normal (CLT)")
    a2.set_xlabel("sample mean")
    a2.legend()
    fig.suptitle("Central Limit Theorem: averages are ~Normal even when data isn't",
                 fontsize=11)
    save(fig, "03-statistics-and-probability", "clt.png")

    # Confidence interval visual.
    fig, ax = plt.subplots(figsize=(6, 3.2))
    x = np.linspace(-4, 4, 400)
    y = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)
    ax.plot(x, y, color=BLUE)
    ax.fill_between(x, y, where=(x >= -1.96) & (x <= 1.96), color=BLUE, alpha=0.25,
                    label="95% of area")
    for v in (-1.96, 1.96):
        ax.axvline(v, color=RED, ls="--")
    ax.set_title("95% Confidence Interval (±1.96 SE under Normal)")
    ax.set_xlabel("standard errors from estimate")
    ax.set_yticks([])
    ax.legend()
    save(fig, "03-statistics-and-probability", "confidence_interval.png")


# --------------------------------------------------------------------------- #
# 04 · Machine Learning — bias/variance, ROC vs PR, confusion matrix
# --------------------------------------------------------------------------- #
def chart_ml():
    # Bias-variance: train error keeps dropping, val error is U-shaped.
    complexity = np.linspace(1, 10, 100)
    train_err = 0.9 / complexity + 0.02
    val_err = 0.9 / complexity + 0.02 + 0.012 * (complexity - 3) ** 2
    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.plot(complexity, train_err, color=GREEN, label="training error")
    ax.plot(complexity, val_err, color=RED, label="validation error")
    best = complexity[np.argmin(val_err)]
    ax.axvline(best, color="gray", ls="--", label="sweet spot")
    ax.annotate("underfit\n(high bias)", (1.5, 0.55), color=BLUE)
    ax.annotate("overfit\n(high variance)", (7.5, 0.55), color=BLUE)
    ax.set_xlabel("model complexity")
    ax.set_ylabel("error")
    ax.set_title("Bias–Variance Tradeoff")
    ax.legend(fontsize=8)
    save(fig, "04-machine-learning", "bias_variance.png")

    # ROC vs PR on imbalanced data.
    from sklearn.datasets import make_classification
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (precision_recall_curve, roc_curve,
                                  average_precision_score, roc_auc_score)
    from sklearn.model_selection import train_test_split
    X, y = make_classification(n_samples=4000, weights=[0.93, 0.07],
                               n_features=15, random_state=0)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.4, random_state=0)
    p = LogisticRegression(max_iter=1000).fit(Xtr, ytr).predict_proba(Xte)[:, 1]
    fpr, tpr, _ = roc_curve(yte, p)
    prec, rec, _ = precision_recall_curve(yte, p)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.6))
    a1.plot(fpr, tpr, color=BLUE, label=f"AUC={roc_auc_score(yte,p):.2f}")
    a1.plot([0, 1], [0, 1], "--", color="gray")
    a1.set_title("ROC curve (looks great)")
    a1.set_xlabel("false positive rate"); a1.set_ylabel("true positive rate")
    a1.legend()
    a2.plot(rec, prec, color=ORANGE, label=f"PR-AUC={average_precision_score(yte,p):.2f}")
    a2.axhline(yte.mean(), color="gray", ls="--", label=f"baseline={yte.mean():.2f}")
    a2.set_title("PR curve (honest on imbalance)")
    a2.set_xlabel("recall"); a2.set_ylabel("precision")
    a2.legend()
    fig.suptitle("On imbalanced data, PR-AUC tells the truth ROC-AUC hides", fontsize=11)
    save(fig, "04-machine-learning", "roc_vs_pr.png")

    # Confusion matrix.
    from sklearn.metrics import confusion_matrix
    cm = confusion_matrix(yte, (p > 0.5).astype(int))
    fig, ax = plt.subplots(figsize=(4.2, 3.6))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["Pred 0", "Pred 1"]); ax.set_yticklabels(["True 0", "True 1"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black", fontsize=13)
    ax.set_title("Confusion Matrix")
    fig.colorbar(im, fraction=0.046)
    ax.grid(False)
    save(fig, "04-machine-learning", "confusion_matrix.png")


# --------------------------------------------------------------------------- #
# 05 · Deep Learning — activation functions + gradient descent
# --------------------------------------------------------------------------- #
def chart_dl():
    x = np.linspace(-6, 6, 400)
    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.plot(x, 1 / (1 + np.exp(-x)), label="Sigmoid", color=BLUE)
    ax.plot(x, np.tanh(x), label="Tanh", color=GREEN)
    ax.plot(x, np.maximum(0, x), label="ReLU", color=RED)
    ax.set_title("Activation Functions")
    ax.set_xlabel("input"); ax.set_ylabel("output")
    ax.set_ylim(-1.5, 3)
    ax.legend()
    save(fig, "05-deep-learning", "activations.png")

    # Gradient descent on a bowl.
    f = lambda w: (w - 3) ** 2 + 1
    w, lr, hist = -4.0, 0.15, []
    for _ in range(12):
        hist.append(w)
        w -= lr * 2 * (w - 3)
    ws = np.linspace(-5, 11, 200)
    fig, ax = plt.subplots(figsize=(6, 3.4))
    ax.plot(ws, f(ws), color=BLUE)
    ax.plot(hist, [f(h) for h in hist], "o-", color=RED, label="gradient steps")
    ax.set_title("Gradient Descent (steps toward the minimum)")
    ax.set_xlabel("weight"); ax.set_ylabel("loss")
    ax.legend()
    save(fig, "05-deep-learning", "gradient_descent.png")


# --------------------------------------------------------------------------- #
# 06 · NLP — cosine similarity heatmap (TF-IDF)
# --------------------------------------------------------------------------- #
def chart_nlp():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    sents = ["reset my password", "forgot my login", "track my order",
             "where is my package"]
    v = TfidfVectorizer().fit_transform(sents)
    sim = cosine_similarity(v)
    fig, ax = plt.subplots(figsize=(4.8, 4))
    im = ax.imshow(sim, cmap="viridis", vmin=0, vmax=1)
    ax.set_xticks(range(len(sents))); ax.set_yticks(range(len(sents)))
    ax.set_xticklabels(sents, rotation=40, ha="right", fontsize=8)
    ax.set_yticklabels(sents, fontsize=8)
    for i in range(len(sents)):
        for j in range(len(sents)):
            ax.text(j, i, f"{sim[i,j]:.2f}", ha="center", va="center",
                    color="white" if sim[i, j] < 0.6 else "black", fontsize=8)
    ax.set_title("Semantic similarity (login vs order intents)")
    ax.grid(False)
    save(fig, "06-nlp", "similarity_heatmap.png")


# --------------------------------------------------------------------------- #
# 08 · Time Series — decomposition
# --------------------------------------------------------------------------- #
def chart_timeseries():
    n = 240
    t = np.arange(n)
    trend = 0.05 * t
    season = 3 * np.sin(2 * np.pi * t / 30)
    noise = RNG.normal(0, 0.7, n)
    obs = 10 + trend + season + noise
    fig, axes = plt.subplots(4, 1, figsize=(7, 6), sharex=True)
    for ax, data, title, c in zip(
        axes, [obs, 10 + trend, season, noise],
        ["Observed", "Trend", "Seasonality", "Residual (noise)"],
        [BLUE, RED, GREEN, "gray"]):
        ax.plot(t, data, color=c)
        ax.set_ylabel(title, fontsize=9)
    axes[-1].set_xlabel("time")
    fig.suptitle("Time Series Decomposition = Trend + Seasonality + Noise", fontsize=11)
    save(fig, "08-time-series", "decomposition.png")


# --------------------------------------------------------------------------- #
# 09 · MLOps — drift (PSI) over time
# --------------------------------------------------------------------------- #
def chart_mlops():
    weeks = np.arange(1, 17)
    psi = np.concatenate([RNG.uniform(0.02, 0.08, 8),
                          np.linspace(0.1, 0.4, 8) + RNG.uniform(0, 0.03, 8)])
    fig, ax = plt.subplots(figsize=(6.5, 3.4))
    ax.plot(weeks, psi, "o-", color=BLUE)
    ax.axhline(0.1, color=ORANGE, ls="--", label="0.10 moderate")
    ax.axhline(0.25, color=RED, ls="--", label="0.25 major → act")
    ax.fill_between(weeks, 0.25, psi, where=(psi > 0.25), color=RED, alpha=0.15)
    ax.set_title("Feature Drift Monitoring (PSI over time)")
    ax.set_xlabel("week"); ax.set_ylabel("PSI")
    ax.legend(fontsize=8)
    save(fig, "09-mlops", "drift_psi.png")


# --------------------------------------------------------------------------- #
# 11 · LLM — temperature reshapes the softmax distribution
# --------------------------------------------------------------------------- #
def chart_llm():
    logits = np.array([2.0, 1.0, 0.5, 0.2, -0.5, -1.0])
    tokens = ["the", "a", "cat", "dog", "sky", "run"]
    fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.2), sharey=True)
    for ax, T in zip(axes, [0.3, 1.0, 2.0]):
        p = np.exp(logits / T) / np.exp(logits / T).sum()
        ax.bar(tokens, p, color=BLUE)
        ax.set_title(f"temperature = {T}")
        ax.tick_params(axis="x", rotation=40)
    axes[0].set_ylabel("probability")
    fig.suptitle("Temperature: low = focused/deterministic, high = diverse/creative",
                 fontsize=11)
    save(fig, "11-llm", "temperature.png")


# --------------------------------------------------------------------------- #
# 12 · RAG — retrieval scores (relevant grounds, off-topic abstains)
# --------------------------------------------------------------------------- #
def chart_rag():
    docs = ["refund policy", "support hours", "password reset", "shipping"]
    relevant = [0.78, 0.12, 0.05, 0.20]
    fig, ax = plt.subplots(figsize=(6, 3.2))
    bars = ax.bar(docs, relevant, color=[GREEN if s > 0.3 else BLUE for s in relevant])
    ax.axhline(0.3, color=RED, ls="--", label="grounding threshold")
    ax.set_title("Query: 'How long do refunds take?' → retrieve top doc")
    ax.set_ylabel("similarity score")
    ax.tick_params(axis="x", rotation=20)
    ax.legend(fontsize=8)
    save(fig, "12-rag", "retrieval_scores.png")


# --------------------------------------------------------------------------- #
# 13 · Prompt Engineering — eval accuracy by technique
# --------------------------------------------------------------------------- #
def chart_prompt():
    techniques = ["zero-shot\n(vague)", "+ role &\nformat", "+ few-shot", "+ chain-\nof-thought"]
    acc = [0.55, 0.72, 0.86, 0.93]
    fig, ax = plt.subplots(figsize=(6, 3.2))
    bars = ax.bar(techniques, acc, color=BLUE)
    bars[-1].set_color(GREEN)
    ax.set_ylim(0, 1)
    ax.set_ylabel("eval accuracy")
    ax.set_title("Prompt techniques compound (measure on an eval set!)")
    for b, a in zip(bars, acc):
        ax.text(b.get_x() + b.get_width() / 2, a + 0.01, f"{a:.0%}", ha="center")
    save(fig, "13-prompt-engineering", "prompt_eval.png")


# --------------------------------------------------------------------------- #
# 16 · Data Visualization — pick the right chart
# --------------------------------------------------------------------------- #
def chart_viz():
    fig, axes = plt.subplots(2, 2, figsize=(8, 5.5))
    t = np.arange(12)
    axes[0, 0].plot(t, np.cumsum(RNG.normal(1, 1, 12)), color=BLUE, marker="o")
    axes[0, 0].set_title("Trend over time → LINE")
    cats = ["A", "B", "C", "D"]
    axes[0, 1].bar(cats, [23, 17, 35, 12], color=ORANGE)
    axes[0, 1].set_title("Comparison → BAR")
    axes[1, 0].hist(RNG.normal(0, 1, 1000), bins=30, color=GREEN)
    axes[1, 0].set_title("Distribution → HISTOGRAM")
    axes[1, 1].scatter(RNG.normal(0, 1, 200), RNG.normal(0, 1, 200), alpha=0.5, color=RED)
    axes[1, 1].set_title("Relationship → SCATTER")
    fig.suptitle("Match the chart to the question", fontsize=12)
    fig.tight_layout()
    save(fig, "16-data-visualization", "chart_chooser.png")


if __name__ == "__main__":
    print("Generating chart assets...")
    chart_python()
    chart_statistics()
    chart_ml()
    chart_dl()
    chart_nlp()
    chart_timeseries()
    chart_mlops()
    chart_llm()
    chart_rag()
    chart_prompt()
    chart_viz()
    print("Done.")
