# Module 3 — Machine Learning Deep Dive

> **Why this matters:** You already train models. This module is about doing it
> *rigorously* — the difference between a model that scores well offline and one
> that actually works in production and survives review.

**Outcome:** you can build leakage-free, well-validated, well-calibrated,
interpretable models and defend every modeling choice.

---

## Section 1 — Data leakage: the #1 silent killer

Leakage = information available at training time that won't be available at
prediction time. It produces *amazing* offline metrics and *terrible* production
performance. Common forms:

- **Target leakage** — a feature is a proxy for the label (e.g., "account_closed"
  feature when predicting churn).
- **Train-test contamination** — fitting any transform (scaler, imputer, target
  encoder, feature selection) on the *full* dataset before splitting.
- **Temporal leakage** — using future information to predict the past (random
  split on time-series data).
- **Group leakage** — same entity (patient, user) in both train and test when
  predictions should generalize to *new* entities.
- **Duplicate leakage** — near-duplicate rows split across train/test.

**Defense:** fit everything inside a `Pipeline`, split *first*, choose a CV
scheme that matches deployment, and ask "would I have this value at predict
time?" for every feature.

## Section 2 — Validation that matches reality

Your CV scheme must mirror how the model is used:
- **i.i.d. tabular** → stratified k-fold.
- **Time-series** → forward-chaining / `TimeSeriesSplit` (never shuffle time).
- **Grouped entities** → `GroupKFold` (groups don't cross folds).
- **Rare events** → stratified + enough positives per fold.

Always keep a **final hold-out** you touch only once. Beware tuning on the same
data you report — that's optimistic bias.

## Section 3 — Baselines & metrics

- **Always build a dumb baseline first** (majority class, mean, last value,
  simple heuristic). If your fancy model barely beats it, rethink.
- **Choose the metric the business cares about.** Accuracy is usually wrong for
  imbalanced data. Know:
  - Classification: precision/recall, F1, ROC-AUC vs **PR-AUC** (PR-AUC for rare
    positives), log loss, **calibration**.
  - Regression: MAE vs RMSE (RMSE punishes large errors), MAPE pitfalls, quantile
    loss for asymmetric costs.
  - Ranking/recsys: NDCG, MAP, recall@k.
- Tie the metric to a **cost model**: what does a false positive vs false
  negative actually cost the business?

## Section 4 — Threshold selection

The default 0.5 threshold is almost never right. Choose the threshold from the
cost trade-off (or to hit a precision/recall target). Report the operating point
you'd actually deploy, not just AUC.

## Section 5 — Calibration

A model can rank well (high AUC) but output miscalibrated probabilities. If
downstream decisions use the probability (expected value, pricing), calibrate
(Platt scaling / isotonic) and check with a reliability diagram.

## Section 6 — Feature engineering (where most of the gains are)

- **Encoding categoricals:** one-hot (low cardinality), ordinal (true order),
  **target/mean encoding** for high cardinality — *but only with cross-fold or
  smoothing to avoid leakage* (see lab02).
- **Numeric:** scaling (needed for linear/NN, not for trees), binning,
  log/power transforms for skew, interaction terms.
- **Temporal:** lags, rolling windows, time-since-event, cyclical encoding
  (sin/cos for hour/day).
- **Text/categorical hashing**, embeddings for high cardinality.
- **Domain features** beat fancy models more often than people admit.

## Section 7 — Gradient boosting (still king of tabular)

- **XGBoost / LightGBM / CatBoost** dominate tabular problems. Know the
  differences: LightGBM (leaf-wise, fast, big data), CatBoost (great native
  categorical handling), XGBoost (robust default).
- Key hyperparameters: learning rate × n_estimators (trade-off), max_depth /
  num_leaves, regularization (lambda, alpha), subsample/colsample, early stopping.
- Trees don't need scaling and handle monotonic relationships and missing values
  natively (a big practical advantage).

## Section 8 — Hyperparameter optimization

- Grid search is wasteful; use **Bayesian/TPE optimization (Optuna)** or random
  search. Always with proper CV and early stopping.
- Optimize the metric you'll deploy on, with the CV scheme that matches reality.
- Beware over-tuning to the validation set (meta-overfitting).

## Section 9 — Imbalanced data

- Don't reflexively oversample. First: is the metric right (PR-AUC)? Is the
  threshold right? Often these solve the "problem" without resampling.
- If needed: class weights, SMOTE (careful — can leak / create unrealistic
  points), focal loss. Always evaluate on the *natural* distribution.

## Section 10 — Interpretability

- **Global:** permutation importance, SHAP summary, partial dependence / ALE.
- **Local:** SHAP values for a single prediction ("why this customer?").
- Use it for **debugging** (find leakage, spurious features) as much as for
  stakeholder explanation.

## Section 11 — Error analysis (the senior habit)

Don't stop at aggregate metrics. **Slice the errors:** which segments, which
feature ranges, which classes fail most? Error analysis surfaces leakage, data
quality issues, and the next feature to build — far more valuable than chasing
0.2% AUC.

## Section 12 — Fairness & robustness

- Check performance across sensitive subgroups; understand fairness metric
  trade-offs (you can't satisfy all simultaneously).
- Stress-test: noise, missing features, distribution shift, adversarial-ish
  inputs. A model that's accurate but brittle fails in production.

---

## Thinking questions
1. Give 3 leakage examples that pass a naive random train/test split.
2. When is ROC-AUC misleading? What do you use instead?
3. Why is target encoding dangerous and how do you do it safely?
4. Your AUC is 0.95 offline but the model is useless live. Debug it — list steps.

## Deliverable
A leakage-free, tuned `Pipeline` on a real dataset with: justified CV scheme,
justified metric, calibration check, SHAP-based interpretation, and an error-slice
analysis. Write a one-page model card.

## Go deeper
RESOURCES §3. Priorities: ISLP, sklearn user guide, *Feature Engineering &
Selection*, Molnar's *Interpretable ML*, Google's *Rules of ML*.
