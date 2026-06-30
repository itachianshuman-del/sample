"""
Lab 04 — Model Monitoring & Drift Detection
============================================
Module 5 | Curriculum Weeks 10-11

GOAL
----
Labels in production are usually delayed, so you must detect trouble from the
INPUTS and PREDICTIONS before accuracy data arrives. We implement, from scratch:
  * PSI (Population Stability Index) -- the industry-standard drift metric,
  * a KS-test drift check for numeric features,
  * prediction-distribution drift,
and simulate three regimes: stable, covariate shift, and concept drift.

In real life, use a library like Evidently (see RESOURCES section 5). Here we
build the math so the library is never a black box.

Run:  python lab04_model_monitoring.py
Deps: numpy, scipy, scikit-learn
"""

from __future__ import annotations

import numpy as np
from scipy import stats
from sklearn.linear_model import LogisticRegression

RNG = np.random.default_rng(11)


def banner(t: str) -> None:
    print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)


# ---------------------------------------------------------------------------
# Population Stability Index: how much a distribution has shifted vs a baseline.
#   PSI < 0.1  : no significant shift
#   0.1-0.25   : moderate shift -- investigate
#   > 0.25     : major shift -- likely action needed
# ---------------------------------------------------------------------------
def psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    # Bin edges from the BASELINE (expected) distribution's quantiles.
    quantiles = np.linspace(0, 1, bins + 1)
    edges = np.quantile(expected, quantiles)
    edges[0], edges[-1] = -np.inf, np.inf
    e_perc = np.histogram(expected, edges)[0] / len(expected)
    a_perc = np.histogram(actual, edges)[0] / len(actual)
    # Avoid div-by-zero / log(0).
    eps = 1e-6
    e_perc = np.clip(e_perc, eps, None)
    a_perc = np.clip(a_perc, eps, None)
    return float(np.sum((a_perc - e_perc) * np.log(a_perc / e_perc)))


def interpret_psi(value: float) -> str:
    if value < 0.1:
        return "stable"
    if value < 0.25:
        return "MODERATE shift -- investigate"
    return "MAJOR shift -- action likely needed"


def main() -> None:
    banner("SETUP — train a model on 'reference' (training-time) data")
    n = 5000
    # Reference distribution.
    X_ref = RNG.normal(0, 1, size=(n, 2))
    y_ref = ((1.5 * X_ref[:, 0] - X_ref[:, 1] + RNG.normal(scale=0.5, size=n)) > 0).astype(int)
    model = LogisticRegression().fit(X_ref, y_ref)
    ref_pred = model.predict_proba(X_ref)[:, 1]
    print(f"Trained on {n} reference samples. Now we watch 3 production regimes.\n")

    # -- Regime 1: STABLE (production looks like training) --
    X1 = RNG.normal(0, 1, size=(n, 2))
    y1 = ((1.5 * X1[:, 0] - X1[:, 1] + RNG.normal(scale=0.5, size=n)) > 0).astype(int)

    # -- Regime 2: COVARIATE SHIFT (inputs move, X->y rule unchanged) --
    X2 = RNG.normal(1.0, 1.3, size=(n, 2))  # mean & variance shifted
    y2 = ((1.5 * X2[:, 0] - X2[:, 1] + RNG.normal(scale=0.5, size=n)) > 0).astype(int)

    # -- Regime 3: CONCEPT DRIFT (inputs same, X->y rule changes) --
    X3 = RNG.normal(0, 1, size=(n, 2))
    y3 = ((-1.0 * X3[:, 0] + 1.5 * X3[:, 1] + RNG.normal(scale=0.5, size=n)) > 0).astype(int)  # flipped!

    regimes = {
        "1. STABLE": (X1, y1),
        "2. COVARIATE SHIFT": (X2, y2),
        "3. CONCEPT DRIFT": (X3, y3),
    }

    for name, (X, y) in regimes.items():
        banner(f"REGIME {name}")
        preds = model.predict_proba(X)[:, 1]
        acc = model.score(X, y)

        # Feature drift (PSI + KS) -- available WITHOUT labels.
        for j in range(X.shape[1]):
            p = psi(X_ref[:, j], X[:, j])
            ks_stat, ks_p = stats.ks_2samp(X_ref[:, j], X[:, j])
            print(f"  feature x{j}: PSI={p:.3f} ({interpret_psi(p)}) | KS p={ks_p:.1e}")

        # Prediction drift -- also available WITHOUT labels.
        pred_psi = psi(ref_pred, preds)
        print(f"  prediction-score PSI: {pred_psi:.3f} ({interpret_psi(pred_psi)})")

        # Actual accuracy -- only once labels arrive (often delayed!).
        print(f"  [delayed] actual accuracy: {acc:.3f}")

        # The senior interpretation:
        if name.startswith("1"):
            print("  -> All green. No action.")
        elif name.startswith("2"):
            print("  -> Feature + prediction drift fire. Inputs moved. Accuracy may")
            print("     hold, but investigate data pipeline / population change.")
        else:
            print("  -> THE DANGEROUS ONE: features look STABLE (low PSI) yet accuracy")
            print("     collapsed. Concept drift is invisible to input monitoring --")
            print("     you only catch it via labels or business-KPI proxies.")

    banner("KEY TAKEAWAYS")
    print(
        """
* Covariate shift  -> visible in feature/prediction drift (no labels needed).
* Concept drift    -> often INVISIBLE in inputs; needs labels or KPI proxies.
* Monitor 3 layers: operational (latency/errors), data quality (schema/nulls),
  model quality (drift now, accuracy when labels arrive).
* Set thresholds & alerts (e.g., PSI>0.25) and tie them to a retraining decision.
"""
    )

    banner("EXTEND THIS")
    print(
        """
1. Re-implement these checks with Evidently (`pip install evidently`) and compare
   its drift report to your hand-rolled PSI/KS.
2. Add a 'data quality' monitor: detect a feature that suddenly becomes 30% null
   or goes out of its training range.
3. Build a delayed-label simulator: labels arrive 14 'days' late. Track a rolling
   accuracy and trigger a retrain alert when it drops below a threshold.
4. Add a guardrail that distinguishes 'real drift' from random noise using a
   bootstrap confidence band on PSI.
"""
    )


if __name__ == "__main__":
    main()
