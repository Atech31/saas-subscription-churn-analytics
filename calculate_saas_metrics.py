import sqlite3
import pandas as pd

# Connect to the local SaaS database
conn = sqlite3.connect('saas_analytics.db')

print("--- Calculating Advanced SaaS Metrics ---")

# 1. Monthly Churn & Growth Analysis query
churn_query = """
WITH monthly_revenue AS (
    SELECT 
        strftime('%Y-%m', invoice_date) AS inv_month,
        SUM(amount_due) AS total_mrr,
        COUNT(DISTINCT customer_id) as active_customers
    FROM fact_invoices
    WHERE payment_status = 'Paid'
    GROUP BY inv_month
)
SELECT 
    inv_month,
    total_mrr,
    active_customers,
    ROUND(total_mrr * 1.0 / active_customers, 2) AS arpu,
    LAG(total_mrr, 1) OVER (ORDER BY inv_month) AS prev_month_mrr,
    ROUND(total_mrr - LAG(total_mrr, 1) OVER (ORDER BY inv_month), 2) AS mrr_growth
FROM monthly_revenue;
"""

df_metrics = pd.read_sql(churn_query, conn)
print(df_metrics.head(12))

conn.close()