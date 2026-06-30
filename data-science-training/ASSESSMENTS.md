# Assessments, Checkpoints & "Are You Senior Yet?"

How you know the training is working. Use these checkpoints, rubrics, and
self-tests. Remember the core rule: **you don't "know" a module until you can
teach it and ship something with it.**

---

## The 4-axis rubric (apply to every deliverable)

Score each deliverable 1–4 on each axis. Senior ≈ consistent 3–4 across all four.

| Axis | 1 (Junior) | 2 (Mid) | 3 (Senior) | 4 (Staff) |
|---|---|---|---|---|
| **Correctness** | Bugs / wrong result | Mostly right | Right & validated | Right, validated, edge cases handled |
| **Rigor** | Assumptions unstated | Some checks | Assumptions stated & tested | Stress-tested; knows where it breaks |
| **Communication** | Only they understand it | Other DS understand | A PM can act on it | Drives a decision across the org |
| **Engineering** | Notebook only | Some functions | Tested, reproducible | Packaged, CI, maintainable |

Most mid-level ICs are strong on **Correctness** and weak on **Rigor** and
**Engineering**. Target the weak axes deliberately.

---

## Phase checkpoints

### Checkpoint 1 — after Week 3 (Foundations)
- [ ] A past project is now an installable, tested package with CI.
- [ ] You can compute a required sample size and explain power vs significance.
- [ ] You produced an A/B test write-up with a clear ship/no-ship recommendation.
- [ ] **Mock:** explain p-values, CIs, and peeking to a non-statistician in 5 min.

### Checkpoint 2 — after Week 6 (ML depth)
- [ ] You can name and detect 4+ kinds of leakage, with code.
- [ ] You built a leak-free, tuned pipeline with a justified metric & CV scheme.
- [ ] You produced an interpretability + error-slice report.
- [ ] **Mock:** "Your AUC is 0.95 offline, useless live — debug it" (talk it out).

### Checkpoint 3 — after Week 9 (DL & GenAI)
- [ ] You implemented backprop from scratch and can explain it.
- [ ] You built a RAG system with a real retrieval evaluation harness.
- [ ] You fine-tuned a model OR wrote a rigorous prompt-vs-RAG-vs-finetune report.
- [ ] **Mock:** "When RAG vs fine-tuning?" and "How do you evaluate an LLM feature?"

### Checkpoint 4 — after Week 12 (Production & systems)
- [ ] You shipped a containerized, monitored model service.
- [ ] You wrote a full ML system design doc with explicit failure modes.
- [ ] You completed the capstone end-to-end + a stakeholder-ready decision doc.
- [ ] **Mock:** a 45-min ML system design interview on a new problem.

---

## The "Are You Senior Yet?" self-test

Answer honestly. A senior DS can do **all** of these without notes:

**Statistics & experimentation**
- [ ] Design an A/B test end-to-end (unit, OEC, guardrails, sample size, duration).
- [ ] Explain why peeking inflates false positives and how to fix it.
- [ ] Estimate a causal effect when you *can't* run an experiment.

**Machine learning**
- [ ] List 4 ways leakage hides and how to prevent each.
- [ ] Choose and justify a metric + CV scheme for an unfamiliar problem.
- [ ] Explain why a high-AUC model can be useless in production.
- [ ] Do an error-slice analysis and turn it into the next action.

**Production / MLOps**
- [ ] Take a model from notebook to monitored service.
- [ ] Distinguish covariate shift from concept drift and monitor for both.
- [ ] Design a retraining trigger + validation gate + rollback.

**GenAI / LLMs**
- [ ] Build and evaluate a RAG system (retrieval metrics, not vibes).
- [ ] Decide between prompting, RAG, and fine-tuning with justification.
- [ ] Stop an LLM feature from silently regressing.

**System design & communication**
- [ ] Lead an ML system design for a new problem, including failure modes.
- [ ] Write a decision doc a PM can act on without you.
- [ ] Scope a vague request into a measurable problem (and push back when ML is wrong).

If you can check ~90% of these honestly, you're operating at senior level.

---

## Capstone evaluation (the final proof)

Your capstone (Week 12) is scored on the 4-axis rubric, and must demonstrate:
1. **Problem framing** tied to a real decision.
2. **Rigorous data + modeling** (leak-free, validated, right metric).
3. **A shipped artifact** (service or reproducible pipeline) with monitoring.
4. **A decision doc + presentation** a stakeholder can act on.

A capstone that scores 3+ on all four axes is portfolio-grade and promo-case
evidence. See `projects/README.md` for capstone briefs.
