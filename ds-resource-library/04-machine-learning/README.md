# 04 · Machine Learning

> Teaching computers to find patterns and make predictions from data. The core
> craft of the field — and gradient boosting is still the king of tabular data.

---

## 📌 What it is & why it matters

Machine learning builds models that learn patterns from data to predict or decide
without being explicitly programmed. It powers recommendations, fraud detection,
pricing, churn prediction, forecasting, and more. For the vast majority of
business problems (which are *tabular*), classical ML — especially gradient
boosting — outperforms deep learning while being cheaper and more interpretable.

---

## 🧠 Core concepts

- **Learning types:** supervised (regression, classification), unsupervised
  (clustering, dimensionality reduction), reinforcement learning.
- **The workflow:** problem framing → data prep → feature engineering → model →
  evaluation → tuning → deployment.
- **Key algorithms:** linear/logistic regression, decision trees, random forests,
  **gradient boosting (XGBoost, LightGBM, CatBoost)**, SVM, k-NN, k-means, PCA.
- **Validation done right:** train/val/test, cross-validation schemes that match
  deployment, and avoiding **data leakage** (the #1 silent killer).
- **Metrics:** accuracy, precision/recall, F1, ROC-AUC vs **PR-AUC**, RMSE/MAE,
  calibration. Pick the metric the *business* cares about.
- **The bias-variance tradeoff**, overfitting/underfitting, regularization.
- **Feature engineering, hyperparameter tuning (Optuna), interpretability (SHAP).**

> Deep dive + labs:
> [`data-science-training/modules/03-machine-learning-deep-dive.md`](../../data-science-training/modules/03-machine-learning-deep-dive.md),
> `hands-on/lab01_leakage_and_validation.py`, `lab02_feature_engineering_pipeline.py`.

---

## 📚 Best resources

### Courses
- **Andrew Ng — Machine Learning Specialization** (DeepLearning.AI + Stanford,
  Coursera) — the classic starting point: https://www.coursera.org/specializations/machine-learning-introduction
- **Stanford CS229** (rigorous, free materials): https://cs229.stanford.edu/
- **Krish Naik — Complete ML playlist** + the
  [Machine-Learning-Algorithms-Materials](https://github.com/krishnaik06/Machine-Learning-Algorithms-Materials)
  and [Complete DS+ML+NLP 2024](https://github.com/krishnaik06/Complete-Data-Science-With-Machine-Learning-And-NLP-2024) repos.

### Videos for intuition
- **StatQuest** — every ML algorithm explained simply: https://www.youtube.com/@statquest

### Books (free)
- **An Introduction to Statistical Learning (ISLP, Python)** — the best applied
  ML book, free: https://www.statlearning.com/
- **Hands-On Machine Learning** (Aurélien Géron) — the practitioner's bible (paid).
- **Google — Rules of Machine Learning** (43 best practices):
  https://developers.google.com/machine-learning/guides/rules-of-ml

### Tools
- scikit-learn: https://scikit-learn.org/ · XGBoost: https://xgboost.readthedocs.io/
- LightGBM: https://lightgbm.readthedocs.io/ · Optuna: https://github.com/optuna/optuna

---

## 💻 Code example

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import HistGradientBoostingClassifier

X, y = make_classification(n_samples=5000, n_features=20,
                           weights=[0.9, 0.1], random_state=0)  # imbalanced

# Everything inside a Pipeline -> no leakage; CV matches deployment.
pipe = Pipeline([
    ("scale", StandardScaler()),
    ("clf", HistGradientBoostingClassifier(learning_rate=0.05, max_iter=300)),
])

cv = StratifiedKFold(5, shuffle=True, random_state=0)
# PR-AUC (average_precision) is the right metric for rare positives.
scores = cross_val_score(pipe, X, y, cv=cv, scoring="average_precision")
print(f"PR-AUC: {scores.mean():.3f} +/- {scores.std():.3f}")
```

---

## 🌍 Real-world use cases

- **Churn / propensity** — who will cancel, who will convert (and what to do about it).
- **Fraud & anomaly detection** — imbalanced classification, real-time scoring.
- **Demand forecasting & pricing** — regression with business cost models.
- **Recommendations & ranking** — what to show next.
- **Credit scoring & risk** — interpretable, regulated models.

---

## 🛠️ Hands-on project ideas

1. End-to-end **churn model**: leak-free pipeline, right metric, SHAP explanation,
   threshold from a cost model.
2. **Kaggle Playground** competition — practice feature engineering + tuning.
3. Compare **XGBoost vs LightGBM vs CatBoost** on a tabular dataset and explain
   the differences.

---

## 🗺️ Suggested learning path

1. Linear/logistic regression → 2. Trees & random forests → 3. Gradient boosting
→ 4. Validation & leakage → 5. Metrics & thresholds → 6. Feature engineering →
7. Tuning (Optuna) & interpretability (SHAP) → 8. Unsupervised (k-means, PCA).
