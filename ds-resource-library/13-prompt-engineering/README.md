# 13 · Prompt Engineering

> The cheapest, fastest lever for getting good results from LLMs. A real
> engineering discipline — measurable, versioned, and testable — not folklore.

---

## 📌 What it is & why it matters

Prompt engineering is the practice of designing inputs that reliably get the
behavior you want from an LLM. It's the first thing to try before RAG or
fine-tuning, and often gets you 80% of the way. Done well, it's reproducible and
evaluated; done poorly, it's brittle guessing.

---

## 🧠 Core concepts

- **Clarity & specificity** — say exactly what you want, the format, and the constraints.
- **Role / system prompts** — set persona, rules, and boundaries.
- **Few-shot prompting** — show examples of input→output.
- **Chain-of-thought** — ask for step-by-step reasoning on hard tasks.
- **Structured output** — request JSON / use function calling; never parse free text
  for programmatic use.
- **Decomposition** — break complex tasks into steps/chains.
- **Context engineering** — what you put *in* the context window (retrieved docs,
  history, tools) often matters more than clever wording.
- **Guardrails & injection** — treat user/retrieved text as untrusted.
- **Prompts are code** — version them, test them, evaluate changes.

---

## 📚 Best resources

- **dair-ai/Prompt-Engineering-Guide** — the most comprehensive open guide
  (prompting, context engineering, RAG, agents): https://github.com/dair-ai/Prompt-Engineering-Guide
- **Anthropic — Interactive Prompt Engineering Tutorial** (hands-on):
  https://github.com/anthropics/prompt-eng-interactive-tutorial
- **Anthropic prompting best practices**: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- **OpenAI — Prompt engineering guide**: https://platform.openai.com/docs/guides/prompt-engineering
- **DeepLearning.AI — ChatGPT Prompt Engineering for Developers** (free short course).
- **promptslab/Awesome-Prompt-Engineering**: https://github.com/promptslab/Awesome-Prompt-Engineering

---

## 💻 Code example

```text
# ❌ Weak prompt (vague, unconstrained, free-text output)
Summarize this review.

# ✅ Strong prompt (role + task + format + constraints + few-shot)
SYSTEM:
You are a product analyst. Classify customer reviews. Reply ONLY with JSON:
{"sentiment": "positive|neutral|negative", "themes": [...], "action_needed": bool}

EXAMPLE
Review: "Battery dies in 2 hours, but the screen is gorgeous."
Output: {"sentiment":"negative","themes":["battery","display"],"action_needed":true}

NOW DO THIS
Review: "Setup was confusing but support walked me through it kindly."
Output:
```

Key techniques shown: a clear role, a strict output schema (JSON), a worked
example (one-shot), and constraints. Set `temperature=0` for deterministic
extraction tasks.

---

## 🌍 Real-world use cases

- **Extraction & classification** — structured fields from messy text.
- **Drafting & rewriting** — emails, summaries, marketing copy with a fixed style.
- **Reasoning tasks** — analysis, planning (with chain-of-thought).
- **Routing** — classify a request, then route to the right tool/agent.

---

## 🛠️ Hands-on project ideas

1. Take one task and build an **eval set**; iterate prompts and measure accuracy
   improvement (treat prompts as code).
2. Convert a free-text prompt to **strict JSON output** + validation, and measure
   how much parsing reliability improves.
3. Build a **prompt-injection test suite** for a RAG app and harden the system prompt.

---

## 🗺️ Suggested learning path

1. Clarity, roles, format → 2. Few-shot & chain-of-thought → 3. Structured output
/ function calling → 4. Decomposition & context engineering → 5. Evaluation of
prompts → 6. Guardrails & injection defense → 7. Apply in RAG (12) & Agents (14).
