# Module 2 — Statistics, Experimentation & Causal Inference

> **Why this matters:** Most ML work is judged by a business decision: ship or
> don't, invest or don't. That decision rests on **inference and experimentation**,
> not model accuracy. This is the single highest-leverage area for an experienced
> DS to deepen, and the most common gap in interviews and promo cases.

**Outcome:** you can design and analyze an experiment end-to-end, reason about
causality when you can't experiment, and avoid the classic statistical traps.

---

## Section 1 — Sampling & the foundations

- **Population vs sample**, sampling distribution, standard error.
- **Central Limit Theorem** — why means are ~normal even when data isn't, and
  when it fails (heavy tails, tiny n, dependence).
- **Law of Large Numbers** vs CLT — don't conflate them.

Key intuition: the *standard error* shrinks like `1/sqrt(n)`. Quadrupling your
sample halves your uncertainty. This governs every "how much data do I need?"
question.

## Section 2 — Estimation & uncertainty

- **Confidence intervals**: what they do and don't mean (a 95% CI does NOT mean
  "95% probability the true value is in this interval" in the frequentist sense).
- **Bootstrap** — your Swiss-army knife for CIs when formulas are hard. Resample
  with replacement, recompute the statistic, take percentiles.
- **Bayesian alternative** — credible intervals, which *do* have the intuitive
  probability interpretation; useful for communicating with stakeholders.

## Section 3 — Hypothesis testing without fooling yourself

- Null/alternative, test statistic, **p-value** (probability of data this extreme
  *if the null were true* — not "probability the null is true").
- **Type I / Type II errors**, significance level α, **power** (1 − β).
- **The pitfalls that bite practitioners:**
  - **p-hacking / the garden of forking paths** — trying many things and
    reporting the significant one.
  - **Multiple comparisons** — testing 20 metrics at α=0.05 → ~1 false positive
    expected. Correct with Bonferroni / Benjamini-Hochberg (FDR).
  - **Peeking** — checking an experiment repeatedly and stopping when significant
    inflates false positives massively. (Fix: sequential testing, §6.)
  - **Confusing statistical and practical significance** — with huge n,
    meaningless effects become "significant."

## Section 4 — Power & sample size (do this BEFORE the experiment)

Power analysis answers "how many samples to detect an effect of size X with
probability 1−β at significance α?" Always do this *before* launching, or you
risk an underpowered test that can't conclude anything.

Drivers: larger effect → fewer samples; lower variance → fewer samples; higher
desired power / lower α → more samples. See `hands-on/lab03_ab_test_analysis.py`.

---

## Section 5 — Designing an A/B test

A senior-quality experiment design specifies, *before launch*:

1. **Hypothesis & decision** — what will we do with each outcome?
2. **Unit of randomization** — user? session? cluster? (Mismatch causes leakage
   between arms via network effects or repeated exposure.)
3. **Primary metric (OEC)** — one Overall Evaluation Criterion you'll decide on.
4. **Guardrail metrics** — things that must NOT get worse (latency, revenue,
   crashes) even if the primary metric improves.
5. **Sample size & duration** — from power analysis; cover weekly seasonality.
6. **Segmentation plan** — pre-registered, to avoid fishing.

## Section 6 — Advanced experimentation

- **CUPED** (variance reduction using pre-experiment data) — same power with far
  less traffic. A core technique at scale.
- **Sequential / always-valid testing** — lets you peek without inflating error
  (mSPRT, group sequential designs). Used by modern platforms.
- **Stratification & covariate adjustment** — reduce variance, fix imbalance.
- **Interference / network effects** — when one user's treatment affects another
  (marketplaces, social). Use cluster randomization or switchback designs.
- **Novelty & primacy effects** — early behavior ≠ steady state.

## Section 7 — When you can't run an experiment (causal inference)

Often you can't randomize (ethics, cost, can't withhold). Then you need
**observational causal inference**:

- **Potential outcomes framework** — treatment effect = Y(1) − Y(0); the
  fundamental problem is you only ever observe one.
- **Confounding** — a common cause of treatment and outcome biases naive
  comparisons. Draw a **DAG** to reason about what to control for (and what NOT
  to — controlling for a collider or mediator introduces bias).
- **Methods:** matching / propensity scores, regression adjustment, **difference-
  in-differences**, **instrumental variables**, **regression discontinuity**,
  synthetic control.
- **Simpson's paradox** — aggregated trends can reverse within subgroups; a
  warning to think causally, not just correlationally.

## Section 8 — Communicating uncertainty

- Report effect size + CI, not just "significant."
- State assumptions and what would change the conclusion.
- Give a decision recommendation, not just a number.

---

## Thinking questions
1. A test shows +0.3% conversion, p=0.04, n=2M. Ship it? What else do you need?
2. Your PM checked the dashboard daily and the result "became significant" on
   day 6. What's wrong, and what do you tell them?
3. You can't A/B test a pricing change. How would you estimate its causal effect?
4. Explain Simpson's paradox with a concrete business example.

## Deliverable
A complete A/B test write-up (design → power analysis → analysis → ship/no-ship
recommendation with guardrails and caveats), using `lab03`.

## Go deeper
RESOURCES §2. Priorities: *Trustworthy Online Controlled Experiments* (Kohavi)
for experimentation; *Causal Inference for the Brave and True* (Facure) and
Brady Neal's course for causality.
