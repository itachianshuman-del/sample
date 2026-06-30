# 02 · SQL & Databases

> The most underrated data science skill. You'll write more SQL than you expect —
> and strong SQL separates people who can self-serve data from those who can't.

---

## 📌 What it is & why it matters

SQL (Structured Query Language) is how you talk to relational databases and data
warehouses. Most company data lives in SQL-accessible stores (Postgres, MySQL,
Snowflake, BigQuery, Redshift). Before any model, you query, join, and aggregate
data with SQL. It's also one of the **most common interview topics** for DS/DA roles.

---

## 🧠 Core concepts

- **The basics:** `SELECT`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, `LIMIT`.
- **Joins:** INNER, LEFT, RIGHT, FULL, CROSS — and *why* a LEFT join can blow up
  row counts (fan-out).
- **Window functions** (the senior skill): `ROW_NUMBER`, `RANK`, `LAG`/`LEAD`,
  running totals, `PARTITION BY`. These solve "per-group" problems elegantly.
- **CTEs (`WITH`)** for readable, composable queries; recursive CTEs.
- **Subqueries** vs CTEs vs joins — and when each is clearest.
- **Performance:** indexes, `EXPLAIN`/query plans, avoiding `SELECT *`, predicate
  pushdown, why full scans happen.
- **Warehouse vs OLTP** — analytics (columnar, Snowflake/BigQuery) vs transactional.

---

## 📚 Best resources

### Practice (do this — SQL is learned by doing)
- **DataLemur** — realistic DS/DA SQL interview questions: https://datalemur.com/
- **StrataScratch** — real company SQL & Python questions.
- **SQLZoo** (free, interactive): https://sqlzoo.net/ · **Mode SQL Tutorial**:
  https://mode.com/sql-tutorial/

### Courses & videos
- **Krish Naik — SQL for Data Science** content within the
  [Grand Complete Data Science Materials](https://github.com/krishnaik06/The-Grand-Complete-Data-Science-Materials).
- **freeCodeCamp — SQL full courses** (YouTube, free, beginner→advanced).

### Reference
- **Devinterview-io/sql-interview-questions**: https://github.com/Devinterview-io/sql-interview-questions
- **DuckDB** (run SQL on local files, blazing fast): https://duckdb.org/
- **Use The Index, Luke** (indexing/performance): https://use-the-index-luke.com/

---

## 💻 Code example

```sql
-- "Each customer's 2nd-largest order" — a classic window-function pattern.
WITH ranked AS (
    SELECT
        customer_id,
        order_id,
        amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY amount DESC
        ) AS rnk
    FROM orders
)
SELECT customer_id, order_id, amount
FROM ranked
WHERE rnk = 2;

-- Running 7-day revenue total (window frame).
SELECT
    order_date,
    SUM(amount) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7d_revenue
FROM daily_revenue
ORDER BY order_date;
```

---

## 🌍 Real-world use cases

- **Self-serve analytics** — pull the exact slice of data you need without waiting on a data engineer.
- **Funnel & cohort analysis** — window functions for retention, churn, sessionization.
- **Feature pipelines** — most production features start as warehouse SQL (often via dbt).
- **Ad-hoc business questions** — "what was revenue by region last quarter, week over week?"

---

## 🛠️ Hands-on project ideas

1. Load a dataset into **DuckDB** and answer 10 business questions using only SQL
   (joins + window functions).
2. Build a **cohort retention** query (users grouped by signup month, retention by month).
3. Take a slow query, run `EXPLAIN`, add an index, and measure the improvement.

---

## 🗺️ Suggested learning path

1. SELECT/WHERE/GROUP BY → 2. All join types (+ fan-out) → 3. Window functions →
4. CTEs & subqueries → 5. Query performance & indexes → 6. Drill interview
questions on DataLemur until fluent.
