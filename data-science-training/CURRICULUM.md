# The 12-Week Curriculum

A week-by-week plan. Each week lists: **focus**, **core resources** (full links
in `RESOURCES.md`), the **hands-on lab**, and the **deliverable** that proves you
learned it. Weeks are ~10 hrs each.

> Legend: 📖 read/watch · 🧪 lab · 🚢 deliverable · 🤔 thinking questions

---

## Phase 1 — Engineering & Statistical Foundations (Weeks 1–3)

### Week 1 — Engineering discipline for data scientists
The thing that most separates a senior from a mid-level DS is not modeling — it's
that their work is **reproducible, tested, and shippable**.

- 📖 Module `01-engineering-foundations.md`
- 📖 Topics: project structure, virtual envs (`uv`/`venv`/`conda`), dependency
  pinning, `pyproject.toml`, type hints, `ruff`/`black`, `pytest` for data code,
  Git branching, pre-commit hooks, Makefiles, config management.
- 🧪 None (setup week) — but convert one of *your own* past notebooks into a
  packaged, tested module.
- 🚢 **Deliverable:** a past project refactored into a installable package with
  `pyproject.toml`, at least 5 unit tests, a `README`, and CI that runs them.
- 🤔 Why do notebooks rot? What makes an analysis reproducible 6 months later?

### Week 2 — Statistics & inference you actually need
- 📖 Module `02-statistics-and-experimentation.md` (sections 1–4)
- 📖 Topics: sampling distributions, CLT, confidence intervals, hypothesis
  testing pitfalls, p-value misuse, multiple comparisons, bootstrap, power.
- 🧪 `lab03_ab_test_analysis.py` (part 1: power & sample size)
- 🚢 **Deliverable:** a notebook that, given an effect size and baseline,
  computes required sample size and runs a bootstrap CI on a real dataset.
- 🤔 What's the difference between statistical and practical significance?

### Week 3 — Experimentation & causal inference
- 📖 Module `02-statistics-and-experimentation.md` (sections 5–8)
- 📖 Topics: A/B test design, randomization, CUPED, sequential testing, peeking,
  Simpson's paradox, intro to causal inference (potential outcomes, DAGs,
  confounding, diff-in-diff).
- 🧪 `lab03_ab_test_analysis.py` (part 2: full experiment analysis)
- 🚢 **Deliverable:** a complete A/B test write-up — design, guardrail metrics,
  analysis, and a clear ship / no-ship recommendation with caveats.
- 🤔 When can you NOT run an A/B test, and what do you do instead?

---

## Phase 2 — Machine Learning Depth (Weeks 4–6)

### Week 4 — ML done rigorously
- 📖 Module `03-machine-learning-deep-dive.md` (sections 1–5)
- 📖 Topics: leakage (the #1 silent killer), proper CV for time-series/grouped
  data, target leakage vs train-test contamination, baselines, metric selection,
  threshold tuning, calibration.
- 🧪 `lab01_leakage_and_validation.py`
- 🚢 **Deliverable:** take a Kaggle/your dataset; build a leakage-free pipeline,
  pick the right CV scheme, and justify your metric choice in writing.
- 🤔 Name three ways leakage sneaks in that pass a naive train/test split.

### Week 5 — Feature engineering & tabular mastery
- 📖 Module `03-machine-learning-deep-dive.md` (sections 6–9)
- 📖 Topics: encoding strategies, target encoding done safely, feature stores,
  gradient boosting deep dive (XGBoost/LightGBM/CatBoost), hyperparameter
  optimization (Optuna), handling imbalance.
- 🧪 `lab02_feature_engineering_pipeline.py`
- 🚢 **Deliverable:** an sklearn `Pipeline` + `ColumnTransformer` that is fully
  reproducible end-to-end, tuned with Optuna, with a model card.
- 🤔 Why is target encoding dangerous, and how do you do it without leakage?

### Week 6 — Interpretability, fairness & robustness
- 📖 Module `03-machine-learning-deep-dive.md` (sections 10–12)
- 📖 Topics: SHAP, permutation importance, partial dependence, error analysis,
  model fairness basics, robustness/stress testing, drift-readiness.
- 🧪 Extend `lab02` with a SHAP analysis + error slice analysis.
- 🚢 **Deliverable:** an interpretability report for your Week 5 model: global +
  local explanations, worst error slices, and fairness check across a subgroup.
- 🤔 A stakeholder asks "why did the model reject this customer?" — answer it.

---

## Phase 3 — Deep Learning & GenAI (Weeks 7–9)

### Week 7 — Deep learning foundations (from scratch)
- 📖 Module `04-deep-learning.md`
- 📖 Core: **Karpathy's Neural Networks: Zero to Hero** (build backprop + a
  GPT from scratch). Then `fast.ai` Practical Deep Learning for the applied view.
