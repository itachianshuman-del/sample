"""
Example — NLP (text classification, TF-IDF baseline)
====================================================
Runnable. Deps: numpy, scikit-learn

Before reaching for transformers, build the classic baseline:
TF-IDF + Logistic Regression. It's fast, strong, and interpretable -- and the
bar a fine-tuned transformer must beat to justify its cost.

Run: python example.py
"""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Tiny sentiment dataset (in practice: thousands of labeled examples).
texts = [
    "I love this product, it works perfectly",
    "Absolutely fantastic, exceeded expectations",
    "Great value and superb quality",
    "Wonderful experience, highly recommend",
    "Terrible, it broke after one day",
    "Awful quality, very disappointed",
    "Worst purchase I have ever made",
    "Completely useless and a waste of money",
]
labels = [1, 1, 1, 1, 0, 0, 0, 0]   # 1 = positive, 0 = negative

clf = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), stop_words="english")),
    ("lr", LogisticRegression()),
])
clf.fit(texts, labels)

tests = ["this is a fantastic and wonderful product",
         "useless and disappointed, broke immediately"]
preds = clf.predict(tests)
probs = clf.predict_proba(tests)[:, 1]

print("=" * 60)
for t, p, pr in zip(tests, preds, probs):
    label = "POSITIVE" if p == 1 else "NEGATIVE"
    print(f"[{label}  p(pos)={pr:.2f}]  {t}")
print("=" * 60)

# Interpretability: which words push toward 'positive'?
vec = clf.named_steps["tfidf"]
coefs = clf.named_steps["lr"].coef_[0]
vocab = vec.get_feature_names_out()
top = sorted(zip(coefs, vocab), reverse=True)[:5]
print("Top positive-signal tokens:", [w for _, w in top])
print("\nNext step: beat this with a fine-tuned DistilBERT (Hugging Face) and")
print("compare the accuracy gain against the extra cost/latency.")
