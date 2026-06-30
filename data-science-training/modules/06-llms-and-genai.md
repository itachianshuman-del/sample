# Module 6 — LLMs & Generative AI

> **Why this matters:** GenAI is now table stakes for a senior data scientist.
> The gap isn't "can you call an API" — it's "can you build, evaluate, and
> operate an LLM system that's reliable, cheap, and doesn't silently regress."

**Outcome:** you can build a RAG system, fine-tune a small model, rigorously
evaluate LLM outputs, and reason about cost/latency/quality trade-offs.

---

## Section 1 — Mental model of LLMs

- LLMs are next-token predictors trained on huge corpora, then aligned (SFT +
  preference tuning). Understand: **pretraining → fine-tuning → alignment**.
- **Tokens** (not words) drive cost and context limits. **Context window** =
  working memory.
- **Temperature / top-p** control randomness. **Logprobs** expose confidence.
- They **hallucinate** because they optimize plausibility, not truth. Every
  design choice below is partly about managing this.

Best structured path: **mlabonne/llm-course** (RESOURCES §6), specifically the
"LLM Engineer" track for application building.

## Section 2 — Prompt engineering (the cheapest lever)

- **Be specific**, give examples (few-shot), specify format, give the model a
  role and constraints.
- **Chain-of-thought / step-by-step** for reasoning tasks.
- **Structured output** (JSON schema / function calling) for anything
  programmatic — don't parse free text.
- **Decompose** complex tasks into steps/chains.
- Prompts are code: version them, test them, and track changes.

## Section 3 — Retrieval-Augmented Generation (RAG)

RAG grounds the model in your data to reduce hallucination and add fresh/private
knowledge. The pipeline:

```
Documents → chunk → embed → vector store
Query → embed → retrieve top-k → build prompt with context → generate → cite
```

Design decisions that actually matter:
- **Chunking** — size and overlap; chunk on semantic boundaries, not arbitrary
  character counts.
- **Embeddings** — model choice and domain fit.
- **Retrieval** — pure vector vs **hybrid (BM25 + vector)**; hybrid usually wins.
- **Re-ranking** — a cross-encoder reranker on top-k improves precision a lot.
- **Context construction** — order, dedupe, fit budget, include citations.

Build it once from scratch (`lab05_rag_from_scratch.py`) before reaching for a
framework, so you understand each component.

## Section 4 — RAG vs fine-tuning vs prompting

| Need | Best tool |
|---|---|
| Inject fresh/private *knowledge* | RAG |
| Change *behavior/format/style* | Fine-tuning |
| Quick task adaptation | Prompting / few-shot |
| Domain *vocabulary* & consistent structure | Fine-tuning (often + RAG) |

A common senior answer: **start with prompting, add RAG for knowledge, fine-tune
only when prompting+RAG plateau** and you have data + a clear ROI.

## Section 5 — Evaluation (the make-or-break skill)

LLM outputs are open-ended, so eval is hard and most teams under-invest. Build:
- **A fixed eval set** of representative inputs with expected behavior.
- **Task metrics:** exact match / F1 for extraction; **retrieval metrics**
  (hit-rate, MRR, recall@k) for RAG; faithfulness/groundedness for generation
  (e.g., **Ragas**).
- **LLM-as-judge** — use a strong model to score outputs against a rubric; cheap
  and scalable, but validate it against human labels and watch its biases.
- **Regression suite** — run the eval set on every prompt/model/config change so
  you catch silent regressions *before* shipping. This is the LLM equivalent of
  unit tests.

## Section 6 — Fine-tuning (SFT, LoRA/QLoRA)

- **SFT (supervised fine-tuning)** — teach format/behavior from (input, ideal
  output) pairs. Data quality > quantity.
- **LoRA / QLoRA** — parameter-efficient fine-tuning; train small adapter
  weights, cheap enough for a single GPU. The default for most practitioners.
- **Preference tuning (DPO/RLHF)** — align to preferences; conceptually important,
  rarely needed at the application layer.
- Tools: Hugging Face `transformers` + `peft` + `trl` (RESOURCES §6).

## Section 7 — Agents & tool use

- **Tool/function calling** — let the model call APIs, search, run code. This is
  where most real value beyond chat lives.
- **Agentic loops** — plan → act → observe → repeat. Powerful but add latency,
  cost, and failure modes; keep them as constrained as the task allows.
- Guard with: max steps, validation of tool inputs/outputs, and fallbacks.

## Section 8 — Production concerns

- **Latency** — streaming, smaller/distilled models, caching, parallel calls.
- **Cost** — tokens add up fast; cache, route easy queries to cheaper models,
  trim context.
- **Reliability** — retries, timeouts, fallbacks, output validation/guardrails.
- **Safety** — prompt injection (especially with RAG/tools), PII handling,
  output moderation.
- **Observability** — log prompts, responses, latencies, costs; trace chains.

## Section 9 — Prompt injection & security

With RAG and tools, untrusted text can hijack the model. Treat retrieved content
and user input as untrusted: constrain tool permissions, validate outputs, and
never let the model execute high-privilege actions without checks.

## Section 10 — Staying current responsibly

The field moves weekly. Anchor on durable concepts (retrieval, evaluation,
alignment) and follow high-signal sources: Chip Huyen, Lilian Weng, Sebastian
Raschka (RESOURCES §6, §11). Ignore the hype cycle; evaluate with your own evals.

---

## Thinking questions
1. When does RAG beat fine-tuning? Give a concrete example of each.
2. How do you stop an LLM feature from silently regressing after a prompt tweak?
3. Your RAG answers are wrong — is it retrieval or generation? How do you tell?
4. What's prompt injection and how do you defend a RAG+tools system against it?

## Deliverable
A working RAG system over a corpus you choose, with an evaluation harness
(retrieval hit-rate + answer-quality scoring). Then EITHER fine-tune a small
model with LoRA on a focused task, OR write a rigorous eval report comparing
prompting vs RAG vs fine-tuning for one task.

## Go deeper
RESOURCES §6. Priorities: mlabonne/llm-course (LLM Engineer track), HF LLM
course, Ragas for eval, PEFT for fine-tuning, Lilian Weng's blog for depth.
