"""
Lab 03 — A/B Test: Power Analysis + Full Analysis
=================================================
Module 2 | Curriculum Weeks 2-3

GOAL
----
Do an experiment the way a senior DS does:
  PART 1  Power & sample size BEFORE launch (don't run underpowered tests).
  PART 2  Analyze a simulated experiment: effect size, CI, p-value, and a
          guardrail check -- ending in a ship / no-ship recommendation.
  PART 3  See WHY peeking inflates false positives (the most common mistake).

Run:  python lab03_ab_test_analysis.py
Deps: numpy, scipy   (statsmodels optional; we implement the math directly)
"""

from __future__ import annotations

import numpy as np
from scipy import stats

RNG = np.random.default_rng(2024)


def banner(t: str) -> None:
    print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)


# ---------------------------------------------------------------------------
# PART 1 — Power analysis for a two-proportion test
# ---------------------------------------------------------------------------
def required_sample_size(p_baseline: float, mde_abs: float, alpha=0.05, power=0.8) -> int:
    """Per-arm sample size to detect an absolute lift `mde_abs` on a proportion.

    MDE = Minimum Detectable Effect. Larger effect -> fewer samples needed.
    """
    p1, p2 = p_baseline, p_baseline + mde_abs
    z_alpha = stats.norm.ppf(1 - alpha / 2)  # two-sided
    z_power = stats.norm.ppf(power)
    pbar = (p1 + p2) / 2
    # Standard two-proportion sample size formula.
    n = ((z_alpha * np.sqrt(2 * pbar * (1 - pbar)) + z_power * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / (
        mde_abs**2
    )
    return int(np.ceil(n))


def demo_power() -> None:
    banner("PART 1 — POWER: how many users do we need?")
    baseline = 0.10  # 10% baseline conversion
    print(f"Baseline conversion = {baseline:.0%}, alpha=0.05, power=0.80\n")
    print(f"{'Relative lift':>14} | {'Absolute MDE':>12} | {'Per-arm n':>12}")
    print("-" * 44)
    for rel in (0.02, 0.05, 0.10, 0.20):
        mde = baseline * rel
        n = required_sample_size(baseline, mde)
        print(f"{rel:>13.0%} | {mde:>12.4f} | {n:>12,}")
    print("\nLesson: detecting a tiny lift (2%) needs ENORMOUS samples. Decide the")
    print("MDE worth caring about BEFORE you launch, then commit to that sample.")


# ---------------------------------------------------------------------------
# PART 2 — Analyze a (simulated) experiment
# ---------------------------------------------------------------------------
def two_proportion_test(c_conv, c_n, t_conv, t_n):
    p_c, p_t = c_conv / c_n, t_conv / t_n
    diff = p_t - p_c
    # Pooled SE for the hypothesis test.
    p_pool = (c_conv + t_conv) / (c_n + t_n)
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / c_n + 1 / t_n))
    z = diff / se_pool
    pval = 2 * (1 - stats.norm.cdf(abs(z)))
    # Unpooled SE for the confidence interval on the difference.
    se_diff = np.sqrt(p_c * (1 - p_c) / c_n + p_t * (1 - p_t) / t_n)
    ci = (diff - 1.96 * se_diff, diff + 1.96 * se_diff)
    return p_c, p_t, diff, pval, ci


