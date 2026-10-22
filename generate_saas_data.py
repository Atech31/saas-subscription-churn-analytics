import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

print("-> Generating Complete SaaS Subscription Dataset...")

# 1. Generate Customers
n_customers = 500
start_date_range = datetime(2024, 1, 1)

customer_ids = [f"CUST_{i:04d}" for i in range(1, n_customers + 1)]
signup_dates = [start_date_range + timedelta(days=int(np.random.randint(0, 600))) for _ in range(n_customers)]
signup_dates.sort()

industries = np.random.choice(['FinTech', 'HealthTech', 'EdTech', 'E-Commerce', 'SaaS B2B'], size=n_customers, p=[0.25, 0.20, 0.15, 0.20, 0.20])
countries = np.random.choice(['USA', 'UK', 'Germany', 'Canada', 'Australia'], size=n_customers, p=[0.4, 0.2, 0.15, 0.15, 0.1])
company_sizes = np.random.choice(['Startup (1-10)', 'SMB (11-50)', 'Mid-Market (51-200)', 'Enterprise (200+)'], size=n_customers, p=[0.4, 0.3, 0.2, 0.1])

df_customers = pd.DataFrame({
    'customer_id': customer_ids,
    'signup_date': signup_dates,
    'industry': industries,
    'country': countries,
    'company_size': company_sizes
})

# 2. Generate Subscriptions & MRR
plans = {
    'Basic': 49,
    'Pro': 199,
    'Enterprise': 699
}

subscription_records = []
sub_id_counter = 1

for idx, row in df_customers.iterrows():
    cust_id = row['customer_id']
    s_date = row['signup_date']
    
    plan = np.random.choice(['Basic', 'Pro', 'Enterprise'], p=[0.5, 0.35, 0.15])
    mrr = plans[plan]
    
    is_churned = np.random.choice([True, False], p=[0.22, 0.78])
    if is_churned:
        churn_duration = int(np.random.randint(30, 450))
        e_date = s_date + timedelta(days=churn_duration)
        if e_date > datetime(2026, 10, 1):
            e_date = None
            status = 'Active'
        else:
            status = 'Churned'
    else:
        e_date = None
        status = 'Active'
        
    subscription_records.append({
        'subscription_id': f"SUB_{sub_id_counter:05d}",
        'customer_id': cust_id,
        'plan_tier': plan,
        'mrr_amount': mrr,
        'start_date': s_date,
        'end_date': e_date,
        'status': status
    })
    sub_id_counter += 1

df_subscriptions = pd.DataFrame(subscription_records)

# 3. Generate Monthly Invoices
invoice_records = []
inv_counter = 1

for idx, sub in df_subscriptions.iterrows():
    cust_id = sub['customer_id']
    sub_id = sub['subscription_id']
    mrr = sub['mrr_amount']
    start = sub['start_date']
    end = sub['end_date'] if pd.notnull(sub['end_date']) else datetime(2026, 10, 1)
    
    curr_date = start.replace(day=1)
    while curr_date <= end and curr_date < datetime(2026, 10, 1):
        payment_status = np.random.choice(['Paid', 'Failed', 'Refunded'], p=[0.92, 0.06, 0.02])
        invoice_records.append({
            'invoice_id': f"INV_{inv_counter:06d}",
            'customer_id': cust_id,
            'subscription_id': sub_id,
            'invoice_date': curr_date,
            'amount_due': mrr,
            'payment_status': payment_status
        })
        inv_counter += 1
        # Move to next month
        if curr_date.month == 12:
            curr_date = curr_date.replace(year=curr_date.year + 1, month=1)
        else:
            curr_date = curr_date.replace(month=curr_date.month + 1)

df_invoices = pd.DataFrame(invoice_records)

# 4. Generate Product Usage Metrics (for Churn Prediction later)
usage_records = []
usage_counter = 1

for cust_id in df_customers['customer_id']:
    # Generate weekly or monthly activity logs per customer
    for month_offset in range(0, 12):
        log_date = datetime(2025, 1, 1) + timedelta(days=30 * month_offset)
        logins = int(np.random.poisson(lam=25))
        features_used = int(np.random.randint(1, 10))
        support_tickets = int(np.random.choice([0, 1, 2, 3], p=[0.7, 0.2, 0.08, 0.02]))
        
        usage_records.append({
            'usage_id': f"USG_{usage_counter:06d}",
            'customer_id': cust_id,
            'log_date': log_date,
            'logins_count': logins,
            'features_used_count': features_used,
            'support_tickets_open': support_tickets
        })
        usage_counter += 1

df_usage = pd.DataFrame(usage_records)

# Save all tables to CSV
df_customers.to_csv('dim_customers.csv', index=False)
df_subscriptions.to_csv('fact_subscriptions.csv', index=False)
df_invoices.to_csv('fact_invoices.csv', index=False)
df_usage.to_csv('fact_usage_metrics.csv', index=False)

print("-> Success! Generated all 4 SaaS relational CSV files (`dim_customers`, `fact_subscriptions`, `fact_invoices`, `fact_usage_metrics`).")