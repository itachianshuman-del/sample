# 06 · Natural Language Processing (NLP)

> Teaching machines to understand and generate human language — the bridge from
> classic text mining to modern LLMs.

---

## 📌 What it is & why it matters

NLP lets computers process text and speech: classification, extraction,
translation, summarization, search, and generation. It underpins chatbots, search
engines, sentiment analysis, and LLMs. Understanding NLP fundamentals (tokenization,
embeddings, transformers) is the foundation for everything in the GenAI section.

---

## 🧠 Core concepts

- **Text preprocessing:** tokenization, stemming/lemmatization, stop words,
  n-grams (classic) — and **subword tokenization** (BPE) for modern models.
- **Representations:** Bag-of-Words, TF-IDF → **word embeddings** (Word2Vec,
  GloVe) → **contextual embeddings** (BERT) → sentence embeddings.
- **Classic tasks:** classification (sentiment, spam), NER, topic modeling, POS.
- **The transformer revolution:** attention, BERT (encoder) vs GPT (decoder),
  transfer learning via pretrained models.
- **Modern NLP = LLMs:** most tasks are now solved by prompting/fine-tuning large
  models (see topics 11–13).
- **Evaluation:** accuracy/F1 (classification), BLEU/ROUGE (generation),
  embedding-based metrics.

---

## 📚 Best resources

### Courses
- **Hugging Face — NLP Course** (free, the modern standard): https://huggingface.co/learn/nlp-course
- **Stanford CS224N — NLP with Deep Learning** (lectures on YouTube, free).
- **Krish Naik — Complete NLP playlist** + the
  [Complete DS + ML + NLP 2024](https://github.com/krishnaik06/Complete-Data-Science-With-Machine-Learning-And-NLP-2024) repo
  (NLTK, spaCy, embeddings, transformers — hands-on).

### Reference
- **The Illustrated Transformer / BERT** (Jay Alammar): https://jalammar.github.io/
- **spaCy course** (free, industrial NLP): https://course.spacy.io/
- Libraries: Hugging Face `transformers`, spaCy, NLTK, `sentence-transformers`.

---

## 💻 Code example

```python
# Modern NLP in 3 lines with Hugging Face pipelines.
from transformers import pipeline

sentiment = pipeline("sentiment-analysis")
print(sentiment("The delivery was late but support fixed it instantly."))
# [{'label': 'POSITIVE', 'score': 0.97}]  (handles mixed sentiment via context)

# Semantic similarity with sentence embeddings (powers search & RAG).
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("all-MiniLM-L6-v2")
emb = model.encode(["How do I reset my password?",
                    "I forgot my login credentials"])
print(f"similarity: {util.cos_sim(emb[0], emb[1]).item():.2f}")  # ~0.6+ (related)
```

---

## 🌍 Real-world use cases

- **Customer support** — ticket classification, intent detection, auto-responses.
- **Search & retrieval** — semantic search over documents (foundation of RAG).
- **Sentiment & social listening** — brand monitoring at scale.
- **Information extraction** — pulling entities/fields from contracts, resumes, invoices.
- **Summarization & translation.**

---

## 🛠️ Hands-on project ideas

1. Build a **text classifier** (TF-IDF + logistic regression) and beat it with a
   fine-tuned transformer; compare effort vs gains.
2. Build a **semantic search** engine over a document set with sentence embeddings.
3. Fine-tune **DistilBERT** for a custom classification task on Hugging Face.

---

## 🗺️ Suggested learning path

1. Text preprocessing & TF-IDF → 2. Word embeddings → 3. Classic tasks
(classification, NER) → 4. Transformers & BERT → 5. Hugging Face `transformers`
→ 6. Move to LLMs (11) and RAG (12).
