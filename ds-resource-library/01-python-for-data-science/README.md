# 01 · Python for Data Science

> The language of data science. Master the data stack (NumPy → pandas → Polars)
> and write code that's fast, correct, and reproducible.

---

## 📌 What it is & why it matters

Python is the default language for data work because of its ecosystem: NumPy for
arrays, pandas/Polars for tables, scikit-learn for ML, and a huge surrounding
community. ~90% of your day-to-day as a data scientist happens in Python, so
fluency here directly multiplies everything else you do.

The difference between a beginner and a strong practitioner isn't "knowing
pandas" — it's writing **vectorized, memory-aware, tested, reproducible** code
instead of slow loops in a fragile notebook.

---

## 🧠 Core concepts

- **NumPy** — n-dimensional arrays, broadcasting, vectorization (avoid Python
  loops; let C-level code do the work).
- **pandas** — `DataFrame`/`Series`, indexing (`loc`/`iloc`), `groupby`, joins
  (`merge`), reshaping (`pivot`/`melt`), `apply` vs vectorized ops.
- **Polars** — a modern, multi-threaded, lazy DataFrame library; much faster than
  pandas on medium/large data and increasingly popular.
- **Vectorization** — the single most important performance idea: operate on
  whole arrays, not element-by-element.
- **Clean code** — functions over copy-paste, type hints, virtual environments,
  and structure (see `data-science-training/modules/01-engineering-foundations.md`).

---

## 📚 Best resources

### Courses & videos
- **Krish Naik — Complete Python playlist** and the
  [Grand Complete Data Science Materials](https://github.com/krishnaik06/The-Grand-Complete-Data-Science-Materials)
  repo (free, comprehensive Python + DS foundations).
- **Corey Schafer — Python/pandas YouTube** — clear, practical Python tutorials.
- **Kaggle Learn — Python & pandas** micro-courses (hands-on, fast):
  https://www.kaggle.com/learn

### Books (free)
- **Python Data Science Handbook** — Jake VanderPlas (NumPy/pandas/sklearn):
  https://jakevdp.github.io/PythonDataScienceHandbook/
- **Effective Python** — Brett Slatkin (write better Python).

### Docs & tools
- pandas: https://pandas.pydata.org/docs/ · NumPy: https://numpy.org/doc/
- Polars: https://docs.pola.rs/ · uv (envs/packaging): https://github.com/astral-sh/uv

---

## 💻 Code example

```python
import numpy as np
import pandas as pd

# --- Vectorization: avoid Python loops ---
prices = np.array([100.0, 250.0, 75.0, 500.0])
discount = np.where(prices > 200, 0.10, 0.05)        # conditional, vectorized
final = prices * (1 - discount)                       # whole-array math
# final -> [ 95.  225.   71.25 450. ]

# --- pandas: the 5 operations you'll use daily ---
df = pd.DataFrame({
    "customer": ["A", "A", "B", "B", "C"],
    "region":   ["EU", "EU", "US", "US", "EU"],
    "revenue":  [100, 150, 200, 50, 300],
})

# 1. filter   2. group + aggregate   3. sort
summary = (
    df[df["revenue"] > 50]                       # filter
      .groupby("region", as_index=False)         # group
      .agg(total=("revenue", "sum"),
           customers=("customer", "nunique"))    # aggregate
      .sort_values("total", ascending=False)     # sort
)
print(summary)
#   region  total  customers
# 0     EU    550          2
# 1     US    200          1
```

---

## 🌍 Real-world use cases

- **Data cleaning & EDA** — the first step of every project; pandas does the heavy lifting.
- **Feature engineering** — turning raw tables into model-ready features.
- **ETL / data prep at scale** — Polars or PySpark when pandas runs out of memory.
- **Glue code** — connecting APIs, databases, and ML pipelines.

---

## 🛠️ Hands-on project ideas

1. Take a messy public CSV (e.g., a Kaggle dataset) and write a **reproducible
   cleaning pipeline** as pure, tested functions.
2. Re-implement a slow pandas `apply` loop as a **vectorized** version and
   benchmark the speedup.
3. Load a 5GB+ dataset with **Polars lazy mode** and compute aggregates that
   would OOM in pandas.

---

## 🗺️ Suggested learning path

1. Python basics → 2. NumPy (arrays, broadcasting) → 3. pandas (the daily 5:
filter, group, join, reshape, aggregate) → 4. Vectorization & performance →
5. Polars for scale → 6. Clean-code & environments
(`data-science-training/modules/01`).
