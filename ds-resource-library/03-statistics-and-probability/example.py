"""
Example — Statistics & Probability
===================================
Runnable. Deps: numpy, scipy

Three things every data scientist uses constantly:
  1. Bootstrap confidence interval (no formula needed)
  2. Two-sample hypothesis test (is B different from A?)
  3. A simulation to build probability intuition

Run: python example.py
"""

from __future__ import annotations

import numpy as np
from scipy import stats

rng = np.random.default_rng(42)


def bootstrap_ci() -> None:
    print("=" * 60, "\n1) Bootstrap 95% CI for the mean of skewed data\n", "=" * 60)
    sample = rng.exponential(scale=5.0, size=200)          # right-skewed
    boot_means = np.array([
        rng.choice(sample, size=len(sample), replace=True).mean()
        for _ in range(10_000)
    ])
    lo, hi = np.percentile(boot_means, [2.5, 97.5])
    print(f"sample mean = {sample.mean():.2f}")
    print(f"95% bootstrap CI = [{lo:.2f}, {hi:.2f}]")


def hypothesis_test() -> None:
    print("\n" + "=" * 60, "\n2) Two-sample t-test\n", "=" * 60)
    a = rng.normal(100, 15, 500)        # control
    b = rng.normal(104, 15, 500)        # treatment (true +4 effect)
    t, p = stats.ttest_ind(b, a)
    effect = b.mean() - a.mean()
    print(f"observed effect = {effect:+.2f}")
    print(f"t = {t:.2f}, p = {p:.4f}  -> "
          f"{'REJECT null (significant)' if p < 0.05 else 'fail to reject'}")


def probability_simulation() -> None:
    print("\n" + "=" * 60, "\n3) Simulation: P(>=8 heads in 10 fair flips)\n", "=" * 60)
    flips = rng.binomial(n=10, p=0.5, size=1_000_000)
    sim = (flips >= 8).mean()
    exact = sum(stats.binom.pmf(k, 10, 0.5) for k in (8, 9, 10))
    print(f"simulated = {sim:.4f}   exact = {exact:.4f}")


if __name__ == "__main__":
    bootstrap_ci()
    hypothesis_test()
    probability_simulation()
    print("\nExtend: simulate an A/A test and show how 'peeking' inflates false positives.")
