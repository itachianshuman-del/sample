"""
Example — LLM structured output + validation (the production-safe pattern)
==========================================================================
Runnable with a MOCK LLM (no API key). Deps: none (stdlib)

For anything programmatic, NEVER parse free text -- request JSON and VALIDATE it.
This shows the validate-and-retry pattern that makes LLM features reliable.
Swap `mock_llm_call` for a real API call (OpenAI/Anthropic) and keep the rest.

Run: python example.py
"""

from __future__ import annotations

import json

REQUIRED_KEYS = {"sentiment", "topics", "urgent"}
VALID_SENTIMENT = {"positive", "neutral", "negative"}


def mock_llm_call(text: str, strict: bool) -> str:
    """Pretend LLM. With strict=False it returns messy text (to show validation)."""
    payload = {
        "sentiment": "negative",
        "topics": ["payment", "support"],
        "urgent": True,
    }
    if strict:
        return json.dumps(payload)                    # clean JSON
    return f"Sure! Here is the result:\n{json.dumps(payload)}\nHope that helps!"


def extract_json(raw: str) -> dict | None:
    """Be liberal in what you accept: find the JSON object inside the response."""
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(raw[start : end + 1])
    except json.JSONDecodeError:
        return None


def validate(obj: dict) -> list[str]:
    errors = []
    if not REQUIRED_KEYS.issubset(obj):
        errors.append(f"missing keys: {REQUIRED_KEYS - set(obj)}")
    if obj.get("sentiment") not in VALID_SENTIMENT:
        errors.append(f"bad sentiment: {obj.get('sentiment')}")
    if not isinstance(obj.get("urgent"), bool):
        errors.append("urgent must be boolean")
    return errors


def get_structured(text: str, max_retries: int = 2) -> dict:
    for attempt in range(max_retries + 1):
        raw = mock_llm_call(text, strict=(attempt > 0))   # retry asks for stricter output
        obj = extract_json(raw)
        if obj and not validate(obj):
            print(f"  attempt {attempt+1}: valid ✓")
            return obj
        print(f"  attempt {attempt+1}: invalid, retrying with stricter prompt...")
    raise ValueError("LLM failed to return valid structured output")


if __name__ == "__main__":
    msg = "My payment failed three times and nobody has replied in two days!"
    print("=" * 60, f"\nExtracting structured data from:\n  {msg!r}\n", "=" * 60)
    result = get_structured(msg)
    print("Parsed & validated:", result)
    print("\nLesson: request JSON, EXTRACT robustly, VALIDATE, and RETRY on failure."
          " This is what makes LLM features production-grade.")
