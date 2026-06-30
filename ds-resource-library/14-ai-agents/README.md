# 14 · AI Agents

> LLMs that don't just answer — they *act*: plan, call tools, use external data,
> and complete multi-step tasks. The fastest-growing area of applied GenAI.

---

## 📌 What it is & why it matters

An AI agent uses an LLM as a reasoning engine that can decide which **tools** to
call (search, APIs, code, databases), observe results, and iterate until a task is
done. This unlocks value far beyond chat — automating research, workflows, and
operations. (Caveat: many things labeled "agents" are just automation with a new
name; real agents reason, use tools, and complete end-to-end tasks.)

---

## 🧠 Core concepts

- **Tool / function calling** — the model invokes functions with structured args;
  the foundation of agency.
- **The agent loop:** plan → act (tool) → observe → repeat (e.g., ReAct pattern).
- **Memory** — short-term (context) and long-term (vector store / state).
- **Orchestration frameworks:**
  - **LangGraph** — graph-based control of states, tools, and evaluators (robust,
    production-leaning).
  - **CrewAI** — role-based multi-agent "crews" (researcher + writer + reviewer).
  - **AutoGen**, **OpenAI Agents SDK**, **LlamaIndex agents**.
- **Multi-agent systems** — specialized agents collaborating.
- **Guardrails** — max steps, validated tool I/O, fallbacks; agents add latency,
  cost, and failure modes, so constrain them to the task.
- **Evaluation & observability** — trace every step; eval task success, not vibes.

---

## 📚 Best resources

### Courses & guides
- **DeepLearning.AI — agent short courses** (LangGraph, CrewAI, AutoGen, Functions/
  Tools/Agents) — free: https://www.deeplearning.ai/short-courses/
- **Hugging Face — AI Agents Course** (free): https://huggingface.co/learn/agents-course
- **Krish Naik — Agentic AI / LangGraph / CrewAI** tutorials (free, hands-on).
- **dair-ai/Prompt-Engineering-Guide** (agents section): https://github.com/dair-ai/Prompt-Engineering-Guide

### Frameworks & examples
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **CrewAI examples**: https://github.com/crewAIInc/crewAI-examples
- **dipanjanS — LangGraph agents workshop (DHS 2025)**: https://github.com/dipanjanS/mastering-intelligent-agents-langgraph-workshop-dhs2025

---

## 💻 Code example

```python
# The essence of an agent: the LLM decides to call a TOOL, you run it, feed back.
import json

def get_weather(city: str) -> str:               # a "tool"
    fake = {"London": "12C, rainy", "Dubai": "38C, sunny"}
    return fake.get(city, "unknown")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {"type": "object",
                       "properties": {"city": {"type": "string"}},
                       "required": ["city"]},
    },
}]

# 1) Model sees the question + available tools and REQUESTS a tool call.
# 2) Your code executes the tool and returns the result.
# 3) Model uses the result to answer. (Pseudo-flow with an OpenAI-compatible API)
#
# resp = client.chat.completions.create(model=..., messages=msgs, tools=tools)
# call = resp.choices[0].message.tool_calls[0]
# args = json.loads(call.function.arguments)
# result = get_weather(**args)                    # -> "12C, rainy"
# ...append result to messages, call the model again for the final answer.
print("Agent pattern: LLM -> tool call -> observe -> respond")
```

---

## 🌍 Real-world use cases

- **Research assistants** — search, read, synthesize, cite.
- **Customer ops** — look up orders, issue refunds, update tickets (with guardrails).
- **Data analysis copilots** — write & run SQL/Python, interpret results.
- **Workflow automation** — multi-step back-office processes.
- **Coding agents** — navigate a repo, edit files, run tests.

---

## 🛠️ Hands-on project ideas

1. Build a **single-tool agent** (e.g., calculator or web search) with function calling.
2. Build a **research crew** in CrewAI (researcher → writer → reviewer).
3. Build a **LangGraph agent** with branching, a tool, and a max-step guardrail; trace its steps.

---

## 🗺️ Suggested learning path

1. Function/tool calling (topic 11/13) → 2. The ReAct loop → 3. A single-tool
agent → 4. LangGraph (state + control) → 5. Multi-agent (CrewAI) → 6. Memory,
guardrails, evaluation & observability → 7. Ship a constrained, monitored agent.
