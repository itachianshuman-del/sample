# 03 · Statistics & Probability

> The foundation that turns "the number went up" into "we're 95% confident this
> change caused a real improvement." The most reliable differentiator in DS.

---

## 📌 What it is & why it matters

Statistics is how you reason under uncertainty — the core of experimentation,
inference, and trustworthy decision-making. Probability is its language. Nearly
every business decision a data scientist supports (ship this feature? is this
effect real?) rests on statistics, not modeling. It's also the topic most
mid-level data scientists are weakest on.

---

## 🧠 Core concepts

- **Descriptive stats:** mean/median/mode, variance/std, percentiles, skew.
- **Probability:** random variables, conditional probability, Bayes' theorem,
  common distributions (normal, binomial, Poisson, exponential).
- **Sampling & CLT:** sampling distribution, standard error (`~1/√n`), the
  Central Limit Theorem and where it fails.
- **Estimation:** confidence intervals, the **bootstrap** (your go-to when
  formulas are hard).
- **Hypothesis testing:** null/alternative, p-values (and what they are *not*),
  Type I/II errors, **power**, t-tests, chi-square, ANOVA.
- **The traps:** p-hacking, multiple comparisons, peeking, confusing statistical
  vs practical significance.
- **Bayesian thinking:** priors, posteriors, credible intervals.

> Deep dive + labs in
> [`data-science-training/modules/02-statistics-and-experimentation.md`](../../data-science-training/modules/02-statistics-and-experimentation.md)
> and `hands-on/lab03_ab_test_analysis.py`.

---

## 📚 Best resources

### Videos (best for intuition)
- **StatQuest with Josh Starmer** — the gold standard for intuitive stats/ML
  explanations: https://www.youtube.com/@statquest
- **3Blue1Brown — Probability & "Essence" series** — beautiful visual intuition:
  https://www.youtube.com/@3blue1brown
- **Krish Naik — Statistics for Data Science** playlist (free, practical).

### Books (free)
- **Think Stats / Think Bayes** — Allen Downey (Python-based): https://greenteapress.com/wp/
- **Statistical Rethinking** — Richard McElreath (Bayesian; lectures + code):
  https://github.com/rmcelreath/stat_rethinking_2024
- **Seeing Theory** — visual intro to probability & stats: https://seeing-theory.brown.edu/

### Courses
- **Khan Academy — Statistics & Probability** (free, foundational).

---

## 💻 Code example

```python
import numpy as np
from scipy import stats

# --- Bootstrap confidence interval (works when no neat formula exists) ---
rng = np.random.default_rng(0)
sample = rng.exponential(scale=5.0, size=200)   # skewed data

boot_means = [rng.choice(sample, size=len(sample), replace=True).mean()
              for _ in range(10_000)]
ci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])
print(f"Mean={sample.mean():.2f}, 95% bootstrap CI=[{ci_low:.2f}, {ci_high:.2f}]")

# --- Two-sample t-test: is group B different from group A? ---
a = rng.normal(100, 15, 500)
b = rng.normal(104, 15, 500)
t, p = stats.ttest_ind(b, a)
print(f"t={t:.2f}, p={p:.4f} -> {'significant' if p < 0.05 else 'not significant'}")
```

---

## 🌍 Real-world use cases

- **A/B testing** — deciding whether a product change actually worked.
- **Anomaly detection** — flagging values outside expected distributions.
- **Risk & forecasting** — quantifying uncertainty in predictions.
- **Quality control** — detecting drift / process shifts.

---

## 🛠️ Hands-on project ideas

1. Simulate an **A/A test** and show how "peeking" inflates false positives.
2. Implement a **bootstrap** from scratch and compare its CI to the formula-based one.
3. Build a small **Bayesian A/B test** (Beta-Binomial) and report P(B > A).

---

## 🗺️ Suggested learning path

1. Descriptive stats & probability basics → 2. Distributions → 3. Sampling & CLT
→ 4. Confidence intervals & bootstrap → 5. Hypothesis testing + the traps →
6. Experimentation (Module 02) → 7. Bayesian basics.
