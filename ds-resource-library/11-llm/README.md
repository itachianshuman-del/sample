# 11 · Large Language Models (LLMs)

> The models behind ChatGPT, Claude, Gemini, and Llama. Understanding how to use,
> adapt, evaluate, and serve them is now core to a senior data scientist's toolkit.

---

## 📌 What it is & why it matters

LLMs are large neural networks (transformers) trained to predict the next token on
massive text corpora, then aligned to follow instructions. They can write, reason,
summarize, extract, classify, and code — often zero-shot. They've redefined what's
buildable in months, and "LLM literacy" is now table stakes.

---

## 🧠 Core concepts

- **The pipeline:** pretraining → supervised fine-tuning (SFT) → preference
  alignment (RLHF/DPO).
- **Tokens** drive cost and the **context window** (working memory).
- **Inference controls:** temperature, top-p, max tokens; logprobs.
- **Hallucination** — they optimize plausibility, not truth; manage it with RAG,
  grounding, and evaluation.
- **Adapting a model:** prompting → **RAG** (inject knowledge) → **fine-tuning**
  (change behavior; LoRA/QLoRA for cheap fine-tuning).
- **Evaluation:** fixed eval sets, task metrics, **LLM-as-judge**, regression suites.
- **Serving:** latency, cost, caching, streaming, structured output / function
  calling, guardrails, prompt-injection safety.

> Deep dive:
> [`data-science-training/modules/06-llms-and-genai.md`](../../data-science-training/modules/06-llms-and-genai.md).

---

## 📚 Best resources

### Courses
- **mlabonne/llm-course** — the best free structured LLM curriculum (LLM Scientist
  + LLM Engineer tracks, Colab notebooks): https://github.com/mlabonne/llm-course
- **Hugging Face — LLM Course**: https://huggingface.co/learn/llm-course
- **Krish Naik — GenAI / LLM playlists** + the
  [Data Science Gen-AI Playlist 2024](https://github.com/krishnaik06/Data-Science-Gen-AI-Playlist-2024) repo.
- **Andrej Karpathy — "Let's build GPT" / Intro to LLMs** (build one yourself).

### Reference & blogs
- **LLM Engineer's Handbook** (curated): https://github.com/SylphAI-Inc/LLM-engineer-handbook
- **Lilian Weng's blog (Lil'Log)** — deep, authoritative posts: https://lilianweng.github.io/
- **Chip Huyen's blog** + the book *AI Engineering*: https://huyenchip.com/blog/
- Hugging Face `transformers` + `peft` (LoRA): https://github.com/huggingface/peft

---

## 💻 Code example

```python
# Calling an LLM with STRUCTURED OUTPUT (the production-safe pattern).
# Don't parse free text — request JSON and validate it.
from openai import OpenAI               # works with OpenAI-compatible APIs
import json

client = OpenAI()
resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content":
         "Extract fields. Reply ONLY with JSON: "
         '{"sentiment": "...", "topics": [...], "urgent": true|false}'},
        {"role": "user", "content":
         "My payment failed three times and no one has responded for two days!"},
    ],
    response_format={"type": "json_object"},   # force valid JSON
    temperature=0,                              # deterministic for extraction
)
data = json.loads(resp.choices[0].message.content)
print(data)   # {'sentiment': 'negative', 'topics': ['payment','support'], 'urgent': True}
```

---

## 🌍 Real-world use cases

- **Support automation** — classification, drafting replies, summarizing tickets.
- **Knowledge assistants** — Q&A over company docs (RAG, topic 12).
- **Content & code generation** — drafting, refactoring, boilerplate.
- **Data extraction** — turning unstructured text into structured fields.
- **Analytics copilots** — natural-language-to-SQL, report generation.

---

## 🛠️ Hands-on project ideas

1. Build a **text-classification** feature with an LLM and compare it to a
   fine-tuned small model (cost/latency/quality).
2. **Fine-tune** a small open model with **LoRA** on a focused task.
3. Build an **eval harness** that scores outputs and catches regressions on prompt changes.

---

## 🗺️ Suggested learning path

1. How transformers/LLMs work (topics 05, 06) → 2. Prompting (topic 13) →
3. Structured output & function calling → 4. RAG (topic 12) → 5. Evaluation →
6. Fine-tuning (LoRA) → 7. Serving & cost/latency → 8. Agents (topic 14).
