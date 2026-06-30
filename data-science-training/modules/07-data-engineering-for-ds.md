# Module 7 — Data Engineering for Data Scientists

> **Why this matters:** You don't need to *be* a data engineer, but senior data
> scientists are bottlenecked far more often by data access, quality, and
> pipelines than by modeling. Speaking this language makes you self-sufficient
> and a better collaborator.

**Outcome:** you can write performant SQL, build reliable data pipelines, reason
about storage/compute trade-offs, and own your data path end-to-end.

---

## Section 1 — SQL beyond the basics

SQL is still the most important data skill. Go past `SELECT ... JOIN`:
- **Window functions** — `ROW_NUMBER`, `RANK`, `LAG/LEAD`, running aggregates,
  `PARTITION BY`. These solve most "per-group" analytics problems.
- **CTEs** (`WITH`) for readable, composable queries; recursive CTEs.
- **Query performance** — indexes, what causes full scans, `EXPLAIN`/query plans,
  predicate pushdown, avoiding `SELECT *` on wide tables.
- **Sampling & approximation** at scale (`TABLESAMPLE`, approx distinct).

Practice on realistic problems: DataLemur, StrataScratch (RESOURCES §7).

## Section 2 — The modern data stack (conceptual map)

```
Sources → Ingestion → Lake/Warehouse → Transform (dbt) → Marts → BI / ML
                                   ↑ orchestration (Airflow/Dagster/Prefect)
```

- **Warehouse** (Snowflake/BigQuery/Redshift) vs **Lake** (object storage +
  Parquet) vs **Lakehouse** (Delta/Iceberg). Know the trade-offs.
- **ELT > ETL** in the modern stack: load raw, transform in-warehouse with SQL.

## Section 3 — Transformations & analytics engineering

- **dbt** — version-controlled, tested, documented SQL transformations. The
  bronze/silver/gold (raw → cleaned → business) layering pattern.
- Treat data transforms like software: tested, reviewed, documented.

## Section 4 — Orchestration

- **Airflow / Prefect / Dagster** — schedule and monitor DAGs of tasks (ingest →
  transform → score → publish). Understand idempotency, backfills, retries, and
  dependencies. Your retraining/batch-scoring pipeline lives here.

## Section 5 — Big data processing

- **Spark / PySpark** — distributed processing when data exceeds one machine.
  Understand the partitioning model, lazy evaluation, shuffles (the expensive
  part), and when a single-node tool would actually be faster.
- **When NOT to use Spark:** most "big data" fits in memory or in DuckDB. Don't
  reach for a cluster to process 2 GB.

## Section 6 — The local-analytics superpowers

- **DuckDB** — in-process OLAP SQL engine; query Parquet/CSV/pandas at high speed
  on your laptop. Often replaces a warehouse for analysis.
- **Polars** — fast, multi-threaded DataFrames; a modern pandas alternative with
  lazy evaluation. Great for medium data.
- **Arrow / Parquet** — columnar formats; understand why columnar + compression
  makes analytics fast.

## Section 7 — Data quality & contracts

- **Validation:** `pandera` / Great Expectations / dbt tests — assert schema,
  ranges, uniqueness, freshness. Catch bad data before it reaches the model.
- **Data contracts** — agreements with upstream producers about schema and
  semantics. Senior DS push for these to stop silent breakage.
- **Idempotency & late-arriving data** — design pipelines to be safely re-runnable.

## Section 8 — Streaming (awareness level)

- **Kafka / Kinesis / Flink** — for real-time data. You should understand the
  concepts (event streams, consumers, exactly-once vs at-least-once) even if you
  don't build them, because real-time features depend on them.

---

## Thinking questions
1. Write a window-function query for "each user's 3rd purchase."
2. Your query is slow. Walk through how you'd diagnose and fix it.
3. When would you choose DuckDB over Spark? Over a warehouse?
4. How do you prevent an upstream schema change from silently breaking your model?

## Deliverable
Build a small end-to-end pipeline: ingest raw data → transform with SQL/dbt or
Polars → validate with pandera/GE → produce a clean feature table, orchestrated
(even a simple scheduled script) and reproducible.

## Go deeper
RESOURCES §7. Priorities: *Fundamentals of Data Engineering*, dbt docs, DuckDB &
Polars docs, DataLemur for SQL, awesome-data-engineering.
