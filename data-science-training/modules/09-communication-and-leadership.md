# Module 9 — Communication, Influence & Technical Leadership

> **Why this matters:** At ~3 years, technical skill is assumed. What gets you to
> senior/staff is **impact through others**: scoping the right problems,
> influencing decisions, communicating clearly, and elevating the team. Many
> strong ICs stall here. This module is deliberately last because it amplifies
> everything before it.

**Outcome:** you can scope an ambiguous problem, write a decision-grade document,
present results so stakeholders can act, and mentor others.

---

## Section 1 — Problem scoping (the highest-leverage skill)

The most valuable thing a senior DS does is **work on the right problem**.
- Start from the **business decision/outcome**, not the model. Ask: "If this
  works perfectly, what changes? Who acts on it?"
- Translate vague asks ("can we use AI here?") into a crisp, measurable problem
  with a success metric and a baseline.
- Push back on ML when a heuristic or a dashboard would do. Knowing when *not* to
  build a model is senior judgment.
- Define done: what result, by when, accurate enough for what decision.

## Section 2 — Writing for impact

Strong writing is the force multiplier of remote/async orgs. Master a few formats:

- **The decision doc / one-pager** — context, options, recommendation, trade-offs,
  risks. A PM/EM should be able to act on it *without you in the room*.
- **The experiment/analysis write-up** — question, method, result with
  uncertainty, recommendation, caveats. Lead with the answer (BLUF — bottom line
  up front), then the evidence.
- **The design doc** — see Module 8.
- **The model card** — what the model does, data, metrics, limitations, intended
  use, failure modes.

Principles: lead with the conclusion; quantify with uncertainty; make the
recommendation explicit; state assumptions and what would change your mind.

## Section 3 — Visualizing & presenting

- One chart = one message. Label it with the takeaway, not just axes.
- Match the chart to the question (trend → line, comparison → bar, distribution →
  histogram/box, relationship → scatter). Avoid pie charts and dual axes.
- **Tailor to the audience:** executives want the decision and risk; engineers
  want the mechanism; analysts want the method. Same result, three framings.
- Always show uncertainty — error bars / CIs — and the practical (not just
  statistical) significance.

## Section 4 — Stakeholder management & influence

- Build a shared mental model *before* presenting results (no surprises).
- Frame trade-offs in their terms (revenue, risk, latency, effort), not yours
  (AUC, F1).
- Disagree with data and options, not opinions. Offer a recommendation, then make
  it easy to say yes.
- Manage expectations early: surface risks and unknowns before they bite.

## Section 5 — Working with engineers, PMs, and leadership

- **Engineers:** speak about interfaces, latency, failure modes, maintainability.
  Respect production constraints.
- **PMs:** speak about user impact, metrics, and trade-offs; help them prioritize.
- **Leadership:** speak about outcomes, risk, and resourcing; be concise and
  decisive.

## Section 6 — Technical leadership & mentoring

- **Mentoring:** review others' work on correctness, rigor, communication, and
  engineering (the four axes from `INSTRUCTOR_GUIDE.md`). Teaching deepens your
  own mastery.
- **Driving direction:** identify high-impact problems, write the doc that aligns
  people, and de-risk the plan. Influence without authority.
- **Raising the bar:** introduce better practices (testing, experimentation
  rigor, reproducibility) by example and by templates, not by decree.
- **Code/design reviews:** be specific, kind, and focused on the most important
  issues first.

## Section 7 — Career & growth

- Build a body of visible work (write-ups, internal docs, talks, OSS).
- Seek feedback aggressively and act on the patterns.
- Develop a specialization (depth) *and* range (breadth) — the "T-shaped" senior.

---

## Thinking questions
1. A stakeholder asks for "an AI model" for something a SQL query solves. What do
   you say?
2. Rewrite a result as a 3-sentence BLUF for an executive, then for an engineer.
3. Your experiment was inconclusive. How do you communicate that usefully?
4. How do you raise the team's experimentation rigor without being the "process
   police"?

## Deliverable
A decision doc for your capstone (Module/Week 12): problem framing, what you did,
result with uncertainty, recommendation, risks — readable and actionable by a
non-DS stakeholder. Plus a 10-minute presentation of it.

## Go deeper
- *The Pyramid Principle* (Barbara Minto) — structured business writing.
- *Storytelling with Data* (Cole Nussbaumer Knaflic) — data communication.
- *Trustworthy Online Controlled Experiments* (Kohavi) — also a model of how to
  communicate experiment results to decision-makers.
- Eugene Yan's and Chip Huyen's blogs — examples of excellent technical writing.
