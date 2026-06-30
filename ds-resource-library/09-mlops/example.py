"""
Example — MLOps: minimal experiment tracking + model registry (from scratch)
============================================================================
Runnable. Deps: numpy, scikit-learn  (no MLflow needed to learn the concept)

Experiment tracking answers "what did we try and how did it do?" and a registry
answers "which model is in production and how was it trained?". Here we implement
a tiny version with the stdlib so the IDEA is crystal clear; in production use
MLflow / Weights & Biases.

Run: python example.py   ->   writes mlruns.jsonl + best_model.pkl
"""

from __future__ import annotations

import hashlib
import json
import pickle
import time
from pathlib import Path

from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=2000, n_features=20, random_state=0)
RUNS = Path("mlruns.jsonl")


def log_run(params: dict, metric: float, model) -> str:
    """Persist a run's params + metric + a content hash of the model artifact."""
    blob = pickle.dumps(model)
    run_id = hashlib.sha1(blob).hexdigest()[:10]      # reproducible artifact id
    record = {"run_id": run_id, "ts": time.time(), "params": params,
              "cv_auc": round(metric, 4)}
    with RUNS.open("a") as f:
        f.write(json.dumps(record) + "\n")
    return run_id


def experiment() -> None:
    RUNS.unlink(missing_ok=True)
    grid = [
        {"n_estimators": 100, "max_depth": 4},
        {"n_estimators": 300, "max_depth": 6},
        {"n_estimators": 500, "max_depth": None},
    ]
    for params in grid:
        model = RandomForestClassifier(**params, random_state=0).fit(X, y)
        auc = cross_val_score(model, X, y, scoring="roc_auc", cv=5).mean()
        run_id = log_run(params, auc, model)
        print(f"  logged run {run_id}: params={params} -> cv_auc={auc:.4f}")


def promote_best() -> None:
    runs = [json.loads(line) for line in RUNS.read_text().splitlines()]
    best = max(runs, key=lambda r: r["cv_auc"])      # the "model registry" choice
    # Re-fit and 'register' (save) the production model.
    model = RandomForestClassifier(**best["params"], random_state=0).fit(X, y)
    Path("best_model.pkl").write_bytes(pickle.dumps(model))
    print("=" * 60)
    print(f"PROMOTED to production: run {best['run_id']} "
          f"(cv_auc={best['cv_auc']}) -> best_model.pkl")


if __name__ == "__main__":
    print("=" * 60, "\nTracking experiments\n", "=" * 60)
    experiment()
    promote_best()
    print("\nLesson: every run is reproducible (params + metric + artifact hash),")
    print("and promotion picks the best by your metric. MLflow does exactly this,")
    print("plus a UI, a real registry, and stage transitions (staging/production).")
