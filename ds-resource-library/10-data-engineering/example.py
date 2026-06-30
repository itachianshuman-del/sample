"""
Example — Data Engineering with DuckDB (warehouse SQL on local files)
=====================================================================
Runnable. Deps: duckdb, pandas

DuckDB lets you run fast, warehouse-style SQL directly on DataFrames/Parquet/CSV
with zero setup -- a data-scientist superpower for ELT and analytics.

Run: python example.py
"""

from __future__ import annotations

import duckdb
import pandas as pd

# Pretend these came from your warehouse / data lake.
orders = pd.DataFrame({
    "order_id":   range(1, 9),
    "customer":   ["A", "A", "B", "C", "B", "C", "A", "B"],
    "region":     ["EU", "EU", "US", "EU", "US", "US", "EU", "US"],
    "amount":     [120, 80, 300, 220, 45, 60, 90, 150],
    "order_date": pd.to_datetime(
        ["2024-01-05", "2024-01-09", "2024-01-10", "2024-02-01",
         "2024-02-03", "2024-02-15", "2024-03-01", "2024-03-02"]),
})

# ELT-style transform: aggregate + a window function, all in SQL on the DataFrame.
result = duckdb.sql("""
    WITH monthly AS (
        SELECT
            region,
            date_trunc('month', order_date) AS month,
            SUM(amount)                     AS revenue
        FROM orders
        GROUP BY region, date_trunc('month', order_date)
    )
    SELECT
        region,
        month,
        revenue,
        revenue - LAG(revenue) OVER (PARTITION BY region ORDER BY month)
            AS mom_change      -- month-over-month change (window function)
    FROM monthly
    ORDER BY region, month
""").df()

print("=" * 60)
print(result.to_string(index=False))
print("=" * 60)
print("DuckDB ran a GROUP BY + window function on a pandas DataFrame -- no server,")
print("no copy. Point it at 'data/*.parquet' the same way for real datasets.")
