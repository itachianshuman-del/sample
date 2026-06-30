"""
Lab 02 — Leak-Free Feature Engineering Pipelines
================================================
Module 3 | Curriculum Week 5

GOAL
----
Build a production-grade, fully reproducible preprocessing + model pipeline that:
  * handles mixed numeric / categorical / high-cardinality features,
  * does SAFE target encoding (out-of-fold) to avoid the leakage from lab01,
  * is tuned with a small random search (an Optuna stand-in with no extra deps),
  * evaluates with the metric and CV scheme that match the problem.

Run:  python lab02_feature_engineering_pipeline.py
Deps: numpy, pandas, scikit-learn
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RNG = np.random.default_rng(7)


def banner(t: str) -> None:
    print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)


# ---------------------------------------------------------------------------
# A safe, out-of-fold target encoder for high-cardinality categoricals.
# Naive target encoding (group mean over ALL rows) leaks the label. The fix:
# compute each row's encoding using only OTHER folds, with smoothing.
# ---------------------------------------------------------------------------
class OutOfFoldTargetEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, cols: list[str], n_splits: int = 5, smoothing: float = 10.0):
        self.cols = cols
        self.n_splits = n_splits
        self.smoothing = smoothing

    def fit(self, X: pd.DataFrame, y: np.ndarray):
        self.global_mean_ = float(np.mean(y))
        # Final maps (fit on ALL training data) used at transform/inference time.
        self.maps_ = {}
        for c in self.cols:
            stats = pd.DataFrame({c: X[c].values, "y": y}).groupby(c)["y"].agg(["mean", "count"])
            smooth = (stats["mean"] * stats["count"] + self.global_mean_ * self.smoothing) / (
                stats["count"] + self.smoothing
            )
            self.maps_[c] = smooth
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        # Used at inference: apply the learned map, fall back to global mean.
        out = X.copy()
        for c in self.cols:
            out[c] = out[c].map(self.maps_[c]).fillna(self.global_mean_)
        return out[self.cols]

    def fit_transform(self, X: pd.DataFrame, y: np.ndarray = None, **kw) -> pd.DataFrame:
        # During TRAINING, produce out-of-fold encodings to avoid leakage.
        self.fit(X, y)
        out = pd.DataFrame(index=X.index)
        skf = StratifiedKFold(self.n_splits, shuffle=True, random_state=0)
        for c in self.cols:
            oof = pd.Series(self.global_mean_, index=X.index, dtype=float)
            for tr, va in skf.split(X, y):
                stats = (
                    pd.DataFrame({c: X[c].values[tr], "y": y[tr]})
                    .groupby(c)["y"]
                    .agg(["mean", "count"])
                )
                smooth = (stats["mean"] * stats["count"] + self.global_mean_ * self.smoothing) / (
                    stats["count"] + self.smoothing
                )
                oof.iloc[va] = X[c].iloc[va].map(smooth).fillna(self.global_mean_).values
            out[c] = oof
        return out


def make_data(n: int = 6000) -> tuple[pd.DataFrame, np.ndarray]:
    """Imbalanced classification with numeric, low- and high-cardinality cats."""
    num1 = RNG.normal(size=n)
    num2 = RNG.exponential(size=n)
    low_card = RNG.choice(["A", "B", "C"], size=n)
    high_card = RNG.choice([f"id_{i}" for i in range(300)], size=n)  # high cardinality

    # True signal: depends on num1, a low-card level, and some high-card ids.
    hot_ids = {f"id_{i}" for i in range(0, 300, 25)}
    logit = (
        1.5 * num1
        - 0.8 * (low_card == "A")
        + 1.2 * np.array([h in hot_ids for h in high_card])
        - 2.0  # base rate -> imbalanced
    )
    p = 1 / (1 + np.exp(-logit))
    y = (RNG.random(n) < p).astype(int)
    df = pd.DataFrame({"num1": num1, "num2": num2, "low_card": low_card, "high_card": high_card})
    return df, y


def build_pipeline(hgb_kwargs: dict) -> Pipeline:
    numeric = ["num1", "num2"]
    low_card = ["low_card"]
    high_card = ["high_card"]

    pre = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric),
            ("low", OneHotEncoder(handle_unknown="ignore"), low_card),
            ("high", OutOfFoldTargetEncoder(cols=high_card), high_card),
        ]
    )
    return Pipeline([("pre", pre), ("clf", HistGradientBoostingClassifier(**hgb_kwargs))])


def main() -> None:
    banner("BUILD: leak-free pipeline on imbalanced data")
    X, y = make_data()
    print(f"n={len(y)}, positive rate={y.mean():.3f} (imbalanced)")
    print("Because positives are rare, we judge with PR-AUC (average precision),")
    print("not plain accuracy and not only ROC-AUC.\n")

    # Small random search -- a dependency-free stand-in for Optuna.
    # In real work use Optuna (see RESOURCES section 3) for smarter search.
    banner("TUNE: random search over HistGradientBoosting hyperparameters")
    search_space = {
        "learning_rate": [0.03, 0.05, 0.1, 0.2],
        "max_depth": [None, 3, 5, 8],
        "max_iter": [200, 400],
        "l2_regularization": [0.0, 1.0, 5.0],
    }
    skf = StratifiedKFold(5, shuffle=True, random_state=1)

    best_score, best_cfg = -1.0, None
    for _ in range(12):  # 12 random trials
        cfg = {k: RNG.choice(v) for k, v in search_space.items()}
        cfg = {k: (None if v is None else (int(v) if k in {"max_depth", "max_iter"} else float(v)))
               for k, v in cfg.items()}
        pipe = build_pipeline(cfg)
        # cross_val_predict gives out-of-fold probabilities -> honest PR-AUC.
        proba = cross_val_predict(pipe, X, y, cv=skf, method="predict_proba")[:, 1]
        score = average_precision_score(y, proba)
        if score > best_score:
            best_score, best_cfg = score, cfg
            print(f"  new best PR-AUC={score:.4f}  cfg={cfg}")

    banner("RESULT")
    final = build_pipeline(best_cfg)
    proba = cross_val_predict(final, X, y, cv=skf, method="predict_proba")[:, 1]
    print(f"Best config     : {best_cfg}")
    print(f"PR-AUC (OOF)    : {average_precision_score(y, proba):.4f}")
    print(f"ROC-AUC (OOF)   : {roc_auc_score(y, proba):.4f}")
    print(f"Positive rate   : {y.mean():.4f}  (PR-AUC baseline = positive rate)")
    print("\nThe whole pipeline -- scaling, encoding, target-encoding -- is re-fit")
    print("inside each fold, so these numbers are leakage-free and trustworthy.")

    banner("EXTEND THIS")
    print(
        """
1. Replace the random search with Optuna (`pip install optuna`) using a TPE
   sampler and `study.optimize`. Compare the number of trials needed.
2. Add SHAP (`pip install shap`) on the final fitted model and identify the top
   drivers. Do they match the true signal we injected (num1, low_card=='A',
   the 'hot' ids)?
3. Swap OutOfFoldTargetEncoder for a naive group-mean encoder fit on all data.
   Watch PR-AUC jump unrealistically -- you've re-created lab01's leakage.
4. Pick a deployment threshold from a cost model (e.g., FN costs 5x a FP) instead
   of 0.5, and report precision/recall at that operating point.
"""
    )


if __name__ == "__main__":
    main()
