# 🧠 Data Science Learning Hub

A complete, hands-on resource for taking a data scientist from **intermediate
(~3 years experience) to senior** — combining a structured curriculum with a
deep, topic-organized reference library and **runnable code throughout**.

It's split into two complementary parts:

| Folder | What it is | Use it when... |
|---|---|---|
| 📘 [`data-science-training/`](./data-science-training/) | A **12-week curriculum** with modules, labs, assessments, and capstone projects | You want a guided, week-by-week program with deliverables |
| 📚 [`ds-resource-library/`](./ds-resource-library/) | A **topic-by-topic reference library** (16 topics) with curated resources + runnable examples | You want to learn or look up a specific topic (RAG, LLMs, MLOps, ...) |

> **The curriculum is the *route*; the library is the *map*.** Follow the
> curriculum for structure; dip into the library for depth on any topic.

---

## 📘 `data-science-training/` — the curriculum

A structured program built around the 6 pillars of a senior data scientist:
engineering discipline, statistical rigor, ML depth, production/MLOps,
GenAI/LLMs, and system design + communication.

- **[README](./data-science-training/README.md)** — start here (audience, pillars, how to use)
- **[INSTRUCTOR_GUIDE](./data-science-training/INSTRUCTOR_GUIDE.md)** — how to run it (solo / mentor / cohort)
- **[CURRICULUM](./data-science-training/CURRICULUM.md)** — the 12-week plan with weekly deliverables
- **[RESOURCES](./data-science-training/RESOURCES.md)** — the master curated resource list
- **[ASSESSMENTS](./data-science-training/ASSESSMENTS.md)** — rubrics + "are you senior yet?" checklist
- **`modules/`** — 9 deep-dive modules · **`hands-on/`** — 5 runnable, tested labs
- **`projects/`** — capstone briefs + doc templates · **`cheatsheets/`** — quick reference

---

## 📚 `ds-resource-library/` — the topic reference

16 topics, each in its own folder with the **same predictable structure**
(what & why → core concepts → best resources → code example → real-world use
cases → project ideas → learning path), plus a **runnable `example.py`**
(or `queries.sql`).

**Foundations:** [Python](./ds-resource-library/01-python-for-data-science/) ·
[SQL](./ds-resource-library/02-sql-and-databases/) ·
[Statistics](./ds-resource-library/03-statistics-and-probability/) ·
[Data Viz](./ds-resource-library/16-data-visualization/)

**Core ML:** [Machine Learning](./ds-resource-library/04-machine-learning/) ·
[Deep Learning](./ds-resource-library/05-deep-learning/) ·
[NLP](./ds-resource-library/06-nlp/) ·
[Computer Vision](./ds-resource-library/07-computer-vision/) ·
[Time Series](./ds-resource-library/08-time-series/)

**Generative AI:** [LLMs](./ds-resource-library/11-llm/) ·
[RAG](./ds-resource-library/12-rag/) ·
[Prompt Engineering](./ds-resource-library/13-prompt-engineering/) ·
[AI Agents](./ds-resource-library/14-ai-agents/)

**Production & Career:** [MLOps](./ds-resource-library/09-mlops/) ·
[Data Engineering](./ds-resource-library/10-data-engineering/) ·
[Interview Prep](./ds-resource-library/15-interview-prep/)

See the **[library index](./ds-resource-library/README.md)** for the full map.

---

## 🚀 Quick start (run the code)

Everything runs offline with a small, common stack. The GenAI examples use
mocks / TF-IDF so they need **no API keys**.

```bash
# 1. Environment
python -m venv .venv && source .venv/bin/activate
pip install -U pip

# 2. Core deps (covers most examples and the training labs)
pip install numpy pandas scikit-learn scipy matplotlib duckdb

# 3. Run a topic example
python ds-resource-library/04-machine-learning/example.py
python ds-resource-library/12-rag/example.py

# 4. Run a training lab
python data-science-training/hands-on/lab01_leakage_and_validation.py
```

Some examples are optional and need heavier libraries (clearly noted in-file):
- Deep Learning → `pip install torch`
- Computer Vision → `pip install ultralytics`
- Real embeddings / fine-tuning → `pip install sentence-transformers transformers`
- Time-series foundation models → `pip install statsforecast prophet`

---

## 🗺️ Suggested paths

- **Solidify fundamentals:** library 01 → 02 → 03 → 16 → 04
- **Go into GenAI:** library 04 → 05 → 06 → 11 → 13 → 12 → 14
- **Move toward production:** training Modules 5–8 + library 09 → 10 → 15
- **Full program:** follow `data-science-training/CURRICULUM.md` week by week

---

## 🌟 Curation & attribution

Resources are curated for **signal over volume** from world-class creators and
orgs — Krish Naik, Andrew Ng / DeepLearning.AI, Stanford (CS229, CS231n),
StatQuest, 3Blue1Brown, Andrej Karpathy, fast.ai, Hugging Face, dair-ai, Nixtla,
Ultralytics, and official docs — linked inline throughout.

> All external materials belong to their respective authors and are only
> *linked* here. Descriptions are paraphrased summaries written for this hub;
> code (labs and `example.py` files) was written for this project. Content was
> rephrased for compliance with licensing restrictions — always refer to the
> linked original for authoritative detail. Links and tool versions change over
> time; re-check periodically.
