"""
Example — Machine Learning (leak-free pipeline, right metric)
=============================================================
Runnable. Deps: numpy, scikit-learn

A correct ML baseline on imbalanced data:
  * everything inside a Pipeline  -> no leakage
  * StratifiedKFold               -> CV matches deployment
  * PR-AUC (average precision)    -> the right metric for rare positives
  * a dumb baseline first         -> always know what 'good' means

Run: python example.py
"""

from __future__ import annotations

import numpy as np
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(
    n_samples=5000, n_features=20, n_informative=6,
    weights=[0.9, 0.1], random_state=0,        # 10% positives (imbalanced)
)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

# Baseline: predict the prior. PR-AUC baseline == positive rate.
baseline = DummyClassifier(strategy="stratified")
base = cross_val_score(baseline, X, y, cv=cv, scoring="average_precision").mean()

# Real model: scaler + gradient boosting, all inside one Pipeline.
pipe = Pipeline([
    ("scale", StandardScaler()),
    ("clf", HistGradientBoostingClassifier(learning_rate=0.05, max_iter=300)),
])
pr_auc = cross_val_score(pipe, X, y, cv=cv, scoring="average_precision").mean()
roc_auc = cross_val_score(pipe, X, y, cv=cv, scoring="roc_auc").mean()

print("=" * 60)
print(f"positive rate (PR-AUC baseline) : {y.mean():.3f}")
print(f"DummyClassifier PR-AUC          : {base:.3f}")
print(f"Gradient Boosting  PR-AUC       : {pr_auc:.3f}   <- the one to report")
print(f"Gradient Boosting  ROC-AUC      : {roc_auc:.3f}   (optimistic on imbalance)")
print("=" * 60)
print("Lesson: on imbalanced data, judge with PR-AUC vs the positive-rate baseline,")
print("not accuracy/ROC-AUC. Keep all transforms inside the Pipeline to avoid leakage.")
