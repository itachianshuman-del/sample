# The Master Resource List

A curated, opinionated map of the **best** materials on the web for an
experienced data scientist leveling up. Every entry is here because it is
high-signal — widely respected, deep, and practical. Prefer **primary sources**
(the linked repos/books/courses) over secondary tutorials.

> Curation note: descriptions are paraphrased summaries written for this program.
> Always defer to the linked original for authoritative detail. Content was
> rephrased for compliance with licensing restrictions.

**How to read this file:** it mirrors the modules. Under each topic you'll find
🏛️ *Foundational* (timeless), 🔧 *Hands-on* (do this), 📚 *Reference* (look up),
and 📰 *Stay current* (blogs/feeds).

---

## 0. Prerequisite refresher (only if you're below the assumed bar)

- 🏛️ **Python Data Science Handbook** — Jake VanderPlas (free online): numpy,
  pandas, matplotlib, sklearn essentials. https://jakevdp.github.io/PythonDataScienceHandbook/
- 🔧 **Kaggle Learn** micro-courses (Python, pandas, SQL, intro ML): fast, hands-on. https://www.kaggle.com/learn
- 📚 **StatQuest (Josh Starmer)** — intuitive stats/ML video explanations. https://www.youtube.com/@statquest

---

## 1. Engineering foundations for data scientists

The discipline that makes your work survive contact with reality.

- 🏛️ **The Twelve-Factor App** — principles that apply to ML services too. https://12factor.net/
- 🔧 **Cookiecutter Data Science** — a sane, opinionated project structure. https://cookiecutter-data-science.drivendata.org/
- 🔧 **`uv`** — fast modern Python packaging/venv manager (Astral). https://github.com/astral-sh/uv
- 🔧 **`ruff`** — fast Python linter & formatter. https://github.com/astral-sh/ruff
- 🔧 **pytest** docs — testing for data/ML code. https://docs.pytest.org/
- 🔧 **pre-commit** — automated checks before every commit. https://pre-commit.com/
- 📚 **Effective Python** (Brett Slatkin) — 90 specific ways to write better Python.
- 📚 **Refactoring** (Martin Fowler) — when your notebook becomes a codebase.
- 📰 **Real Python** — consistently high-quality Python tutorials. https://realpython.com/

---

## 2. Statistics, experimentation & causal inference

This is where mid-level DS most often have gaps. Invest heavily here.

### Experimentation / A/B testing
- 🏛️ **Trustworthy Online Controlled Experiments** (Kohavi, Tang, Xu) — the
  definitive practitioner's book on A/B testing at scale. https://experimentguide.com/
- 🔧 **Eppo / Statsig / GrowthBook docs** — modern experimentation platforms;
  great free conceptual content on CUPED, sequential testing, guardrails.
  GrowthBook (open source): https://github.com/growthbook/growthbook
- 📰 **Netflix, Airbnb, Microsoft experimentation blogs** — read how the best
  teams actually run experiments (links via `eugeneyan/applied-ml` below).

### Causal inference
- 🏛️ **Causal Inference: The Mixtape** (Scott Cunningham, free online) — applied,
  code-driven. https://mixtape.scunning.com/
- 🏛️ **Causal Inference for The Brave and True** (Matheus Facure, free) — Python,
  hands-on, excellent. https://matheusfacure.github.io/python-causality-handbook/
- 🏛️ **Brady Neal — Introduction to Causal Inference** (free course + book). https://www.bradyneal.com/causal-inference-course
- 📚 **The Book of Why** (Judea Pearl) — the conceptual foundation of DAGs/causality.
- 🔧 **awesome-causal-inference** — curated list of books, courses, software.
  https://github.com/matteocourthoud/awesome-causal-inference
- 🔧 **DoWhy** (Microsoft) + **EconML** — causal inference libraries in Python.
  https://github.com/py-why/dowhy

### Core statistics
- 🏛️ **Statistical Rethinking** (Richard McElreath) — Bayesian thinking, with
  free lectures + code. https://github.com/rmcelreath/stat_rethinking_2024
- 📚 **Think Stats / Think Bayes** (Allen Downey, free) — practical, Python-based.
  https://greenteapress.com/wp/

---

## 3. Machine learning depth (beyond `model.fit()`)

- 🏛️ **The Elements of Statistical Learning** (Hastie, Tibshirani, Friedman, free
  PDF) — the rigorous reference. https://hastie.su.domains/ElemStatLearn/
  - Gentler companion: **An Introduction to Statistical Learning** (ISLP, Python
    edition, free). https://www.statlearning.com/
- 🔧 **scikit-learn User Guide** — read it cover to cover; it's a stats course in
  disguise. https://scikit-learn.org/stable/user_guide.html
