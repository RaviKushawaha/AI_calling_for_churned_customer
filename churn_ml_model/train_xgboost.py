import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import joblib

# -----------------------------
# 1. Load or use existing dataframes
# -----------------------------
customer_profile = pd.read_csv("../synthetic_data/customer_profile.csv")
purchase_behavior = pd.read_csv("../synthetic_data/purchase_behavior.csv")
customer_support = pd.read_csv("../synthetic_data/customer_support.csv")

# -----------------------------
# 2. Merge tables
# -----------------------------
df = (
    customer_profile
    .merge(purchase_behavior, on="customer_id")
    .merge(customer_support, on="customer_id")
)

df = df.drop(columns=["customer_id", "email_id", "phone_number"])


# -----------------------------
# 3. Prepare Features + Target
# -----------------------------
y = df["churned"]
X = df.drop(columns=["churned"])

X = pd.get_dummies(X, drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# -----------------------------
# 4. Train XGBoost Model
# -----------------------------
model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss"
)

model.fit(X_train, y_train)


# -----------------------------
# 5. Predictions + Probabilities
# -----------------------------
probs = model.predict_proba(X_test)[:, 1]
preds = model.predict(X_test)


# -----------------------------
# 6. Top-K Precision (Top 10%)
# -----------------------------
def top_k_precision(probabilities, true_labels, k=0.10):
    df_temp = pd.DataFrame({
        "prob": probabilities,
        "true": true_labels
    }).sort_values("prob", ascending=False)

    top_k_count = int(k * len(df_temp))
    top_k = df_temp.head(top_k_count)

    precision = top_k["true"].mean()  # proportion of actual churners
    return precision

top10_precision = top_k_precision(probs, y_test, k=0.10)
print("Top-10% Precision:", round(top10_precision, 3))


# -----------------------------
# 7. Evaluation Metrics
# -----------------------------
print(classification_report(y_test, preds))
print("AUC:", roc_auc_score(y_test, probs))


# -----------------------------
# 8. Feature Importance Plot
# -----------------------------
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
features = X.columns
n_features = len(features)
top_n = min(20, n_features)

plt.figure(figsize=(10, 6))
plt.bar(range(top_n), importances[indices][:top_n])
plt.xticks(range(top_n), features[indices][:top_n], rotation=75)
plt.title("Top Feature Importances (XGBoost)")
plt.tight_layout()

plt.savefig("model_statistics.png")

joblib.dump(model, "xgb_churn_model.pkl")
print("Model saved as xgb_churn_model.pkl")
