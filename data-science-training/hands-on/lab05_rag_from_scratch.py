"""
Lab 05 — RAG From Scratch (no framework)
========================================
Module 6 | Curriculum Week 8

GOAL
----
Build the entire Retrieval-Augmented Generation pipeline by hand so every piece
is transparent:
  1. chunk documents,
  2. embed chunks,
  3. retrieve top-k by cosine similarity (vector) + keyword (BM25-ish) = HYBRID,
  4. build a grounded prompt with citations,
  5. EVALUATE retrieval (hit-rate / MRR) -- the step most teams skip.

We DON'T call a paid LLM. Generation is mocked so the lab runs offline and free;
the focus is the retrieval + evaluation machinery, which is where RAG succeeds or
fails. If `sentence-transformers` is installed it's used for real embeddings;
otherwise a deterministic hashing embedding is used as a fallback.

Run:  python lab05_rag_from_scratch.py
Deps: numpy   (optional: sentence-transformers for real embeddings)
"""

from __future__ import annotations

import re
from collections import Counter

import numpy as np

# ---------------------------------------------------------------------------
# A tiny knowledge base. In real life: your docs, chunked from PDFs/markdown/etc.
# ---------------------------------------------------------------------------
DOCS = {
    "doc_psi": "Population Stability Index (PSI) measures how much a distribution "
    "has shifted from a baseline. PSI below 0.1 means stable, 0.1 to 0.25 is a "
    "moderate shift, and above 0.25 signals a major shift requiring action.",
    "doc_leakage": "Data leakage happens when information unavailable at prediction "
    "time leaks into training, producing optimistic offline metrics. Fix it by "
    "fitting all transforms inside a pipeline and choosing a CV scheme that matches "
    "deployment.",
    "doc_cuped": "CUPED reduces variance in an A/B test by using a pre-experiment "
    "covariate correlated with the outcome, achieving the same statistical power "
    "with less traffic.",
    "doc_drift": "Concept drift is when the relationship between inputs and the "
    "target changes over time. It is dangerous because input distributions can look "
    "stable while model accuracy silently degrades.",
    "doc_calibration": "A model can rank well yet output miscalibrated "
    "probabilities. Use Platt scaling or isotonic regression and check a "
    "reliability diagram when decisions depend on the probability value.",
}

# Evaluation set: question -> the doc id that SHOULD be retrieved.
EVAL = [
    ("What PSI value indicates a major distribution shift?", "doc_psi"),
    ("How do I prevent data leakage in a model?", "doc_leakage"),
    ("How can I reduce variance in an experiment?", "doc_cuped"),
    ("Why is concept drift hard to detect?", "doc_drift"),
    ("My probabilities are unreliable, what do I do?", "doc_calibration"),
]


def banner(t: str) -> None:
    print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)


# ---------------------------------------------------------------------------
# Embeddings: real (sentence-transformers) if available, else a hashing fallback.
# ---------------------------------------------------------------------------
def get_embedder():
    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("[embeddings] using sentence-transformers all-MiniLM-L6-v2")
        return lambda texts: np.asarray(model.encode(list(texts), normalize_embeddings=True))
    except Exception:
        print("[embeddings] sentence-transformers not found -> hashing fallback")
        print("             (install it for real semantic search: pip install sentence-transformers)")
        return _hashing_embedder(dim=256)


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _hashing_embedder(dim: int):
    def embed(texts):
        vecs = np.zeros((len(texts), dim))
        for i, t in enumerate(texts):
            for tok in _tokenize(t):
                vecs[i, hash(tok) % dim] += 1.0
        # L2 normalize so dot product == cosine similarity.
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        return vecs / np.clip(norms, 1e-9, None)

    return embed


