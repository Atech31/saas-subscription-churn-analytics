# SaaS Subscription Revenue & Churn Intelligence Platform  

A portfolio-grade data analytics and machine learning solution designed to model SaaS subscription lifecycles, track Monthly Recurring Revenue (MRR), evaluate customer engagement metrics, and predict churn risk using Python, SQLite, Scikit-Learn, and Power BI.

---

##   Executive Summary

This end-to-end project simulates a modern B2B SaaS analytics architecture. By integrating relational data engineering, machine learning predictive modeling, and executive reporting dashboards, the platform provides actionable insights into customer retention, plan tier performance, and operational churn risks.

---

##   Architecture & Data Model

The project is built around a **Star Schema** relational structure centered on `dim_customers` to maintain strict multi-table relationships and data integrity:

- **`dim_customers`** (Dimension): Central customer demographics and profiles.
- **`fact_subscriptions`** (Fact): Subscription plan tiers (*Enterprise, Pro, Basic*), billing status, and MRR.
- **`fact_invoices`** (Fact): Transactional billing dates, amount due, and payment status.
- **`fact_usage_metrics`** (Fact): Platform usage patterns, including login frequency and open support tickets.

---

##   Project Phases & Tech Stack

### 1. Synthetic Data Generation & Database Pipeline (`Python` + `SQLite`)
- Generated relational datasets mimicking realistic SaaS business operations.
- Built an automated SQLite database ingestion script (`load_to_sqlite.py`) to maintain data pipelines.

### 2. SQL Analytics & Financial Metrics (`SQL`)
- Formulated SQL queries (`calculate_saas_metrics.py`) to calculate core SaaS KPIs:
  - **MRR (Monthly Recurring Revenue)**
  - **Active vs. Churned Customer Counts**
  - **Customer Health Scores** based on usage patterns.

### 3. Machine Learning Churn Risk Prediction (`Scikit-Learn`)
- Trained a **Random Forest Classifier** (`churn_prediction_model.py`) to identify key drivers of customer churn.
- Key predictive feature importances identified:
  1. `avg_logins` (Login Frequency)
  2. `avg_features_used` (Product Adoption)
  3. `total_support_tickets` (Support Friction)

### 4. Power BI Executive Dashboard (`Power BI`)
- Modeled `1:*` star schema relationships in Power BI Desktop.
- Designed an executive report featuring:
  - **Total MRR KPI Card**
  - **Revenue Breakdown by Plan Tier** (*Enterprise, Pro, Basic*)
  - **MRR Growth Trend Over Time**
  - **High Churn Risk Customer Table** (connecting usage drop-offs to support ticket volume)

---

##   Repository Structure

```text
├── generate_saas_data.py          # Data synthesis script
├── load_to_sqlite.py              # Ingestion pipeline to SQLite
├── calculate_saas_metrics.py      # Core SQL business logic
├── churn_prediction_model.py      # Machine Learning churn model
├── saas_analytics.db              # SQLite relational database
├── SaaS_Churn_Analytics.pbix      # Power BI Desktop report
├── dim_customers.csv              # Customer dimension dataset
├── fact_subscriptions.csv         # Subscriptions fact table
├── fact_invoices.csv              # Invoices fact table
└── fact_usage_metrics.csv         # Usage metrics fact table
