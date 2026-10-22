import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

print("--- Phase 3: Building SaaS Churn Prediction Model ---")

# 1. Connect to SQLite and extract aggregated customer behavior data
conn = sqlite3.connect('saas_analytics.db')

query = """
SELECT 
    s.customer_id,
    s.plan_tier,
    CASE WHEN s.status = 'Churned' THEN 1 ELSE 0 END AS is_churned,
    AVG(u.logins_count) AS avg_logins,
    AVG(u.features_used_count) AS avg_features_used,
    SUM(u.support_tickets_open) AS total_support_tickets
FROM fact_subscriptions s
JOIN fact_usage_metrics u ON s.customer_id = u.customer_id
GROUP BY s.customer_id, s.plan_tier, s.status;
"""

df_model = pd.read_sql(query, conn)
conn.close()

# 2. Preprocess data (One-Hot Encoding for Plan Tiers)
df_encoded = pd.get_dummies(df_model, columns=['plan_tier'], drop_first=True)

X = df_encoded.drop(columns=['customer_id', 'is_churned'])
y = df_encoded['is_churned']

# 3. Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate the Model
y_pred = model.predict(X_test)
print(f"\nModel Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# 6. Feature Importances (What drives churn?)
importances = pd.DataFrame({
    'Feature': X.columns,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\nTop Churn Drivers (Feature Importances):")
print(importances)