# ---------------------------------------------------------------------------
# Lexical scoring (BM25-ish): keyword overlap. Complements dense embeddings.
# ---------------------------------------------------------------------------
def bm25_scores(query: str, doc_tokens: dict[str, list[str]]) -> dict[str, float]:
    q = _tokenize(query)
    scores = {}
    for did, toks in doc_tokens.items():
        counts = Counter(toks)
        scores[did] = float(sum(counts[w] for w in q))
    # Normalize to 0-1 for fair fusion with cosine.
    mx = max(scores.values()) or 1.0
    return {k: v / mx for k, v in scores.items()}


def main() -> None:
    banner("STEP 1-2 — chunk (already chunked here) and embed the knowledge base")
    embed = get_embedder()
    doc_ids = list(DOCS)
    doc_texts = [DOCS[d] for d in doc_ids]
    doc_emb = embed(doc_texts)
    doc_tokens = {d: _tokenize(DOCS[d]) for d in doc_ids}
    print(f"Indexed {len(doc_ids)} chunks.")

    def retrieve(query: str, k: int = 2, alpha: float = 0.5):
        """HYBRID retrieval: alpha * cosine(dense) + (1-alpha) * lexical."""
        q_emb = embed([query])[0]
        cos = {d: float(np.dot(q_emb, doc_emb[i])) for i, d in enumerate(doc_ids)}
        lex = bm25_scores(query, doc_tokens)
        fused = {d: alpha * cos[d] + (1 - alpha) * lex[d] for d in doc_ids}
        ranked = sorted(fused, key=fused.get, reverse=True)
        return ranked[:k], fused

    banner("STEP 3-4 — retrieve + build a grounded, cited prompt")
    q = EVAL[0][0]
    top, _ = retrieve(q, k=2)
    context = "\n".join(f"[{i+1}] ({d}) {DOCS[d]}" for i, d in enumerate(top))
    prompt = (
        "Answer ONLY from the context. Cite sources like [1]. "
        "If the answer isn't present, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {q}\nAnswer:"
    )
    print("Example grounded prompt sent to the LLM:\n")
    print(prompt)
    print("\n[mock LLM answer] A PSI above 0.25 signals a major shift [1].")

    banner("STEP 5 — EVALUATE retrieval (the step teams skip)")
    # hit-rate@k: did the correct doc make the top-k?  MRR: how high did it rank?
    def evaluate(k=2, alpha=0.5):
        hits, rr = 0, 0.0
        for question, gold in EVAL:
            ranked_all, _ = retrieve(question, k=len(doc_ids), alpha=alpha)
            topk = ranked_all[:k]
            if gold in topk:
                hits += 1
            rank = ranked_all.index(gold) + 1
            rr += 1.0 / rank
        return hits / len(EVAL), rr / len(EVAL)

    print(f"{'alpha (dense weight)':>22} | {'hit-rate@2':>11} | {'MRR':>6}")
    print("-" * 46)
    for alpha in (0.0, 0.5, 1.0):  # 0=lexical only, 1=dense only, 0.5=hybrid
        hr, mrr = evaluate(k=2, alpha=alpha)
        label = {0.0: "lexical only", 1.0: "dense only", 0.5: "HYBRID"}[alpha]
        print(f"{alpha:>6.1f} ({label:>12}) | {hr:>11.2f} | {mrr:>6.3f}")
    print("\nLesson: you cannot improve what you don't measure. Build the eval set")
    print("FIRST, then tune chunking / embeddings / alpha / k against it.")

    banner("EXTEND THIS")
    print(
        """
1. Add a cross-encoder re-ranker (e.g., sentence-transformers CrossEncoder) over
   the top-k and measure the MRR improvement.
2. Make chunking real: take a long markdown doc, split with overlap, and study
   how chunk size changes hit-rate.
3. Wire in a real LLM for generation and add a 'faithfulness' check: does every
   sentence in the answer trace to a retrieved chunk? (See Ragas, RESOURCES 6.)
4. Add an 'I don't know' test: ask a question NOT covered by the docs and verify
   the system abstains instead of hallucinating.
"""
    )


if __name__ == "__main__":
    main()