- 🔧 **Feature Engineering & Selection** (Kuhn & Johnson, free online). http://www.feat.engineering/
- 🔧 **XGBoost / LightGBM / CatBoost** docs — gradient boosting is still the king
  of tabular data. https://xgboost.readthedocs.io/ · https://lightgbm.readthedocs.io/
- 🔧 **Optuna** — hyperparameter optimization done right. https://github.com/optuna/optuna
- 🔧 **SHAP** — model interpretability. https://github.com/shap/shap
- 🏛️ **Interpretable Machine Learning** (Christoph Molnar, free book). https://christophm.github.io/interpretable-ml-book/
- 🏛️ **Rules of Machine Learning** (Google / Martin Zinkevich) — 43 hard-won
  best practices for applied ML. https://developers.google.com/machine-learning/guides/rules-of-ml
- 🔧 **awesome-machine-learning** — the canonical curated ML library list.
  https://github.com/josephmisiti/awesome-machine-learning

---

## 4. Deep learning

- 🏛️ **Neural Networks: Zero to Hero** (Andrej Karpathy) — build backprop and a
  GPT from scratch, code-first. The single best deep-learning starting point for
  someone who wants real understanding. https://github.com/karpathy/nn-zero-to-hero
  - Course page: https://karpathy.ai/zero-to-hero.html
- 🏛️ **Practical Deep Learning for Coders** (fast.ai, Jeremy Howard) — top-down
  applied approach; ship models fast. https://course.fast.ai/
- 🏛️ **Dive into Deep Learning (d2l.ai)** — interactive book with code in
  PyTorch/JAX/TF. https://d2l.ai/
- 🔧 **PyTorch tutorials** — the framework that dominates research & increasingly
  industry. https://pytorch.org/tutorials/
- 📚 **Deep Learning** (Goodfellow, Bengio, Courville, free) — the theory reference.
  https://www.deeplearningbook.org/
- 📰 **The Illustrated Transformer** (Jay Alammar) — the clearest visual intro. https://jalammar.github.io/illustrated-transformer/

---

## 5. MLOps & production machine learning

- 🏛️ **Designing Machine Learning Systems** (Chip Huyen, O'Reilly) — the best
  single book on production ML end-to-end. Companion: https://github.com/chiphuyen/dmls-book
- 🏛️ **Machine Learning Systems Design** (Chip Huyen, free booklet + 27 design
  questions). https://github.com/chiphuyen/machine-learning-systems-design
- 🔧 **awesome-production-machine-learning** (EthicalML) — the definitive curated
  list of tools to deploy, monitor, version, and scale ML. https://github.com/EthicalML/awesome-production-machine-learning
- 🔧 **awesome-mlops** (kelvins) — curated MLOps tools & references. https://github.com/kelvins/awesome-mlops
- 🔧 **Made With ML** (Goku Mohandas) — free, end-to-end MLOps course with code.
  https://github.com/GokuMohandas/Made-With-ML
- 🔧 **MLflow** — experiment tracking + model registry. https://github.com/mlflow/mlflow
- 🔧 **Evidently** — ML monitoring & drift detection. https://github.com/evidentlyai/evidently
- 🔧 **DVC** — data & model versioning. https://github.com/iterative/dvc
- 🔧 **BentoML / FastAPI** — model serving. https://github.com/bentoml/BentoML
- 📰 **MLOps Community** — Slack + podcast + meetups. https://mlops.community/
- 🏛️ **Hidden Technical Debt in ML Systems** (Google/Sculley et al., paper) —
  required reading on why ML systems decay. (Search the title; NeurIPS 2015.)

---

## 6. LLMs & Generative AI

- 🏛️ **mlabonne/llm-course** — roadmaps + Colab notebooks split into "LLM
  Scientist" (training models) and "LLM Engineer" (building apps). The best free
  structured LLM curriculum. https://github.com/mlabonne/llm-course
- 🔧 **LLM Engineer's Handbook** (curated list, SylphAI) — training, serving,
  fine-tuning, app-building resources. https://github.com/SylphAI-Inc/LLM-engineer-handbook
- 🔧 **awesome-llmops** (KennethanCeyer) — LLMOps tooling. https://github.com/KennethanCeyer/awesome-llmops
- 🏛️ **Hugging Face — LLM Course / NLP Course** (free). https://huggingface.co/learn
- 🔧 **LangChain / LlamaIndex docs** — RAG & agent frameworks (learn concepts,
  the APIs change fast). https://python.langchain.com/ · https://docs.llamaindex.ai/
- 🔧 **RAG evaluation: Ragas** — metrics for retrieval-augmented systems.
  https://github.com/explodinggradients/ragas
- 🔧 **PEFT / LoRA** (Hugging Face) — parameter-efficient fine-tuning. https://github.com/huggingface/peft
- 📰 **Chip Huyen's blog** (e.g., RLHF, LLM evaluation, AI engineering). https://huyenchip.com/blog/
- 📰 **Lilian Weng's blog (Lil'Log)** — deep, authoritative posts on LLMs/agents.
  https://lilianweng.github.io/
