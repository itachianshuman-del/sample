"""
Example — Python for Data Science (NumPy + pandas)
==================================================
Runnable. Deps: numpy, pandas

Demonstrates the two ideas that matter most day-to-day:
  1. VECTORIZATION (let NumPy do loops in C, not Python)
  2. The pandas "daily five": filter -> group -> aggregate -> join -> reshape

Run: python example.py
"""

from __future__ import annotations

import time

import numpy as np
import pandas as pd


def vectorization_demo() -> None:
    print("=" * 60, "\n1) VECTORIZATION: same result, ~100x faster\n", "=" * 60)
    data = np.random.default_rng(0).normal(100, 20, size=1_000_000)

    # Slow: Python loop
    t0 = time.perf_counter()
    out_loop = [x * 1.1 if x > 100 else x * 0.9 for x in data]
    t_loop = time.perf_counter() - t0

    # Fast: vectorized with np.where
    t0 = time.perf_counter()
    out_vec = np.where(data > 100, data * 1.1, data * 0.9)
    t_vec = time.perf_counter() - t0

    assert np.allclose(out_loop, out_vec)  # identical results
    print(f"Python loop : {t_loop*1000:7.1f} ms")
    print(f"Vectorized  : {t_vec*1000:7.1f} ms   -> {t_loop/max(t_vec,1e-9):.0f}x faster")


def pandas_demo() -> None:
    print("\n" + "=" * 60, "\n2) The pandas daily five\n", "=" * 60)
    orders = pd.DataFrame({
        "order_id":  [1, 2, 3, 4, 5, 6],
        "customer":  ["A", "A", "B", "B", "C", "C"],
        "region":    ["EU", "EU", "US", "US", "EU", "US"],
        "amount":    [120, 80, 300, 45, 220, 60],
    })
    customers = pd.DataFrame({"customer": ["A", "B", "C"],
                              "tier": ["gold", "silver", "gold"]})

    result = (
        orders[orders["amount"] >= 60]                       # 1. filter
        .merge(customers, on="customer")                     # 2. join
        .groupby(["region", "tier"], as_index=False)         # 3. group
        .agg(revenue=("amount", "sum"),                      # 4. aggregate
             n_orders=("order_id", "count"))
        .sort_values("revenue", ascending=False)             # 5. sort
    )
    print(result.to_string(index=False))


if __name__ == "__main__":
    vectorization_demo()
    pandas_demo()
    print("\nExtend: rewrite a slow .apply() in your own code as a vectorized op.")
