# Cheatsheets — Dense Quick Reference

Compressed, high-density reference for fast recall. Not a substitute for the
modules — these are for *after* you've learned the concept and need a fast
reminder (e.g., before an interview or a design review).

---

## Metric selection (classification)

| Situation | Use | Avoid / why |
|---|---|---|
| Balanced classes, equal costs | Accuracy, ROC-AUC | — |
| Imbalanced (rare positives) | **PR-AUC**, recall@precision | Accuracy (misleading), ROC-AUC (optimistic) |
| Probabilities feed a decision | Log loss + **calibration** | Bare accuracy |
| Ranking / recsys | NDCG, MAP, recall@k | — |
| Asymmetric error costs | Cost-weighted threshold | Default 0.5 threshold |

## Metric selection (regression)
- **MAE** = robust to outliers; **RMSE** = punishes large errors; **MAPE** =
  breaks near zero; **Quantile loss** = asymmetric costs / prediction intervals.

## Cross-validation scheme
| Data | Scheme |
|---|---|
| i.i.d. tabular | Stratified K-Fold |
| Time-series | TimeSeriesSplit (forward chaining), never shuffle |
| Grouped entities | GroupKFold |
| Rare events | Stratified + enough positives/fold |

## Leakage checklist
- [ ] Did any transform (scale/impute/select/encode) see test/full data? → pipeline it.
- [ ] Is any feature a proxy for the label or only known post-outcome? → drop it.
- [ ] Random split on time-ordered data? → use TimeSeriesSplit.
- [ ] Same entity in train & test (and you must generalize to new ones)? → GroupKFold.
- [ ] Near-duplicate rows across splits? → dedupe first.

---

## A/B testing quick reference
- **Before launch:** define OEC + guardrails, unit of randomization, sample size
  (power analysis), duration (cover weekly seasonality).
- **p-value** = P(data this extreme | null true). NOT P(null true).
- **95% CI** ≠ "95% chance the value is inside" (frequentist).
- **Peeking** inflates false positives → fix sample size OR use sequential testing.
- **Significant ≠ meaningful** with large n. Report effect size + CI + guardrails.
- **CUPED** = variance reduction via pre-experiment covariate → less traffic.
- **Can't randomize?** → causal inference (DiD, IV, RDD, matching, synthetic control).

---

## Gradient boosting hyperparameters (XGBoost/LightGBM/CatBoost)
- `learning_rate` ↓ + `n_estimators` ↑ (with **early stopping**) = the core trade-off.
- Complexity: `max_depth` / `num_leaves`.
- Regularization: `lambda` (L2), `alpha` (L1), `min_child_weight`/`min_data_in_leaf`.
- Sampling: `subsample`, `colsample_bytree`.
- Trees: no scaling needed; handle missing values & monotonic relations natively.
- **CatBoost** for many categoricals; **LightGBM** for speed/large data; **XGBoost** robust default.

---

## Drift & monitoring
- **PSI**: <0.1 stable · 0.1–0.25 moderate · >0.25 major.
- **Covariate shift** = P(X) changes (visible in feature/prediction drift, no labels needed).
- **Concept drift** = P(y|X) changes (often invisible in inputs; needs labels/KPIs).
- Monitor 3 layers: **operational** (latency/errors), **data quality** (schema/nulls/range), **model quality** (drift now, accuracy when labels arrive).

---

## RAG quick reference
- Pipeline: chunk → embed → retrieve (hybrid: dense + BM25) → rerank → grounded prompt → generate w/ citations.
- **Chunk** on semantic boundaries; tune size/overlap against an eval set.
- **Hybrid > pure vector** usually; add a **cross-encoder reranker** for precision.
- **Evaluate retrieval** (hit-rate@k, MRR) AND generation (faithfulness/groundedness).
- **RAG vs fine-tune:** RAG = inject knowledge; fine-tune = change behavior/format.
- Build a **regression eval set** → run on every prompt/model change (LLM "unit tests").
- Treat retrieved/user text as **untrusted** (prompt injection); constrain tools.

---

## LLM decision: prompt vs RAG vs fine-tune
| Need | Reach for |
|---|---|
| Fresh / private knowledge | RAG |
| Behavior, format, style, tone | Fine-tuning (LoRA/QLoRA) |
| Quick task adaptation | Prompting / few-shot |
| Domain vocab + consistent structure | Fine-tune (often + RAG) |
Default path: **prompt → add RAG → fine-tune only when those plateau**.

---

## Deep learning debugging (Karpathy's recipe, condensed)
1. **Overfit one batch first** — can't? It's a bug, not a model problem.
2. Get the **data pipeline** right (most bugs live here).
3. Start simple; add one change at a time.
4. Visualize loss, gradients, activations, predictions.
5. **LR** is the most important hyperparameter; use warmup + decay.

---

## ML system design (the 8-step skeleton)
1. Problem & requirements (ML or not? scale/latency/cost/privacy)
2. ML framing (inputs/outputs/task/labels)
3. Metrics (offline + online + guardrails)
4. Data (sources/volume/labels/freshness/splits/leakage)
5. Features (train vs serve; skew)
6. Model (baseline → candidates → choice + why)
7. Serving (batch vs online; latency; rollout)
8. Monitoring & iteration (drift; retrain trigger; rollback) + **failure modes**

---

## Communication (the senior reflexes)
- Lead with the **conclusion** (BLUF), then evidence.
- Quantify with **uncertainty**; state assumptions + "what would change my mind."
- One chart = one message; label with the takeaway.
- Frame trade-offs in the **stakeholder's** terms (revenue/risk/latency), not AUC.
- Always give a **recommendation**, not just numbers.
