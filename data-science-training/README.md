# Data Science Mastery Track — Intermediate → Senior

> A structured, hands-on training program designed to take a data scientist with
> **~3 years of experience** (solid company + personal projects) to a **senior /
> staff-level** practitioner who can own ML systems end-to-end in production.

This is **not** a beginner course. It assumes you already know Python, pandas,
scikit-learn, basic SQL, and have shipped at least a couple of models or
analyses. The goal here is to close the gaps that separate a competent IC from a
senior data scientist: **rigorous experimentation, production ML, system design,
modern GenAI/LLMs, and the engineering discipline that makes your work durable.**

---

## Who this is for

| You already... | This program adds... |
|---|---|
| Train models in notebooks | Ship them as monitored, versioned services |
| Run `train_test_split` and check accuracy | Design experiments, reason about causality, and avoid leakage |
| Use pandas/sklearn fluently | Write tested, packaged, reproducible Python |
| Know what a transformer "is" | Build, fine-tune, evaluate, and serve LLM apps |
| Answer "which model is best?" | Answer "what should we build, and how do we know it worked?" |

If most of the left column sounds like you, this track is calibrated correctly.

---

## How this repository is organized

```
data-science-training/
├── README.md              ← you are here (start here)
├── INSTRUCTOR_GUIDE.md    ← context for the trainer/mentor + how to run the program
├── CURRICULUM.md          ← the 12-week structured plan, week by week
├── RESOURCES.md           ← the master curated resource list (books, courses, repos, papers, blogs)
├── ASSESSMENTS.md         ← checkpoints, rubrics, and "are you senior yet?" self-tests
├── modules/               ← deep-dive notes per topic (the "what to learn & why")
│   ├── 01-engineering-foundations.md
│   ├── 02-statistics-and-experimentation.md
│   ├── 03-machine-learning-deep-dive.md
│   ├── 04-deep-learning.md
│   ├── 05-mlops-and-production.md
│   ├── 06-llms-and-genai.md
│   ├── 07-data-engineering-for-ds.md
│   ├── 08-ml-system-design.md
│   └── 09-communication-and-leadership.md
├── hands-on/              ← runnable Python labs you complete and extend
│   ├── README.md
│   ├── lab01_leakage_and_validation.py
│   ├── lab02_feature_engineering_pipeline.py
│   ├── lab03_ab_test_analysis.py
│   ├── lab04_model_monitoring.py
│   └── lab05_rag_from_scratch.py
├── projects/              ← portfolio-grade capstone briefs
│   └── README.md
└── cheatsheets/           ← dense quick-reference material
    └── README.md
```

**Reading order:** `README.md` → `INSTRUCTOR_GUIDE.md` → `CURRICULUM.md`, then
work module-by-module, doing the matching `hands-on/` lab and dipping into
`RESOURCES.md` for depth. Use `ASSESSMENTS.md` at each checkpoint.

---

## The 6 pillars of a senior data scientist

This program is built around the skills that actually differentiate senior ICs.
Each maps to one or more modules.

1. **Engineering discipline** — reproducibility, testing, packaging, Git, envs. *(Module 1, 7)*
2. **Statistical rigor & causality** — experimentation, inference, decision-making under uncertainty. *(Module 2)*
3. **ML depth** — beyond `model.fit()`: validation, imbalanced data, calibration, interpretability. *(Module 3, 4)*
4. **Production & MLOps** — serving, monitoring, drift, retraining, CI/CD for ML. *(Module 5)*
5. **GenAI / LLMs** — RAG, fine-tuning, evaluation, agents, cost & latency. *(Module 6)*
6. **System design & communication** — scoping problems, designing ML systems, influencing decisions. *(Module 8, 9)*

---

## How to use the labs

```bash
# 1. Create an isolated environment (uv is fast; venv/conda also fine)
python -m venv .venv && source .venv/bin/activate
pip install -U pip

# 2. Install the lab dependencies
pip install numpy pandas scikit-learn matplotlib scipy statsmodels \
            xgboost lightgbm shap mlflow evidently sentence-transformers

# 3. Run a lab
python hands-on/lab01_leakage_and_validation.py
```

Each lab is self-contained, uses synthetic or openly-available data, prints
explanatory output, and ends with **"Extend this"** challenges. Don't just run
them — break them, modify them, and explain the output to someone else.

---

## Progress tracking

Use `ASSESSMENTS.md`. The rule of thumb: **you don't "know" a module until you
can teach it and ship something with it.** Every module ends with a deliverable
you can put in a portfolio or your work repo.

---

## A note on philosophy

Tools change every 18 months; fundamentals don't. This track deliberately
balances **timeless fundamentals** (statistics, validation, system design) with
**current tooling** (LLMs, modern MLOps). When a tool is mentioned, the
*concept* it represents matters more than the specific library — learn the
concept, then the tool is interchangeable.

> "The hard part of machine learning isn't the modeling — it's everything
> around it: the data, the experiments, the deployment, and knowing whether you
> actually solved the problem."

Let's get to work. Open `INSTRUCTOR_GUIDE.md` next.