- 🧪 Implement micrograd-style autodiff (follow Karpathy), then train a small net.
- 🚢 **Deliverable:** a from-scratch neural net (no autograd framework) that
  learns a non-trivial function, plus a written explanation of backprop.
- 🤔 Why does batch norm help? What actually happens during backprop?

### Week 8 — LLMs: using, prompting, and RAG
- 📖 Module `06-llms-and-genai.md` (sections 1–5)
- 📖 Core: **mlabonne/llm-course** (LLM Engineer track), RAG fundamentals.
- 🧪 `lab05_rag_from_scratch.py` (embeddings → retrieval → grounded generation)
- 🚢 **Deliverable:** a working RAG system over a document corpus you choose,
  with an evaluation harness (retrieval hit-rate + answer quality).
- 🤔 When does RAG beat fine-tuning, and vice versa? How do you evaluate RAG?

### Week 9 — LLMs: fine-tuning, evaluation & agents
- 📖 Module `06-llms-and-genai.md` (sections 6–10)
- 📖 Topics: SFT, LoRA/QLoRA, preference tuning intuition, evaluation
  (LLM-as-judge, benchmarks, regression suites), agents & tool use, cost/latency.
- 🧪 Fine-tune a small open model with LoRA on a focused task (Colab/GPU).
- 🚢 **Deliverable:** a fine-tuned model OR a rigorous eval report comparing
  prompt-engineering vs RAG vs fine-tuning for one concrete task.
- 🤔 How do you stop an LLM feature from silently regressing in production?

---

## Phase 4 — Production, Systems & Influence (Weeks 10–12)

### Week 10 — MLOps & production ML
- 📖 Module `05-mlops-and-production.md`
- 📖 Topics: experiment tracking (MLflow), model registry, packaging & serving
  (FastAPI, batch vs online), containerization, CI/CD for ML, reproducible
  pipelines, feature/serving skew.
- 🧪 `lab04_model_monitoring.py` + wrap your Week 5 model in a FastAPI service.
- 🚢 **Deliverable:** a containerized model service with a `/predict` endpoint,
  logged experiments, and a model registry entry. Bonus: deploy it.
- 🤔 What's training/serving skew and how do you detect it before users do?

### Week 11 — Monitoring, drift & ML system design
- 📖 Module `08-ml-system-design.md` + `05` (monitoring sections)
- 📖 Core: **Chip Huyen — Designing Machine Learning Systems** framework.
- 🧪 Extend `lab04` with drift detection (Evidently) + alerting logic.
- 🚢 **Deliverable:** a full ML system design doc for a realistic problem (e.g.,
  recommendation, fraud, churn) — covering data, features, model, serving,
  monitoring, and failure modes. Use the template in the module.
- 🤔 How would you design a system to detect when your model should be retrained?

### Week 12 — Communication, leadership & the capstone
- 📖 Module `09-communication-and-leadership.md`
- 📖 Topics: structured problem scoping, stakeholder management, writing
  decision docs, presenting results, mentoring, driving technical direction.
- 🧪 Present your capstone to a (real or simulated) stakeholder audience.
- 🚢 **Capstone deliverable:** pick one project from `projects/README.md` and
  ship it end-to-end: problem framing → data → model → eval → service →
  monitoring → a written decision doc + a 10-minute presentation.
- 🤔 Could a PM read your decision doc and make the right call without you?

---

## After Week 12

- Do a mock senior-DS / ML-engineer interview loop (system design + stats +
  coding + behavioral). Resources in `RESOURCES.md` → Interview prep.
- Pick a specialization to go deep: GenAI/LLM systems, ML platform/MLOps,
  causal inference & experimentation, or applied research.
- Contribute to one open-source repo from `RESOURCES.md`. Real review = growth.

See `ASSESSMENTS.md` for the "are you senior yet?" checklist.
