-- ============================================================================
-- Example SQL — the patterns that show up constantly in DS work & interviews
-- Dialect: ANSI / works in Postgres, DuckDB, Snowflake, BigQuery (minor tweaks)
-- ============================================================================

-- Sample schema (for reference)
--   customers(customer_id, name, signup_date, region)
--   orders(order_id, customer_id, amount, order_date, status)

-- ----------------------------------------------------------------------------
-- 1) Aggregation + HAVING: regions with more than 100 completed orders
-- ----------------------------------------------------------------------------
SELECT region, COUNT(*) AS completed_orders, SUM(amount) AS revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
GROUP BY region
HAVING COUNT(*) > 100
ORDER BY revenue DESC;

-- ----------------------------------------------------------------------------
-- 2) Window function: each customer's 2nd-largest order (top-N per group)
-- ----------------------------------------------------------------------------
WITH ranked AS (
    SELECT
        customer_id,
        order_id,
        amount,
        ROW_NUMBER() OVER (PARTITION BY customer_id
                           ORDER BY amount DESC) AS rnk
    FROM orders
)
SELECT customer_id, order_id, amount
FROM ranked
WHERE rnk = 2;

-- ----------------------------------------------------------------------------
-- 3) Running total: cumulative revenue by day (window frame)
-- ----------------------------------------------------------------------------
SELECT
    order_date,
    SUM(amount) AS daily_revenue,
    SUM(SUM(amount)) OVER (ORDER BY order_date
                           ROWS UNBOUNDED PRECEDING) AS cumulative_revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;

-- ----------------------------------------------------------------------------
-- 4) Cohort retention: % of each signup-month cohort still ordering N months later
-- ----------------------------------------------------------------------------
WITH cohort AS (
    SELECT customer_id, DATE_TRUNC('month', signup_date) AS cohort_month
    FROM customers
),
activity AS (
    SELECT
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) AS active_month,
        o.customer_id
    FROM cohort c
    JOIN orders o ON o.customer_id = c.customer_id
)
SELECT
    cohort_month,
    active_month,
    COUNT(DISTINCT customer_id) AS active_customers
FROM activity
GROUP BY cohort_month, active_month
ORDER BY cohort_month, active_month;

-- ----------------------------------------------------------------------------
-- 5) LAG/LEAD: month-over-month growth
-- ----------------------------------------------------------------------------
WITH monthly AS (
    SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT
    month,
    revenue,
    revenue - LAG(revenue) OVER (ORDER BY month) AS mom_change,
    ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
          / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS mom_pct
FROM monthly
ORDER BY month;
