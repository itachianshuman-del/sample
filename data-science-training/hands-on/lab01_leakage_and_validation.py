"""
Lab 01 — Data Leakage & Validation That Matches Reality
=======================================================
Module 3 | Curriculum Week 4

GOAL
----
Feel, in your bones, how data leakage produces beautiful offline metrics and
useless models -- and how the right validation scheme prevents it.

We demonstrate three classic leakage modes and their fixes:
  A. Preprocessing leakage   (fitting a scaler/selector on ALL data before split)
  B. Temporal leakage        (random split on time-ordered data)
  C. Group leakage           (same entity in train and test)

Run:  python lab01_leakage_and_validation.py
Deps: numpy, pandas, scikit-learn
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    GroupKFold,
    StratifiedKFold,
    TimeSeriesSplit,
    cross_val_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RNG = np.random.default_rng(42)


def banner(title: str) -> None:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------------------
# A. PREPROCESSING LEAKAGE
# ---------------------------------------------------------------------------
def demo_preprocessing_leakage() -> None:
    banner("A. PREPROCESSING LEAKAGE — feature selection before the split")

    # Pure noise: there is NO real signal. A correct pipeline should score ~0.5.
    n, p = 200, 10_000
    X = RNG.normal(size=(n, p))
    y = RNG.integers(0, 2, size=n)

    # ---- WRONG: select features using the WHOLE dataset, THEN split ----
    # SelectKBest peeks at y for all rows, including the future test rows.
    X_sel = SelectKBest(f_classif, k=20).fit_transform(X, y)
    Xtr, Xte, ytr, yte = train_test_split(X_sel, y, test_size=0.5, random_state=0)
    leaky = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
    leaky_acc = leaky.score(Xte, yte)

    # ---- RIGHT: put selection INSIDE a pipeline, evaluate with CV ----
    # Selection is re-fit on each training fold only -- no peeking.
    pipe = Pipeline(
        [
            ("select", SelectKBest(f_classif, k=20)),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    honest_acc = cross_val_score(pipe, X, y, cv=5).mean()

    print(f"Data is PURE NOISE -> honest accuracy should be ~0.50")
    print(f"  Leaky 'accuracy'  : {leaky_acc:.3f}   <- looks great, is a lie")
    print(f"  Honest CV accuracy: {honest_acc:.3f}   <- the truth")
    print("Lesson: ANY step that touches y (selection, target-encoding, scaling")
    print("on full data) must live INSIDE the CV loop / pipeline.")


# ---------------------------------------------------------------------------
# B. TEMPORAL LEAKAGE
# ---------------------------------------------------------------------------
def demo_temporal_leakage() -> None:
    banner("B. TEMPORAL LEAKAGE — random split on time-series data")

    # A drifting time series: the relationship changes over time.
    t = np.arange(1000)
    trend = t / 1000.0
    X = RNG.normal(size=(1000, 5))
    # Signal strength drifts with time -> future differs from past.
    y = ((X[:, 0] * (1 - trend) + X[:, 1] * trend + RNG.normal(scale=0.3, size=1000)) > 0).astype(int)
    df = pd.DataFrame(X).assign(t=t, y=y).sort_values("t")

    model = LogisticRegression(max_iter=1000)

    # ---- WRONG: random split mixes future into training ----
    Xtr, Xte, ytr, yte = train_test_split(df[[0, 1, 2, 3, 4]], df["y"], random_state=0)
    random_acc = model.fit(Xtr, ytr).score(Xte, yte)

    # ---- RIGHT: forward-chaining split (train on past, test on future) ----
    tscv = TimeSeriesSplit(n_splits=5)
    fwd_acc = cross_val_score(model, df[[0, 1, 2, 3, 4]], df["y"], cv=tscv).mean()

    print(f"  Random-split accuracy     : {random_acc:.3f}  <- optimistic")
    print(f"  TimeSeriesSplit accuracy  : {fwd_acc:.3f}  <- what you'll actually get")
    print("Lesson: if predictions are made about the FUTURE, validate on the")
    print("future. Never shuffle time. Use TimeSeriesSplit / forward chaining.")


# ---------------------------------------------------------------------------
# C. GROUP LEAKAGE
# ---------------------------------------------------------------------------
def demo_group_leakage() -> None:
    banner("C. GROUP LEAKAGE — same entity in train and test")

    # 60 users, ~20 rows each. Each user has a RANDOM label (a per-user trait that
    # does NOT generalize from features). We include the user id as a feature -- a
    # very common real mistake. A model can then memorize "user 37 -> label 1".
    #  * Random KFold: the same user is in train & test, so memorizing WINS.
    #  * GroupKFold:  test users are unseen, their id columns are all-zero, so the
    #                 memorized mapping is useless -> the honest ~chance score.
    n_users = 60
    rows = []
    for u in range(n_users):
        user_label = int(RNG.random() > 0.5)          # arbitrary per-user label
        for _ in range(20):
            x_noise = RNG.normal(size=2)              # no real signal
            y_row = user_label if RNG.random() > 0.05 else 1 - user_label
            rows.append((u, *x_noise, y_row))
    df = pd.DataFrame(rows, columns=["user", "x1", "x2", "y"])

    # One-hot the user id (the leaky feature) alongside the noise features.
    X = pd.concat([df[["x1", "x2"]], pd.get_dummies(df["user"], prefix="u")], axis=1)
    y, groups = df["y"], df["user"]

    model = LogisticRegression(max_iter=5000, C=1e4)  # little regularization -> can memorize

    # ---- WRONG: shuffled KFold spreads each user across folds -> leak ----
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
    random_acc = cross_val_score(model, X, y, cv=skf).mean()

    # ---- RIGHT: GroupKFold keeps each user entirely in one fold ----
    gkf = GroupKFold(n_splits=5)
    grouped_acc = cross_val_score(model, X, y, cv=gkf, groups=groups).mean()

    print(f"  Random KFold accuracy : {random_acc:.3f}  <- memorizes users (leak)")
    print(f"  GroupKFold accuracy   : {grouped_acc:.3f}  <- truth on NEW users (~chance)")
    print("Lesson: if you must generalize to unseen entities (users, patients,")
    print("devices), keep each entity in ONE fold with GroupKFold -- and never")
    print("feed raw entity ids as features unless you truly will see them again.")


def main() -> None:
    demo_preprocessing_leakage()
    demo_temporal_leakage()
    demo_group_leakage()

    banner("EXTEND THIS")
    print(
        """
1. In demo A, move SelectKBest OUTSIDE the pipeline but AFTER the split (fit on
   train only). Does the leak disappear? Why does the pipeline make this safe by
   default?
2. In demo B, add a feature that is a future-aggregated value (e.g., rolling mean
   computed over the whole series). Show how it leaks even with TimeSeriesSplit.
3. In demo C, add a per-user mean-target feature computed over all rows. Watch
   the GroupKFold score collapse -- you've re-introduced leakage. Fix it with
   out-of-fold target encoding (see lab02).
4. Write a checklist function `assert_no_obvious_leakage(df, target, time_col,
   group_col)` that warns about the patterns above.
"""
    )


if __name__ == "__main__":
    main()
