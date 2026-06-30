# Module 8 — ML System Design

> **Why this matters:** System design separates senior from mid-level. It's the
> ability to take an ambiguous business problem and design the *whole* solution —
> data, features, model, serving, monitoring, and failure modes — while
> justifying every trade-off. It's also the centerpiece of senior interviews.

**Outcome:** you can lead a whiteboard/doc ML system design for a realistic
problem and defend your choices.

---

## Section 1 — The framework (use this every time)

Adapted from Chip Huyen's *Designing ML Systems* (RESOURCES §5, §8). Work top-down:

1. **Clarify the problem & requirements**
   - What's the business goal? What decision/action does the model drive?
   - Is ML even the right tool? (A heuristic might be enough.)
   - Functional + non-functional requirements: scale (QPS, data volume),
     latency SLA, accuracy needs, budget, privacy/regulatory constraints.

2. **Frame as an ML problem**
   - Inputs, outputs, and the ML task type (classification/regression/ranking/
     generation). What's the label, and how do you get it?
   - Define **success metrics**: offline (model) AND online (business), plus
     guardrails.

3. **Data**
   - Sources, volume, labels (and label latency/cost), freshness, quality.
   - Train/val/test split that matches deployment; how you avoid leakage.

4. **Features**
   - Candidate features, how they're computed at train vs serve time (skew!),
     batch vs real-time feature path.

5. **Model**
   - Baseline first. Candidate models with trade-offs (interpretability, latency,
     training cost, data needs). Why this one.

6. **Serving**
   - Batch vs online; latency/throughput; where features come from at request
     time; A/B or shadow rollout.

7. **Monitoring & iteration**
   - Drift, data quality, performance; retraining trigger; rollback.

8. **Failure modes & risks**
   - What breaks? Cold start, feedback loops, adversarial inputs, fairness,
     degenerate predictions, dependency failures. Mitigations for each.

> Senior signal: you spend most time on **problem framing, data, metrics,
> serving constraints, and failure modes** — not on picking the fanciest model.

---

## Section 2 — Recurring design patterns

- **The OEC + guardrails** pattern — one decision metric, several "don't make it
  worse" metrics.
- **Two-stage retrieval+ranking** (recsys/search) — cheap candidate generation,
  expensive precise ranking. Know it cold.
- **Cascade / fallback** — cheap model first, escalate hard cases.
- **Shadow deployment** — run new model in parallel, compare, no user impact.
- **Human-in-the-loop** — for high-stakes or low-confidence predictions.
- **Feedback loops** — when predictions influence future training data (e.g.,
  recommendations shape clicks); recognize and break harmful ones.

---

## Section 3 — Worked archetypes to practice

Practice designing these (then compare with real write-ups in
**eugeneyan/applied-ml**, RESOURCES §8):

- **Recommendation system** (e.g., "recommend products/videos") — candidate
  generation + ranking, cold start, feedback loops, freshness.
- **Fraud / abuse detection** — extreme imbalance, adversarial adaptation,
  precision/recall trade-off, real-time latency, label delay.
- **Churn prediction** — label definition, time-based split, action mapping
  (what do you *do* with a churn score?), batch serving.
- **Search ranking** — relevance labels, NDCG, two-stage, query understanding.
- **Demand/forecasting** — time-series CV, seasonality, intervals not points.
- **An LLM-powered feature** (e.g., support assistant) — RAG, eval harness,
  latency/cost, hallucination guardrails, fallback to human.

For each: state assumptions, sketch the data flow, name the metric, and call out
the top 3 failure modes.

---

## Section 4 — Non-functional thinking (the senior differentiator)

- **Scale:** QPS, data volume, model size — does the design hold at 100x?
- **Latency:** end-to-end budget; where the time goes (feature computation often
  dominates, not inference).
- **Cost:** training + serving; is the value worth it?
- **Reliability:** graceful degradation, fallbacks, no single point of failure.
- **Maintainability:** can the team operate and evolve this in a year?
- **Ethics/compliance:** privacy, fairness, explainability requirements.

---

## Section 5 — How to practice

1. Read Chip Huyen's 27 design questions
   (**chiphuyen/machine-learning-systems-design**) and answer 5 in writing.
2. For each archetype above, write a 1–2 page design doc using the §1 framework.
3. Read 5 real write-ups in **eugeneyan/applied-ml** and reverse-engineer their
   design decisions.
4. Do mock design sessions out loud (explain to a peer) — design is communication.

---

## Thinking questions
1. Design a system to recommend items on a homepage. Where does latency go?
2. How would you design a system to know *when* a model should be retrained?
3. A recsys creates a feedback loop that narrows recommendations over time. How
   do you detect and fix it?
4. For fraud detection, why might you optimize precision at a fixed recall, and
   how does adversarial adaptation change your monitoring?

## Deliverable
A full ML system design doc for a realistic problem (pick one archetype),
covering all 8 framework steps, with an explicit failure-modes section. Use the
template in `projects/README.md`.

## Go deeper
RESOURCES §8 + §5. Priorities: *Designing ML Systems* (Chip Huyen),
chiphuyen/machine-learning-systems-design, eugeneyan/applied-ml,
khangich/machine-learning-interview, the System Design Primer.
