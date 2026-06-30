# Module 1 — Engineering Foundations for Data Scientists

> **Why this is module 1:** The biggest gap between a mid-level and senior data
> scientist is rarely modeling skill. It's that the senior's work is
> **reproducible, tested, packaged, and shippable**. A brilliant analysis that
> nobody can rerun is worth less than a decent one that's bulletproof.

**Outcome:** you can turn any notebook into a tested, installable, reproducible
package that a teammate can run in one command.

---

## 1. The notebook ceiling (and how to break it)

Notebooks are great for exploration and terrible for production:
- Hidden state (cells run out of order) → "works on my machine."
- No tests → silent breakage when data or deps change.
- Hard to diff, review, and reuse.

**The senior move:** explore in a notebook, then *graduate* the keepers into
`.py` modules with functions, type hints, and tests. The notebook becomes a thin
orchestration layer or gets deleted.

> Rule of thumb: if a piece of code will run more than 3 times or be touched by
> more than 1 person, it belongs in a tested module, not a notebook cell.

---

## 2. Project structure

A predictable layout reduces cognitive load. A good default:

```
project/
├── pyproject.toml          # deps + build config (single source of truth)
├── README.md
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── data.py         # loading, validation
│       ├── features.py     # feature engineering (pure functions)
│       ├── model.py        # train / predict
│       └── config.py       # typed config
├── tests/
│   ├── test_features.py
│   └── test_model.py
├── notebooks/              # exploration only; not imported by src
├── data/                   # gitignored; use DVC/remote storage
└── Makefile                # `make test`, `make lint`, `make train`
```

Use **Cookiecutter Data Science** as a starting template (see RESOURCES §1).

---

## 3. Environments & dependency management

Reproducibility starts with pinned dependencies.

- **`uv`** (recommended, fast) or `venv`/`conda`. Avoid system Python.
- Declare deps in **`pyproject.toml`**, pin exact versions in a lockfile.
- Separate runtime deps from dev deps (`pytest`, `ruff`, etc.).

```toml
# pyproject.toml (minimal)
[project]
name = "churn-model"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["scikit-learn>=1.4", "pandas>=2.2", "numpy>=1.26"]

[project.optional-dependencies]
dev = ["pytest>=8", "ruff>=0.5", "mypy>=1.10"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

**Why it matters:** "it worked last quarter" is not reproducibility. A lockfile
+ a pinned Python version is.

---

## 4. Clean, typed, testable code

- **Type hints** everywhere in `src/`. Run `mypy` or `pyright`.
- Write **pure functions** for feature logic (same input → same output, no I/O).
  Pure functions are trivially testable.
- Keep I/O (reading files, DB, network) at the edges, separate from logic.

```python
# Good: pure, typed, testable
def add_recency_features(df: pd.DataFrame, now: pd.Timestamp) -> pd.DataFrame:
    out = df.copy()
    out["days_since_signup"] = (now - out["signup_date"]).dt.days
    return out
```

---

## 5. Testing data & ML code

You can't unit-test "is the model good" (that's evaluation), but you *can* test:
- **Feature logic** — known input → known output.
- **Data contracts** — schema, ranges, nullability (use `pandera` or
  `great_expectations`).
- **Pipeline shape** — output columns/shape are as expected.
- **Determinism** — same seed → same result.
- **Edge cases** — empty df, all-null column, single row.

```python
def test_add_recency_features():
    df = pd.DataFrame({"signup_date": [pd.Timestamp("2024-01-01")]})
    out = add_recency_features(df, now=pd.Timestamp("2024-01-11"))
    assert out["days_since_signup"].iloc[0] == 10
```

---

## 6. Git & collaboration hygiene

- Small, focused commits with meaningful messages.
- Branch per change; PRs with description + how you tested.
- **`.gitignore`** data, secrets, `.venv`, checkpoints. Never commit credentials.
- **pre-commit** hooks to auto-run `ruff` + tests before commit.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks: [{id: ruff}, {id: ruff-format}]
```

---

## 7. Reproducibility checklist

- [ ] Pinned Python version + lockfile
- [ ] Fixed random seeds (numpy, sklearn, torch) — and you know which ops are
      still nondeterministic (e.g., some GPU kernels)
- [ ] Data versioned (DVC or immutable snapshot + hash)
- [ ] Config in files, not hardcoded in code
- [ ] One command to reproduce (`make train` / a script)
- [ ] Results logged (MLflow) so you can compare runs

---

## Thinking questions
1. Why do notebooks "rot"? List 3 concrete failure modes.
2. What's the difference between a unit test and model evaluation? Which catches
   a feature bug?
3. Your model gave different results today than last week with "the same code."
   List 5 possible causes.

## Deliverable
Refactor one of your past projects into an installable package: `pyproject.toml`,
`src/` layout, ≥5 unit tests, a `Makefile`, pre-commit, and CI (GitHub Actions)
that runs lint + tests. One command should reproduce your main result.

## Go deeper
RESOURCES §1 (Engineering foundations). Especially Cookiecutter DS, `uv`, `ruff`,
pytest docs, and *Effective Python*.
