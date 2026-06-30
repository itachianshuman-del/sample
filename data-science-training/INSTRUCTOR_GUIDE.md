# Instructor & Context Guide

> This file gives **context** for anyone using or delivering this program —
> whether you're a mentor running it with a mentee, a manager onboarding a data
> scientist, or the learner running it solo. Read this before the curriculum.

---

## 1. Context: what problem this program solves

Data scientists at the ~3-year mark usually hit one of a few plateaus:

- **The "notebook ceiling"** — strong at analysis and modeling in notebooks, but
  work never reaches production cleanly, isn't reproducible, and is hard to hand off.
- **The "accuracy trap"** — optimizes offline metrics without connecting to
  business outcomes, experiment design, or causal reasoning.
- **The "tool follower"** — can use libraries but struggles to design a system,
  choose between approaches, or justify trade-offs to stakeholders.
- **The "GenAI gap"** — deep classical ML skills but hasn't operationalized LLMs.

This program is explicitly designed to break through those plateaus. It is
**opinionated**: it prioritizes the skills that hiring committees and promotion
panels actually evaluate for senior roles.

---

## 2. Target learner profile (assumed starting point)

The learner is assumed to be comfortable with:

- Python (functions, classes, comprehensions, basic OOP), `pandas`, `numpy`
- `scikit-learn` for standard supervised learning
- Basic SQL (joins, group by, window functions at a basic level)
- Git basics (commit, push, branch)
- One or more real projects: a model in production *or* a substantial analysis,
  plus personal/portfolio projects

If a learner is **below** this bar, send them to the "Prerequisite refresher"
section in `RESOURCES.md` first (2–3 weeks) before starting Week 1.

---

## 3. How to run the program (three modes)

### Mode A — Mentor + mentee (recommended, 12 weeks)
- **Weekly 60-min 1:1**: review the deliverable, discuss the "thinking
  questions" in each module, do one mock (system design or stats reasoning).
- Mentor's job is **not** to lecture — it's to review deliverables, pressure-test
  reasoning, and share war stories. Use the rubrics in `ASSESSMENTS.md`.
- Mentee does ~8–10 hrs/week of focused work between sessions.

### Mode B — Self-paced solo (12–20 weeks)
- Follow `CURRICULUM.md` in order. Replace the mentor review with: write a short
  blog post / internal doc explaining each deliverable. Teaching = the test.
- Find a peer or community (see `RESOURCES.md`) to review your work.

### Mode C — Team onboarding / cohort (8–12 weeks)
- Run modules as bi-weekly seminars. Each member presents one module.
- Use the capstone projects in `projects/` as shared, reviewed deliverables.

---

## 4. Time budget

| Commitment | Duration | Best for |
|---|---|---|
| ~10 hrs/week | 12 weeks | Working professional, focused |
| ~5 hrs/week | ~20 weeks | Busy schedule, steady pace |
| Full-time | ~4–5 weeks | Between jobs / dedicated sprint |

Depth beats speed. It is better to fully complete 6 modules than to skim 9.

---

## 5. Teaching principles baked into this material

1. **Learn by shipping.** Every module ends in a concrete artifact, not a
   "completed reading." Knowledge that doesn't produce an artifact evaporates.
2. **Fundamentals first, tools second.** We teach the concept, then name 2–3
   tools that implement it. Tools are swappable; concepts compound.
3. **Production is the destination.** Even the stats and modeling modules are
   framed by "how does this survive contact with real data and real users?"
4. **Reasoning over recall.** The assessments test *judgment* (when/why), not
   trivia. Senior work is mostly judgment under ambiguity.
5. **Read the source.** Curated repos and papers are linked so the learner
   builds the habit of going to primary sources, not just tutorials.

---

## 6. How to give feedback on deliverables (for mentors)

For each deliverable, evaluate on four axes (detailed rubric in `ASSESSMENTS.md`):

- **Correctness** — is the analysis/model/system actually right?
- **Rigor** — were assumptions stated, validated, and stress-tested?
- **Communication** — could a non-expert stakeholder act on this?
- **Engineering** — is it reproducible, tested, and maintainable?

A senior IC scores high on all four; a mid-level IC is usually strong on
correctness but weak on rigor and engineering. Target the weak axes.

---

## 7. Maintenance & attribution

- The external resources in `RESOURCES.md` are curated from widely-recognized,
  high-quality sources (linked inline). Tooling moves fast — re-check links and
  versions roughly every quarter.
- All linked third-party materials belong to their respective authors; this repo
  only curates and links to them, with original code/notes written for this program.

> *Some descriptions of external resources here were summarized/paraphrased for
> brevity; always refer to the linked original for authoritative detail.*

Next: open `CURRICULUM.md`.
