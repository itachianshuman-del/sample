# 12 · RAG (Retrieval-Augmented Generation)

> Ground an LLM in *your* data to reduce hallucination and answer from private,
> fresh knowledge. The most common and valuable LLM application pattern in industry.

---

## 📌 What it is & why it matters

RAG retrieves relevant documents from your knowledge base and feeds them to the
LLM as context, so answers are grounded in facts the model didn't memorize. It's
how you build assistants over company docs, support knowledge, codebases, and
policies — without retraining the model. RAG is usually the **first** thing teams
build with LLMs.

---

## 🧠 Core concepts

```
Documents → chunk → embed → vector store        (indexing, done once)
Query → embed → retrieve top-k → (rerank) → build grounded prompt → generate + cite
```

- **Chunking** — split docs on semantic boundaries; tune size & overlap.
- **Embeddings** — turn text into vectors; choice/domain-fit matters.
- **Vector store** — FAISS, Chroma, pgvector, Qdrant, Weaviate, Pinecone.
- **Retrieval:** dense (vector) vs **hybrid** (BM25 + vector — usually wins).
- **Re-ranking** — a cross-encoder on top-k boosts precision a lot.
- **Context construction** — order, dedupe, fit token budget, include citations.
- **Evaluation (critical):** retrieval metrics (hit-rate@k, MRR) + generation
  metrics (faithfulness/groundedness, e.g., Ragas).
- **Failure analysis:** is it a *retrieval* problem or a *generation* problem?

> Build it from scratch:
> [`data-science-training/hands-on/lab05_rag_from_scratch.py`](../../data-science-training/hands-on/lab05_rag_from_scratch.py)
> · Deep dive: `modules/06-llms-and-genai.md` (section 3).

---

## 📚 Best resources

- **rag-zero-to-hero-guide** (KalyanKS-NLP) — basics to advanced:
  https://github.com/KalyanKS-NLP/rag-zero-to-hero-guide
- **awesome-rag** (coree): https://github.com/coree/awesome-rag
- **LangChain RAG docs** & **LlamaIndex** (concepts > specific APIs):
  https://python.langchain.com/docs/tutorials/rag/ · https://docs.llamaindex.ai/
- **Ragas** — RAG evaluation framework: https://github.com/explodinggradients/ragas
- **superlinked/VectorHub** — advanced RAG articles: https://github.com/superlinked/VectorHub
- **Krish Naik — RAG / LangChain** tutorials (free, hands-on).

---

## 💻 Code example

```python
# Minimal RAG core: embed -> retrieve -> grounded prompt. (no framework)
import numpy as np
from sentence_transformers import SentenceTransformer

docs = [
    "Refunds are processed within 5-7 business days.",
    "Our office is open Monday to Friday, 9am-5pm.",
    "Premium plans include 24/7 priority support.",
]
embedder = SentenceTransformer("all-MiniLM-L6-v2")
doc_emb = embedder.encode(docs, normalize_embeddings=True)   # index once

def retrieve(query, k=2):
    q = embedder.encode([query], normalize_embeddings=True)[0]
    sims = doc_emb @ q                       # cosine sim (vectors normalized)
    top = np.argsort(sims)[::-1][:k]
    return [docs[i] for i in top]

query = "How long do refunds take?"
context = "\n".join(f"- {c}" for c in retrieve(query))
prompt = (f"Answer ONLY from the context. If absent, say you don't know.\n\n"
          f"Context:\n{context}\n\nQuestion: {query}\nAnswer:")
print(prompt)   # -> feed to an LLM; it answers "5-7 business days" grounded in context
```

---

## 🌍 Real-world use cases

- **Customer support assistants** — answer from the help center / knowledge base.
- **Internal knowledge search** — "what's our policy on X?" over wikis/docs.
- **Codebase assistants** — answer questions grounded in a repo.
- **Research & legal** — Q&A with citations over large document sets.

---

## 🛠️ Hands-on project ideas

1. Build a RAG assistant over a document set with **hybrid retrieval + a reranker**.
2. Add an **evaluation harness** (hit-rate@k + faithfulness with Ragas).
3. Add an **"I don't know"** guardrail — verify it abstains on out-of-scope questions.

---

## 🗺️ Suggested learning path

1. Embeddings & semantic search (topic 06) → 2. Build RAG from scratch (lab05) →
3. Chunking strategies → 4. Hybrid retrieval + reranking → 5. Evaluation (Ragas)
→ 6. Production concerns (latency, citations, injection safety) → 7. Agents (topic 14).
