"""
Example — Interview Prep (probability + a coding pattern)
=========================================================
Runnable. Deps: numpy

Two interview staples:
  1. A probability question solved BOTH by simulation and exact reasoning
     (interviewers love when you can do both and sanity-check yourself).
  2. A common Python data pattern: top-N per group without pandas.

Run: python example.py
"""

from __future__ import annotations

from collections import defaultdict

import numpy as np


def birthday_paradox(n_people: int = 23, trials: int = 200_000) -> None:
    """P(at least two people share a birthday) in a room of n. Classic question."""
    rng = np.random.default_rng(0)
    days = rng.integers(0, 365, size=(trials, n_people))
    # A collision exists if unique birthdays < n_people.
    has_collision = np.array([len(np.unique(row)) < n_people for row in days[:20_000]])
    sim = has_collision.mean()

    # Exact: 1 - product((365-i)/365) for i in 0..n-1
    p_no = 1.0
    for i in range(n_people):
        p_no *= (365 - i) / 365
    print("=" * 60)
    print(f"Birthday paradox (n={n_people}):  simulated={sim:.3f}  exact={1-p_no:.3f}")


def top_n_per_group(rows, n=2):
    """Top-N by score within each group -- a frequent coding question."""
    groups = defaultdict(list)
    for name, group, score in rows:
        groups[group].append((score, name))
    result = {}
    for group, items in groups.items():
        result[group] = sorted(items, reverse=True)[:n]
    return result


if __name__ == "__main__":
    birthday_paradox()

    data = [
        ("Alice", "eng", 95), ("Bob", "eng", 88), ("Cara", "eng", 91),
        ("Dan", "sales", 70), ("Eve", "sales", 82), ("Finn", "sales", 75),
    ]
    print("\nTop-2 per department:")
    for dept, top in top_n_per_group(data, n=2).items():
        print(f"  {dept}: {[(name, sc) for sc, name in top]}")
    print("\nTip: state assumptions, think out loud, give a baseline first, then"
          " optimize. Interviewers score your reasoning, not just the answer.")
