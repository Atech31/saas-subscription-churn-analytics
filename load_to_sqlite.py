import sqlite3
import pandas as pd

print("-> Loading SaaS CSV files into SQLite database...")

# Connect to SQLite database (creates it locally)
conn = sqlite3.connect('saas_analytics.db')

# Load CSVs into DataFrames and write to SQL tables
df_customers = pd.read_csv('dim_customers.csv')
df_subscriptions = pd.read_csv('fact_subscriptions.csv')
df_invoices = pd.read_csv('fact_invoices.csv')
df_usage = pd.read_csv('fact_usage_metrics.csv')

df_customers.to_sql('dim_customers', conn, if_exists='replace', index=False)
df_subscriptions.to_sql('fact_subscriptions', conn, if_exists='replace', index=False)
df_invoices.to_sql('fact_invoices', conn, if_exists='replace', index=False)
df_usage.to_sql('fact_usage_metrics', conn, if_exists='replace', index=False)

print("-> Success! All tables loaded into 'saas_analytics.db'.")

# Test query: Calculate Total MRR by Month from Invoices
query = """
SELECT 
    strftime('%Y-%m', invoice_date) AS invoice_month,
    SUM(amount_due) AS total_mrr,
    COUNT(DISTINCT customer_id) AS active_customers
FROM fact_invoices
WHERE payment_status = 'Paid'
GROUP BY invoice_month
ORDER BY invoice_month;
"""

df_mrr = pd.read_sql(query, conn)
print("\n--- Sample Monthly Recurring Revenue (MRR) ---")
print(df_mrr.head(10))

conn.close()