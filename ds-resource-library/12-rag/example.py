"""
Example — RAG core (embed -> retrieve -> grounded prompt -> abstain)
====================================================================
Runnable offline with ZERO external services. Deps: numpy, scikit-learn

Retrieval here uses TF-IDF vectors + cosine similarity -- a legitimate, simple,
deterministic method that runs offline. In production you'd swap `Retriever` for
dense neural embeddings (sentence-transformers / OpenAI / Cohere) and a vector
DB; the retrieve -> ground -> abstain logic stays identical.

Run: python example.py
"""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCS = [
    "Refunds are processed within 5 to 7 business days after approval.",
    "Support is available 24/7 for premium plan customers.",
    "You can reset your password from the account settings page.",
    "Free shipping applies to orders over 50 dollars.",
]


class Retriever:
    """Index once, then retrieve top-k by cosine similarity."""

    def __init__(self, docs: list[str]):
        self.docs = docs
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.doc_vecs = self.vectorizer.fit_transform(docs)   # the 'embeddings'

    def retrieve(self, query: str, k: int = 2):
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.doc_vecs)[0]
        order = sims.argsort()[::-1][:k]
        return [(self.docs[i], float(sims[i])) for i in order]


def build_prompt(query: str, hits) -> str:
    context = "\n".join(f"[{i+1}] {doc}" for i, (doc, _) in enumerate(hits))
    return (
        "Answer ONLY from the context and cite like [1]. "
        "If the answer is not present, say you don't know.\n\n"
        f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )


if __name__ == "__main__":
    retriever = Retriever(DOCS)
    GROUND_THRESHOLD = 0.10   # below this, the top match is too weak -> abstain

    for query in ["How long do refunds take?", "What is the capital of France?"]:
        hits = retriever.retrieve(query)
        best_doc, best_score = hits[0]
        print("=" * 60)
        print(f"QUERY : {query}")
        print(f"top match (score={best_score:.2f}): {best_doc}")
        if best_score >= GROUND_THRESHOLD:
            print("-> GROUNDED: build a cited prompt and let the LLM answer.")
            # print(build_prompt(query, hits))   # uncomment to see the full prompt
        else:
            print("-> ABSTAIN: no relevant context. Say 'I don't know' (no hallucination).")

    print("\nLesson: retrieval quality decides RAG quality. Measure it with a")
    print("hit-rate@k eval set, add hybrid (BM25 + dense) retrieval and a reranker,")
    print("and always abstain when the best match is too weak.")
