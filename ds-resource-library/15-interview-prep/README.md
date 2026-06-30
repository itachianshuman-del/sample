# 15 · Data Science Interview Prep

> Everything that gets tested in DS/ML interviews — SQL, stats, ML, coding, and
> system design — plus the strategy to pass each round.

---

## 📌 What it is & why it matters

DS/ML interviews are broad: they probe coding, SQL, statistics, ML breadth + depth,
ML system design, and behavioral/communication. Strong on-the-job skills don't
automatically translate to interview performance — you need targeted, deliberate
practice on the specific formats.

---

## 🧠 What gets tested (the rounds)

- **SQL** — joins, aggregations, **window functions**, query writing under time.
- **Coding / DSA** — Python data manipulation, sometimes LeetCode-style (easy–medium).
- **Statistics & probability** — A/B testing, p-values, distributions, Bayes,
  estimation; "explain it simply" questions.
- **ML breadth** — algorithms, bias-variance, regularization, metrics, leakage,
  "how would you approach X?"
- **ML depth** — your past projects: be ready to defend every choice.
- **ML system design** — design a recommender / fraud / search system end-to-end
  (the senior differentiator).
- **Behavioral** — impact, collaboration, conflict, communication (STAR format).
- **Case / product** — frame an ambiguous business problem into a measurable one.

---

## 📚 Best resources

### Books & guides
- **Introduction to Machine Learning Interviews** (Chip Huyen, free):
  https://huyenchip.com/ml-interviews-book/
- **machine-learning-interview** (Khang Pham) — FAANG-style, system design + prep:
  https://github.com/khangich/machine-learning-interview
- **Data-Science-Interview-Resources** (rbhatia46): https://github.com/rbhatia46/Data-Science-Interview-Resources
- **Ace the Data Science Interview** (book) — broad coverage + SQL/stats drills.
- **Krish Naik — interview prep & "crack DS interviews"** content + the
  [Data Science Gen-AI Playlist 2024](https://github.com/krishnaik06/Data-Science-Gen-AI-Playlist-2024)
  (interview prep + real-world projects).

### Practice platforms
- **DataLemur** (SQL/stats/ML): https://datalemur.com/
- **StrataScratch** (real company questions) · **LeetCode** (coding) · **Pramp** (mock interviews).

### System design
- **chiphuyen/machine-learning-systems-design** (framework + 27 questions):
  https://github.com/chiphuyen/machine-learning-systems-design
- **eugeneyan/applied-ml** (real systems to study): https://github.com/eugeneyan/applied-ml
- Deep dive: [`data-science-training/modules/08-ml-system-design.md`](../../data-science-training/modules/08-ml-system-design.md)

---

## 💻 Code example

```sql
-- A frequently-asked SQL interview pattern: top-N per group.
-- "Find the top 2 highest-paid employees in each department."
SELECT department, name, salary
FROM (
    SELECT
        department, name, salary,
        DENSE_RANK() OVER (PARTITION BY department
                           ORDER BY salary DESC) AS rnk
    FROM employees
) ranked
WHERE rnk <= 2
ORDER BY department, salary DESC;
```

```python
# A common Python/stats question: simulate to build intuition.
# "If you flip a fair coin 10 times, P(at least 8 heads)?"
import numpy as np
rng = np.random.default_rng(0)
trials = rng.binomial(n=10, p=0.5, size=1_000_000)
print(f"P(>=8 heads) ~ {(trials >= 8).mean():.4f}")   # ~0.0547
```

---

## 🌍 Interview strategy (the meta-skills)

- **Clarify before solving** — restate the question, state assumptions.
- **Think out loud** — interviewers score reasoning, not just the final answer.
- **Start with a baseline** — simplest approach first, then improve.
- **Connect to impact** — tie answers to business outcomes.
- **For system design** — use a framework (requirements → data → metrics →
  features → model → serving → monitoring → failure modes).

---

## 🛠️ Practice plan (4–6 weeks)

1. **Week 1–2:** SQL daily (DataLemur) + stats fundamentals.
2. **Week 3:** ML breadth flashcards + defend your past projects out loud.
3. **Week 4:** ML system design — write 5 design docs, do mocks.
4. **Week 5–6:** Full mock loops (Pramp/peers) + behavioral STAR stories.

---

## 🗺️ Suggested learning path

1. Diagnose gaps with a mock → 2. Drill SQL + stats (highest ROI) → 3. ML breadth
+ project defense → 4. System design framework + reps → 5. Behavioral stories →
6. Full mock loops until consistent.