def demo_analysis() -> None:
    banner("PART 2 — ANALYZE: control vs treatment, with a guardrail")
    n_per_arm = required_sample_size(0.10, 0.10 * 0.05)  # power to detect +5% rel

    # Simulate a TRUE +0.7pp effect (above our MDE) so the test is well-powered.
    true_c, true_t = 0.100, 0.107
    c_conv = RNG.binomial(n_per_arm, true_c)
    t_conv = RNG.binomial(n_per_arm, true_t)

    p_c, p_t, diff, pval, ci = two_proportion_test(c_conv, n_per_arm, t_conv, n_per_arm)
    rel = diff / p_c

    print(f"Per-arm sample size : {n_per_arm:,}")
    print(f"Control conversion  : {p_c:.4f}")
    print(f"Treatment conversion: {p_t:.4f}")
    print(f"Absolute lift       : {diff:+.4f}  ({rel:+.1%} relative)")
    print(f"95% CI on lift      : [{ci[0]:+.4f}, {ci[1]:+.4f}]")
    print(f"p-value             : {pval:.4f}")

    # Guardrail metric: latency must NOT regress. Simulate a small regression.
    lat_c = RNG.normal(200, 40, n_per_arm)      # ms
    lat_t = RNG.normal(206, 40, n_per_arm)      # +6ms
    t_stat, lat_p = stats.ttest_ind(lat_t, lat_c)
    lat_diff = lat_t.mean() - lat_c.mean()
    print(f"\nGuardrail (latency) : {lat_diff:+.1f} ms  (p={lat_p:.3f})")

    banner("DECISION")
    sig = pval < 0.05 and ci[0] > 0
    guardrail_ok = lat_p >= 0.05 or lat_diff < 10  # tolerate <10ms
    print(f"Primary metric significant & positive? {sig}")
    print(f"Guardrail acceptable?                  {guardrail_ok}")
    if sig and guardrail_ok:
        print("-> SHIP. Lift is significant, CI excludes zero, guardrail acceptable.")
    elif sig and not guardrail_ok:
        print("-> HOLD. Conversion improved but a guardrail regressed -- investigate.")
    else:
        print("-> NO SHIP / INCONCLUSIVE. Don't ship on a non-significant result.")
    print("\nNote: report the CI, not just the p-value. 'Significant' without an")
    print("effect size and guardrails is not a decision.")


# ---------------------------------------------------------------------------
# PART 3 — Why peeking inflates false positives
# ---------------------------------------------------------------------------
def demo_peeking(n_experiments=2000, n_users=4000, checks=20) -> None:
    banner("PART 3 — PEEKING: the silent false-positive machine")
    # A/A test: treatment == control. ANY 'significant' result is a false positive.
    false_pos_fixed = 0
    false_pos_peek = 0
    check_points = np.linspace(n_users // checks, n_users, checks).astype(int)

    for _ in range(n_experiments):
        a = RNG.random(n_users) < 0.10
        b = RNG.random(n_users) < 0.10  # same true rate -> null is TRUE

        # Fixed-horizon: test once at the end.
        _, _, _, p_end, _ = two_proportion_test(a.sum(), n_users, b.sum(), n_users)
        false_pos_fixed += p_end < 0.05

        # Peeking: stop the first time it looks significant.
        for cp in check_points:
            _, _, _, p, _ = two_proportion_test(a[:cp].sum(), cp, b[:cp].sum(), cp)
            if p < 0.05:
                false_pos_peek += 1
                break

    print(f"True effect = ZERO (A/A test). Target false-positive rate = 5%.")
    print(f"  Test once at the end : {false_pos_fixed / n_experiments:.1%}  (~as expected)")
    print(f"  Peek {checks}x and stop early: {false_pos_peek / n_experiments:.1%}  (INFLATED!)")
    print("\nLesson: repeatedly checking and stopping when p<0.05 wildly inflates")
    print("false positives. Fix: pre-commit a sample size, or use sequential /")
    print("always-valid testing (see Module 2, section 6).")


def main() -> None:
    demo_power()
    demo_analysis()
    demo_peeking()

    banner("EXTEND THIS")
    print(
        """
1. Implement CUPED: use a pre-experiment covariate correlated with the outcome to
   reduce variance, and show the required sample size drops for the same power.
2. Replace the z-test with a bootstrap CI on the difference in conversion. Do the
   conclusions match?
3. Add a second guardrail (e.g., revenue per user) and apply a multiple-comparison
   correction (Benjamini-Hochberg) across your metrics.
4. Implement an always-valid p-value (mSPRT) and re-run PART 3 -- show peeking no
   longer inflates the error rate.
"""
    )


if __name__ == "__main__":
    main()