- 📚 **AI Engineering** (Chip Huyen, 2025) — the production-LLM successor to DMLS.

---

## 7. Data engineering for data scientists

You don't need to be a data engineer, but you must speak the language.

- 🏛️ **Fundamentals of Data Engineering** (Reis & Housley) — the conceptual map.
- 🔧 **awesome-data-engineering** (igorbarinov) — curated tools list. https://github.com/igorbarinov/awesome-data-engineering
- 🔧 **dbt** — analytics engineering / SQL transformations. https://github.com/dbt-labs/dbt-core
- 🔧 **Apache Airflow** — orchestration. https://github.com/apache/airflow
- 🔧 **Apache Spark / PySpark** — distributed processing. https://spark.apache.org/docs/latest/api/python/
- 🔧 **DuckDB** — blazing-fast local analytics SQL; a DS superpower. https://duckdb.org/
- 🔧 **Polars** — fast DataFrames, a modern pandas alternative. https://github.com/pola-rs/polars
- 🔧 **SQL practice**: DataLemur (https://datalemur.com/) and StrataScratch for
  realistic DS SQL interview questions.

---

## 8. ML system design

- 🏛️ **chiphuyen/machine-learning-systems-design** — framework + 27 open-ended
  design questions. https://github.com/chiphuyen/machine-learning-systems-design
- 🔧 **machine-learning-interview** (Khang Pham) — FAANG-style ML system design
  + prep, from someone with multiple big-tech offers. https://github.com/khangich/machine-learning-interview
- 🏛️ **System Design Primer** — general system design foundations (apply to ML).
  https://github.com/donnemartin/system-design-primer
- 📚 **eugeneyan/applied-ml** — real company write-ups of ML in production,
  organized by problem type. Study how real systems are designed. https://github.com/eugeneyan/applied-ml
- 📰 **Eugene Yan's blog** — exceptional applied ML / recsys / LLM-in-prod essays.
  https://eugeneyan.com/

---

## 9. Interview & career prep (for the next level)

- 🔧 **Introduction to Machine Learning Interviews** (Chip Huyen, free book). https://huyenchip.com/ml-interviews-book/
- 🔧 **chiphuyen/ml-interviews-book** (source). https://github.com/chiphuyen/ml-interviews-book
- 🔧 **Data-Science-Interview-Resources** (rbhatia46) — broad curated prep list.
  https://github.com/rbhatia46/Data-Science-Interview-Resources
- 🔧 **machine-learning-interview** (khangich) — see Section 8.
- 🔧 **Ace the Data Science Interview** (book) + DataLemur for SQL/stats drills.

---

## 10. Portfolio & guided projects

- 🔧 **Awesome-AI-Data-Guided-Projects** (Youssef Hosni) — curated guided
  projects to build a portfolio. https://github.com/youssefHosni/Awesome-AI-Data-Guided-Projects
- 🔧 **Kaggle** — competitions + datasets + public notebooks (read winners'
  solutions; they're a masterclass). https://www.kaggle.com/
- 🔧 **Papers with Code** — SOTA + reproducible implementations. https://paperswithcode.com/
- 🔧 **Hugging Face Datasets & Spaces** — data + deployable demos. https://huggingface.co/

---

## 11. Staying current (build a reading habit)

- 📰 **Newsletters:** The Batch (DeepLearning.AI), Data Elixir, Import AI, TLDR AI,
  Sebastian Raschka's "Ahead of AI."
- 📰 **Blogs:** Chip Huyen, Eugene Yan, Lilian Weng, Sebastian Raschka, Jay Alammar,
  Netflix/Airbnb/Uber/Spotify engineering blogs.
- 📰 **Papers:** skim arXiv cs.LG / cs.CL weekly; use Papers with Code trending.
- 📰 **Communities:** MLOps Community, r/MachineLearning, local ML meetups.

---

## How to not drown in this list

You do **not** read all of this. The curriculum (`CURRICULUM.md`) tells you
*exactly* what to use each week. This file is the map; the curriculum is the
route. Pick the foundational resource for your current module, do the lab, and
only go deeper when a real problem demands it.

> "Don't collect resources. Finish one, ship something, move on."
