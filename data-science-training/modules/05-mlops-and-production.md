# Module 5 — MLOps & Production Machine Learning

> **Why this matters:** A model that isn't deployed, monitored, and maintainable
> creates no value. This module is the difference between "data scientist who
> hands off a notebook" and "data scientist who owns a system in production."

**Outcome:** you can take a trained model and turn it into a versioned,
served, monitored, reproducible system — and you understand why ML systems decay.

---

## Section 1 — Why ML systems are different (and harder)

ML systems have all the problems of software *plus*:
- **Data dependencies** that change silently (upstream schema, distribution).
- **Training/serving skew** — code or data differs between train and inference.
- **Decay over time** — the world drifts; a static model gets worse.
- **Reproducibility across data + code + config + randomness.**

Read **"Hidden Technical Debt in Machine Learning Systems"** (Google, RESOURCES
§5) — the canonical paper on why "the model is 5% of the system."

## Section 2 — The ML lifecycle

```
Problem framing → Data → Features → Train/Experiment → Evaluate →
Package → Serve → Monitor → (Detect drift) → Retrain → repeat
```

MLOps is the engineering discipline that makes every arrow reliable, automated,
and reproducible.

## Section 3 — Experiment tracking & model registry

- **Track every run:** params, metrics, data version, code version, artifacts.
  Use **MLflow** (or W&B). "Which model is in prod and how was it trained?" must
  have a one-click answer.
- **Model registry:** versioned models with stages (staging/production), lineage,
  and the ability to roll back instantly.

## Section 4 — Packaging & serving

Two main patterns:
- **Batch / offline** — score a table on a schedule (Airflow + a job). Simplest;
  fits churn scores, nightly recommendations. Often the right default.
- **Online / real-time** — a service (FastAPI/BentoML) behind an API. Needed for
  per-request predictions. Watch **latency**, **throughput**, and **the feature
  computation path** (the hard part is computing features fast at request time).

Key concerns: versioned model artifact, input validation, graceful degradation,
A/B or shadow deployment, and reproducible containers (Docker).

## Section 5 — Feature/serving skew & feature stores

The most common production failure: features computed differently in training
(batch SQL) vs serving (live code). Mitigations:
- Single source of feature logic (shared library or a **feature store** like
  Feast for larger orgs).
- Log the actual features used at inference and compare to training.

## Section 6 — Reproducible pipelines & versioning

- **Data versioning:** DVC or immutable snapshots + hashes.
- **Pipeline orchestration:** Airflow / Prefect / Dagster for scheduled
  retraining and batch scoring.
- **Config & code versioning:** tie a model version to exact data + code + config.

## Section 7 — Monitoring (the part everyone skips)

You must monitor three layers:
1. **Operational** — latency, error rate, throughput, resource use (standard SWE).
2. **Data quality** — schema changes, nulls, range violations, volume anomalies.
   Bad data is the most common cause of bad predictions.
3. **Model quality** — prediction distribution drift, **feature drift**, and
   (when labels arrive) actual performance. Use **Evidently** or similar.

**Drift types:**
- **Covariate shift** — input distribution changes (P(X) shifts).
- **Concept drift** — the X→y relationship changes (P(y|X) shifts) — the
  dangerous one; accuracy degrades even if inputs look normal.

Labels are often delayed, so lean on **proxy signals** (prediction drift, feature
drift, business KPIs) for early warning.

## Section 8 — Retraining strategy

- **Trigger:** scheduled (e.g., weekly) vs performance-triggered vs drift-
  triggered. Decide deliberately.
- **Validate before promoting:** automated eval gate, comparison to current prod
  model, shadow testing. Never auto-deploy without a gate.
- **Rollback plan:** always have one.

## Section 9 — CI/CD for ML

- CI: lint, unit tests, data validation, a small training smoke test.
- CD: build container, run eval gate, register model, deploy to staging →
  canary → prod.
- **Test the data and the pipeline**, not just the code.

## Section 10 — Cost & scale awareness

- Know the cost of training and serving (GPU hours, inference $/1k requests).
- Right-size: batch vs online, model distillation/quantization, caching.
- Senior signal: choosing the *simplest* architecture that meets the SLA.

---

## Thinking questions
1. What's training/serving skew? How would you detect it before users complain?
2. Labels arrive 30 days late. How do you monitor model health in the meantime?
3. Covariate shift vs concept drift — which is more dangerous and why?
4. When is batch scoring the right choice over a real-time API?

## Deliverable
Wrap your Module 3 model in a containerized FastAPI service with a `/predict`
endpoint, input validation, MLflow-logged experiments, and a model registry
entry. Add basic monitoring (see `lab04`).

## Go deeper
RESOURCES §5. Priorities: *Designing ML Systems* (Chip Huyen), Made With ML
(end-to-end), awesome-production-machine-learning, MLflow + Evidently docs, the
Hidden Technical Debt paper.
