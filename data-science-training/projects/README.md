# Capstone Projects

Portfolio-grade project briefs. Each is designed to exercise the **full** senior
skill set: problem framing → data → modeling → evaluation → serving → monitoring
→ communication. Pick **one** for your Week 12 capstone (or do more over time).

Each brief intentionally leaves room for judgment — that's the point. A senior DS
turns an ambiguous brief into a scoped, defensible solution.

> For more guided project ideas, see `youssefHosni/Awesome-AI-Data-Guided-Projects`
> and Kaggle (RESOURCES §10).

---

## How to do a capstone well

Deliver all of:
1. **A decision doc** (see the template below) — the most important artifact.
2. **A reproducible repo** — packaged, tested, one-command reproduce (Module 1).
3. **A served artifact** — a batch pipeline or an API service (Module 5).
4. **Monitoring** — drift/quality checks (Module 5, `lab04`).
5. **A 10-minute presentation** — tailored to a non-DS stakeholder (Module 9).

Score it against `ASSESSMENTS.md` (the 4-axis rubric).

---

## Project 1 — Churn prediction that drives an action (tabular, end-to-end)
**Business framing:** predict which customers will churn so retention can
intervene — but the score is worthless unless it changes a decision.
- **Hard parts:** define "churn" precisely; time-based split (no leakage);
  choose a metric tied to intervention cost; map scores → actions (who to
  contact, expected ROI).
- **Stretch:** add uplift modeling (treat vs not), not just churn probability.
- **Skills:** Modules 1, 3, 5. Labs 01, 02, 04.

## Project 2 — Experimentation analysis & decision (stats-heavy)
**Business framing:** you're handed (or simulate) results from a product
experiment; deliver a trustworthy ship/no-ship recommendation.
- **Hard parts:** power/sample-size justification, guardrail metrics, multiple
  comparisons, segment analysis without fishing, communicating uncertainty.
- **Stretch:** apply CUPED for variance reduction; analyze a case where you
  *can't* randomize and use a causal method instead.
- **Skills:** Module 2, 9. Lab 03.

## Project 3 — RAG assistant over a real corpus (GenAI, end-to-end)
**Business framing:** build a question-answering assistant over a document set
(docs, policies, a codebase) that's grounded and doesn't hallucinate.
- **Hard parts:** chunking strategy, hybrid retrieval + reranking, a real
  evaluation harness (retrieval + faithfulness), latency/cost, abstaining when
  unsure, prompt-injection safety.
- **Stretch:** compare prompting vs RAG vs fine-tuning on one task with metrics.
- **Skills:** Modules 4, 6, 5. Lab 05.

## Project 4 — Recommendation / ranking system (system design + ML)
**Business framing:** recommend items (products, content) with a two-stage
candidate-generation + ranking design.
- **Hard parts:** offline vs online metrics, cold start, feedback loops,
  freshness, serving latency, evaluation that predicts online lift.
- **Stretch:** design (and partially build) the serving path and a monitoring plan.
- **Skills:** Modules 3, 5, 8. Labs 01, 02, 04.

## Project 5 — Fraud / anomaly detection (imbalance + adversarial + real-time)
**Business framing:** flag fraudulent transactions in near-real-time.
- **Hard parts:** extreme imbalance (PR-AUC, thresholding by cost), label delay,
  adversarial adaptation, real-time feature computation, precision at fixed
  recall, monitoring under drift.
- **Skills:** Modules 3, 5, 8. Labs 02, 04.

## Project 6 — Demand / time-series forecasting (intervals, not points)
**Business framing:** forecast demand to drive inventory/staffing decisions.
- **Hard parts:** time-series CV, seasonality/holidays, prediction *intervals*
  (decisions need uncertainty), backtesting, evaluating against a naive baseline.
- **Skills:** Modules 2, 3, 5. Labs 01, 04.

---

## Decision Doc Template (use for any capstone)

```markdown
# <Project> — Decision Doc

## TL;DR (BLUF)
<2-3 sentences: what you found and what you recommend.>

## Problem & decision
- What business decision does this inform? Who acts on it?
- Why ML (or why not)? What's the baseline / status quo?

## Success metrics
- Offline (model): <metric + why>
- Online / business: <metric + guardrails>

## Data
- Sources, volume, label definition, freshness, known quality issues.
- Train/val/test scheme and how leakage is prevented.

## Approach
- Baseline, candidate models, chosen model + why. Key features.

## Results (with uncertainty)
- Headline metric + CI. Error-slice analysis. Where it fails.

## Recommendation
- Ship / don't ship / iterate. The action. Expected impact.

## Risks & failure modes
- Top 3 ways this breaks in production + mitigations + monitoring plan.

## What would change my mind
- The assumptions and the evidence that would flip the recommendation.
```

---

## ML System Design Doc Template (for Project 4/5 or Module 8)

```markdown
# <System> — ML System Design

1. Problem & requirements (goal, ML or not, scale/latency/cost/privacy)
2. ML problem framing (inputs, outputs, task type, labels)
3. Metrics (offline, online, guardrails)
4. Data (sources, volume, labels, freshness, splits, leakage prevention)
5. Features (candidates, train vs serve computation, skew prevention)
6. Model (baseline, candidates + trade-offs, chosen + why)
7. Serving (batch vs online, latency budget, rollout: shadow/canary/A-B)
8. Monitoring & iteration (drift, quality, perf; retrain trigger; rollback)
9. Failure modes & risks (cold start, feedback loops, fairness, dependencies)
```
