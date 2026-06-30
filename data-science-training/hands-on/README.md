# Hands-On Labs

Runnable, self-contained Python labs. Each one teaches a concept by *doing*,
prints explanatory output, and ends with **"Extend this"** challenges. They use
synthetic data so they run anywhere with no downloads.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install numpy pandas scikit-learn scipy statsmodels matplotlib \
            xgboost lightgbm shap mlflow evidently sentence-transformers
```

Most labs only need `numpy pandas scikit-learn scipy`. Heavier deps are noted per
lab. The RAG lab (`lab05`) works with a pure-numpy fallback if
`sentence-transformers` isn't installed.

## The labs (map to modules & curriculum weeks)

| Lab | Topic | Module | Week | Core deps |
|---|---|---|---|---|
| `lab01_leakage_and_validation.py` | Data leakage & CV that matches reality | 3 | 4 | sklearn |
| `lab02_feature_engineering_pipeline.py` | Leak-free pipelines, safe target encoding, Optuna-style tuning | 3 | 5 | sklearn |
| `lab03_ab_test_analysis.py` | Power analysis + full A/B test analysis | 2 | 2–3 | scipy, statsmodels |
| `lab04_model_monitoring.py` | Drift detection & monitoring signals | 5 | 10–11 | numpy, scipy |
| `lab05_rag_from_scratch.py` | RAG: embed → retrieve → ground (no framework) | 6 | 8 | numpy (optional: sentence-transformers) |

## How to work through a lab

1. **Read it top to bottom first** — the comments are the lesson.
2. **Run it** and study the printed output.
3. **Predict, then break it** — change a parameter and predict the effect before
   running again.
4. **Do the "Extend this" challenges** at the bottom of each file.
5. **Explain it to someone.** If you can't, you don't know it yet.

```bash
python hands-on/lab01_leakage_and_validation.py
```
