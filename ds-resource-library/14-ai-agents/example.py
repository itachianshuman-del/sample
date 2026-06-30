"""
Example — AI Agent loop (plan -> act -> observe -> answer)
==========================================================
Runnable with a MOCK reasoning step (no API key). Deps: none (stdlib)

Shows the ESSENCE of an agent: the model decides to call a tool, your code runs
the real tool, the result is fed back, and the model produces a final answer.
The "reasoning" here is a simple rule so it runs offline; in production this is
an LLM with function/tool calling.

Run: python example.py
"""

from __future__ import annotations

import re

# ---- Real tools the agent can call ----
def calculator(expression: str) -> str:
    # In production: sandbox this. Here we allow only digits/operators.
    if not re.fullmatch(r"[0-9+\-*/(). ]+", expression):
        return "error: invalid expression"
    try:
        return str(eval(expression))          # safe-ish given the regex guard
    except Exception as e:                     # noqa: BLE001
        return f"error: {e}"


def get_weather(city: str) -> str:
    return {"London": "12C rainy", "Dubai": "38C sunny"}.get(city, "unknown")


TOOLS = {"calculator": calculator, "get_weather": get_weather}


def reason(user_query: str) -> tuple[str, str]:
    """MOCK of an LLM deciding which tool + args to use (returns tool, arg)."""
    q = user_query.lower()
    if any(c.isdigit() for c in q) and any(op in q for op in "+-*/"):
        expr = re.sub(r"[^0-9+\-*/(). ]", "", user_query)
        return "calculator", expr.strip()
    if "weather" in q:
        city = "Dubai" if "dubai" in q else "London"
        return "get_weather", city
    return "none", ""


def agent(user_query: str, max_steps: int = 3) -> str:
    print(f"\nUSER: {user_query}")
    for step in range(max_steps):                       # guardrail: bounded loop
        tool, arg = reason(user_query)                  # 1. PLAN
        if tool == "none":
            return "I can answer directly (no tool needed)."
        observation = TOOLS[tool](arg)                  # 2. ACT (run real tool)
        print(f"  step {step+1}: call {tool}({arg!r}) -> {observation}")  # 3. OBSERVE
        return f"Answer: {observation}"                 # 4. RESPOND
    return "Stopped: hit max steps (guardrail)."


if __name__ == "__main__":
    print("=" * 60, "\nAgent pattern: PLAN -> ACT -> OBSERVE -> RESPOND\n", "=" * 60)
    print(agent("What is 1234 * 17 + 9?"))
    print(agent("What's the weather in Dubai?"))
    print("\nExtend: replace reason() with a real LLM tool-call, add memory,"
          " and orchestrate multi-step flows with LangGraph or CrewAI.")
