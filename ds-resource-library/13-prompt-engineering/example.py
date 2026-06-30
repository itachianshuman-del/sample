"""
Example — Prompt Engineering as an evaluated discipline
=======================================================
Runnable with a MOCK LLM (no API key). Deps: none (stdlib)

The key idea: prompts are CODE. Build an eval set, run candidate prompts against
it, and measure accuracy -- so you can improve prompts objectively and catch
regressions. Here a tiny rule-based "mock LLM" stands in for a real model so the
harness runs offline; swap `mock_llm` for a real API call unchanged.

Run: python example.py
"""

from __future__ import annotations

import json
import re

# --- A fixed evaluation set: input -> expected label (the "ground truth") ---
EVAL_SET = [
    ("My order never arrived and support is ignoring me!", "negative"),
    ("Works great, super happy with the quality.", "positive"),
    ("It's okay, nothing special.", "neutral"),
    ("Absolutely terrible, want a refund now.", "negative"),
    ("Pretty good but shipping was slow.", "positive"),
]


def mock_llm(prompt: str, text: str) -> str:
    """Stand-in for a real LLM. A 'better' prompt yields better mock behavior."""
    pos = {"great", "happy", "good", "love", "excellent"}
    neg = {"terrible", "never", "ignoring", "refund", "awful", "bad"}
    t = set(re.findall(r"[a-z]+", text.lower()))
    has_examples = "EXAMPLE" in prompt          # reward the few-shot prompt
    score = len(t & pos) - len(t & neg)
    if score > 0:
        label = "positive"
    elif score < 0:
        label = "negative"
    else:
        label = "neutral" if has_examples else "positive"   # weak prompt guesses
    return json.dumps({"sentiment": label})


WEAK_PROMPT = "Classify the sentiment."
STRONG_PROMPT = (
    "You are a precise classifier. Reply ONLY JSON {\"sentiment\": "
    "\"positive|neutral|negative\"}.\n"
    "EXAMPLE\nText: 'It is fine, nothing special.' -> {\"sentiment\": \"neutral\"}\n"
)


def evaluate(prompt: str) -> float:
    correct = 0
    for text, expected in EVAL_SET:
        try:
            pred = json.loads(mock_llm(prompt, text)).get("sentiment")
        except json.JSONDecodeError:
            pred = None
        correct += (pred == expected)
    return correct / len(EVAL_SET)


if __name__ == "__main__":
    print("=" * 60)
    print(f"Weak prompt   accuracy: {evaluate(WEAK_PROMPT):.0%}")
    print(f"Strong prompt accuracy: {evaluate(STRONG_PROMPT):.0%}")
    print("=" * 60)
    print("Lesson: measure prompts against a fixed eval set. The strong prompt"
          " (role + strict JSON + a worked example) wins -- and you can prove it.")
    print("Run this on every prompt change to catch silent regressions.")
