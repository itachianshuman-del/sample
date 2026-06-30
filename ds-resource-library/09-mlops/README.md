# 09 · MLOps & Production ML

> Getting models *out of notebooks* and into reliable, monitored, maintainable
> production systems. The skill that turns experiments into business value.

---

## 📌 What it is & why it matters

MLOps applies software/DevOps engineering discipline to the ML lifecycle:
versioning, testing, deployment, monitoring, and automated retraining. A model
that isn't deployed and monitored creates no value — and "the model is only ~5%
of a real ML system." This is the single biggest gap between mid-level and senior
practitioners.

---

## 🧠 Core concepts

- **The lifecycle:** data → features → train → evaluate → package → serve →
  monitor → retrain.
- **Experiment tracking & model registry** — reproducibility; "what's in prod and
  how was it trained?" must have a one-click answer (MLflow, W&B).
- **Serving patterns:** batch (scheduled scoring) vs online (real-time API).
- **Containerization & CI/CD** — Docker, automated tests, eval gates, canary/
  shadow deploys.
- **Monitoring:** operational (latency/errors), data quality (schema/nulls), and
  model quality (**drift** — covariate vs concept, performance when labels arrive).
- **Training/serving skew** — the most common production failure.
- **Feature stores, data/model versioning (DVC), orchestration (Airflow).**

> Deep dive + lab:
> [`data-science-training/modules/05-mlops-and-production.md`](../../data-science-training/modules/05-mlops-and-production.md),
> `hands-on/lab04_model_monitoring.py`.

---

## 📚 Best resources

### Courses & books
- **Made With ML** (Goku Mohandas) — free, end-to-end MLOps with code:
  https://github.com/GokuMohandas/Made-With-ML
- **Designing Machine Learning Systems** (Chip Huyen) — the best production-ML
  book: https://github.com/chiphuyen/dmls-book
- **Krish Naik — MLOps playlist** (MLflow, Docker, deployment, hands-on).
- **DataTalksClub — MLOps Zoomcamp** (free cohort course):
  https://github.com/DataTalksClub/mlops-zoomcamp

### Curated lists & tools
- **awesome-production-machine-learning** (EthicalML): https://github.com/EthicalML/awesome-production-machine-learning
- **awesome-mlops** (kelvins): https://github.com/kelvins/awesome-mlops
- MLflow: https://mlflow.org/ · Evidently (drift/monitoring): https://github.com/evidentlyai/evidently
- DVC: https://dvc.org/ · BentoML/FastAPI for serving.

---

## 💻 Code example

```python
# Track an experiment + serve readiness with MLflow (the MLOps starting point).
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=2000, random_state=0)

with mlflow.start_run():
    params = {"n_estimators": 300, "max_depth": 6}
    model = RandomForestClassifier(**params).fit(X, y)
    auc = cross_val_score(model, X, y, scoring="roc_auc", cv=5).mean()

    mlflow.log_params(params)            # what we tried
    mlflow.log_metric("cv_auc", auc)     # how it did
    mlflow.sklearn.log_model(model, "model")   # the artifact (versioned)
    print(f"logged run with cv_auc={auc:.3f}")
# Later: register the best run's model and promote it to 'Production'.
```

---

## 🌍 Real-world use cases

- **Real-time scoring APIs** — fraud, recommendations, ranking behind a service.
- **Batch scoring pipelines** — nightly churn scores, lead scoring.
- **Automated retraining** — drift-triggered or scheduled, with eval gates.
- **Monitoring & alerting** — catch data/model issues before users do.

---

## 🛠️ Hands-on project ideas

1. Wrap a model in a **FastAPI `/predict` service**, containerize with Docker,
   and log runs to MLflow.
2. Build a **drift monitor** with Evidently and an alert when PSI > 0.25.
3. Set up a **CI/CD pipeline** (GitHub Actions) that tests + an eval gate before deploy.

---

## 🗺️ Suggested learning path

1. Experiment tracking (MLflow) → 2. Packaging & serving (FastAPI + Docker) →
3. CI/CD + eval gates → 4. Monitoring & drift (Evidently) → 5. Orchestration
(Airflow) → 6. Full end-to-end project (Made With ML / MLOps Zoomcamp).
