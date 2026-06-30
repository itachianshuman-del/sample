# 10 · Data Engineering for Data Scientists

> Building the pipelines that deliver clean, reliable, timely data. You don't have
> to *be* a data engineer, but you must speak the language — bad data beats good
> models every time.

---

## 📌 What it is & why it matters

Data engineering is about moving and shaping data: ingestion, storage,
transformation, and serving — reliably and at scale. Data scientists are bottlenecked
far more often by data access and quality than by modeling. Understanding the modern
data stack makes you self-sufficient and a far better collaborator.

---

## 🧠 Core concepts

- **The modern stack:** sources → ingestion → lake/warehouse → transform (dbt) →
  marts → BI/ML, with **orchestration** (Airflow/Dagster/Prefect) tying it together.
- **Storage:** warehouse (Snowflake/BigQuery/Redshift) vs lake (object storage +
  Parquet) vs lakehouse (Delta/Iceberg).
- **ELT vs ETL** — modern stacks load raw then transform in-warehouse with SQL.
- **Transformation:** **dbt** for version-controlled, tested SQL (bronze/silver/gold layers).
- **Big data:** **Spark/PySpark** for distributed processing; partitioning,
  lazy evaluation, shuffles (the expensive part).
- **Local power tools:** **DuckDB** (fast local SQL on files), **Polars** (fast DataFrames).
- **Data quality & contracts:** schema/range/freshness checks (pandera, Great
  Expectations); idempotency; handling late-arriving data.
- **Streaming (awareness):** Kafka/Flink for real-time.

> Deep dive:
> [`data-science-training/modules/07-data-engineering-for-ds.md`](../../data-science-training/modules/07-data-engineering-for-ds.md).

---

## 📚 Best resources

### Books & courses
- **Fundamentals of Data Engineering** (Reis & Housley) — the conceptual map.
- **DataTalksClub — Data Engineering Zoomcamp** (free, hands-on, end-to-end):
  https://github.com/DataTalksClub/data-engineering-zoomcamp
- **dbt Learn** (free official courses): https://learn.getdbt.com/

### Curated lists & tools
- **awesome-data-engineering** (igorbarinov): https://github.com/igorbarinov/awesome-data-engineering
- dbt: https://github.com/dbt-labs/dbt-core · Airflow: https://airflow.apache.org/
- DuckDB: https://duckdb.org/ · Polars: https://pola.rs/ · PySpark: https://spark.apache.org/docs/latest/api/python/

---

## 💻 Code example

```python
# DuckDB: run warehouse-style SQL directly on local files (no DB server needed).
import duckdb

# Query a Parquet/CSV file as if it were a table — fast and zero-setup.
result = duckdb.sql("""
    SELECT
        region,
        COUNT(*)            AS n_orders,
        SUM(amount)         AS revenue,
        AVG(amount)         AS avg_order
    FROM 'orders.parquet'
    WHERE order_date >= '2024-01-01'
    GROUP BY region
    ORDER BY revenue DESC
""").df()                       # -> returns a pandas DataFrame
print(result)
```

---

## 🌍 Real-world use cases

- **Feature pipelines** — most production features begin as scheduled warehouse SQL (dbt).
- **Analytics/BI** — clean, modeled tables powering dashboards.
- **Batch scoring** — orchestrated pipelines that ingest → transform → score → publish.
- **Data quality gates** — stop bad upstream data from reaching models.

---

## 🛠️ Hands-on project ideas

1. Build a **bronze→silver→gold** dbt project on a sample dataset with tests.
2. Orchestrate an **Airflow DAG**: ingest → transform → validate → output.
3. Process a large dataset with **Polars lazy** or **PySpark** and add **pandera**
   data-quality checks.

---

## 🗺️ Suggested learning path

1. SQL (topic 02) → 2. Warehouse vs lake concepts → 3. dbt transformations →
4. Orchestration (Airflow) → 5. DuckDB/Polars for scale → 6. Data quality &
contracts → 7. Spark when data is truly big.
