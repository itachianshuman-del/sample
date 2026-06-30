# 16 · Data Visualization & Storytelling

> Turning data into understanding. A chart's job isn't to look pretty — it's to
> make the right decision obvious. Communication is a senior-level multiplier.

---

## 📌 What it is & why it matters

Data visualization communicates patterns, comparisons, and uncertainty visually.
For a data scientist, it serves two jobs: **exploration** (understand your data
fast) and **explanation** (drive a decision with stakeholders). Brilliant analysis
that nobody understands has zero impact — viz is how impact happens.

---

## 🧠 Core concepts

- **Chart-to-question matching:** trend → line; comparison → bar; distribution →
  histogram/box; relationship → scatter; composition → stacked bar.
- **The grammar of graphics** — map data fields to visual channels (x, y, color, size).
- **Encoding hierarchy** — position is read most accurately; avoid pie charts and
  dual axes.
- **Show uncertainty** — error bars / confidence intervals, not just point estimates.
- **Storytelling:** one chart = one message; label with the takeaway; lead with
  the conclusion (BLUF); tailor to the audience (exec vs engineer vs analyst).
- **EDA vs presentation** — quick-and-dirty for yourself, polished for others.
- **Dashboards** — when to build one vs a one-off chart.

> Communication deep dive:
> [`data-science-training/modules/09-communication-and-leadership.md`](../../data-science-training/modules/09-communication-and-leadership.md).

---

## 📚 Best resources

### Books
- **Storytelling with Data** — Cole Nussbaumer Knaflic (the standard): https://www.storytellingwithdata.com/
- **The Visual Display of Quantitative Information** — Edward Tufte (classic).
- **Fundamentals of Data Visualization** — Claus Wilke (free online): https://clauswilke.com/dataviz/

### Tools & docs
- matplotlib: https://matplotlib.org/ · seaborn: https://seaborn.pydata.org/
- Plotly (interactive): https://plotly.com/python/ · Altair (declarative): https://altair-viz.github.io/
- BI: Tableau, Power BI, Looker, Metabase (open source).
- **Krish Naik — Data visualization / EDA** tutorials (free).
- **From Data to Viz** (pick the right chart): https://www.data-to-viz.com/

---

## 💻 Code example

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(data=tips, x="day", y="total_bill", hue="time",
            errorbar=("ci", 95), ax=ax)          # show the uncertainty (95% CI)

# Label with the TAKEAWAY, not just the axes — this is the senior habit.
ax.set_title("Dinner bills run higher than lunch, especially on weekends")
ax.set_xlabel(""); ax.set_ylabel("Avg bill ($)")
sns.despine()                                     # remove chart junk
plt.tight_layout()
# plt.savefig("bills_by_day.png", dpi=150)
```

---

## 🌍 Real-world use cases

- **Executive reporting** — one decision-driving chart, not a wall of numbers.
- **EDA** — spot outliers, distributions, and relationships before modeling.
- **Experiment results** — effect size + confidence intervals for ship decisions.
- **Self-serve dashboards** — KPIs stakeholders can monitor.

---

## 🛠️ Hands-on project ideas

1. Take a boring default chart and **redesign it** to make one message obvious.
2. Build an **interactive Plotly dashboard** for a dataset you care about.
3. Recreate a great chart from *Storytelling with Data* and write its one-line takeaway.

---

## 🗺️ Suggested learning path

1. matplotlib/seaborn basics → 2. Chart-to-question matching → 3. Encoding
principles & chart junk → 4. Showing uncertainty → 5. Storytelling (BLUF, audience)
→ 6. Interactive (Plotly) & dashboards.
