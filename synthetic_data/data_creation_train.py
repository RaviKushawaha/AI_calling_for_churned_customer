import numpy as np
import pandas as pd

np.random.seed(42)

NUM_CUSTOMERS = 5000
AOV_THRESHOLD = 600  # for churn rule (₹)
today = pd.Timestamp.today().normalize()

# ---------------------------
# 1) CUSTOMER PROFILE TABLE
# ---------------------------
customer_id = np.arange(1, NUM_CUSTOMERS + 1)

def random_phone(n):
    # Indian-style: start with 9,10,8,7 etc. Simple synthetic version
    starts = np.random.choice(['9', '8', '7'], size=n)
    rest = np.random.randint(0, 10, size=(n, 9))
    return np.array(["".join([s] + list(map(str, r))) for s, r in zip(starts, rest)])

customer_profile = pd.DataFrame({
    "customer_id": customer_id,
    "phone_number": random_phone(NUM_CUSTOMERS),
    "email_id": [f"customer{cid}@example.com" for cid in customer_id],
    "age": np.random.randint(18, 60, size=NUM_CUSTOMERS),
    "gender": np.random.choice(["Male", "Female", "Other"],
                               size=NUM_CUSTOMERS,
                               p=[0.48, 0.48, 0.04]),
    "city_tier": np.random.choice([1, 2, 3],
                                  size=NUM_CUSTOMERS,
                                  p=[0.3, 0.4, 0.3]),
    "acquisition_channel": np.random.choice(
        ["Instagram", "Google Ads", "Organic", "Influencer", "Referral"],
        size=NUM_CUSTOMERS,
        p=[0.3, 0.25, 0.25, 0.1, 0.1]
    )
})

days_as_customer = np.random.randint(30, 730, size=NUM_CUSTOMERS)  # between 1 month & 2 years

# ---------------------------
# 2) PURCHASE BEHAVIOR TABLE
# ---------------------------
# total_orders: more low-order than high-order customers
total_orders = np.random.poisson(lam=3, size=NUM_CUSTOMERS) + 1
total_orders = np.clip(total_orders, 1, 25)

# avg_order_value: around ₹700 with some spread
avg_order_value = np.random.normal(loc=700, scale=150, size= NUM_CUSTOMERS)
avg_order_value = np.clip(avg_order_value, 250, 1500)

# days since last purchase (more orders -> usually more recent)
base_recency = np.random.exponential(scale=120, size=NUM_CUSTOMERS)
days_since_last_purchase = (base_recency * (6 / (total_orders + 3))).astype(int)
days_since_last_purchase = np.clip(days_since_last_purchase, 0, days_as_customer)

# days between orders ~ tenure / total_orders (with noise)
days_between_orders_avg = (days_as_customer / total_orders) + np.random.normal(0, 5, NUM_CUSTOMERS)
days_between_orders_avg = np.clip(days_between_orders_avg, 1, 365)

# last_order_value ~ around avg_order_value
last_order_value = avg_order_value * (1 + np.random.normal(0, 0.2, NUM_CUSTOMERS))
last_order_value = np.clip(last_order_value, 200, 2000)

# sku_diversity: unique products <= total_orders
sku_diversity = np.minimum(total_orders, np.random.randint(1, 10, size=NUM_CUSTOMERS))

# return_rate: mostly low, Beta distribution
return_rate = np.random.beta(a=1, b=10, size=NUM_CUSTOMERS)

# churn rule:
# churned = 1 if days_since_last_purchase > 90 AND total_orders > 3 AND avg_order_value < AOV_THRESHOLD
churned = (
    (days_since_last_purchase > 90) &
    (total_orders > 3) &
    (avg_order_value < AOV_THRESHOLD)
).astype(int)

purchase_behavior = pd.DataFrame({
    "customer_id": customer_id,
    "total_orders": total_orders,
    "avg_order_value": avg_order_value.round(2),
    "last_order_value": last_order_value.round(2),
    "days_since_last_purchase": days_since_last_purchase,
    "days_between_orders_avg": days_between_orders_avg.round(1),
    "sku_diversity": sku_diversity,
    "return_rate": return_rate.round(3),
    "churned": churned
})

# ---------------------------
# 3) CUSTOMER SUPPORT / EXPERIENCE TABLE
# ---------------------------
# more recent, engaged customers may have more tickets
# but keep rates low overall
complaints_last_6_months = np.random.poisson(
    lam=np.where(days_since_last_purchase <= 180, 0.15, 0.05)
)
support_tickets_last_6_months = np.random.poisson(
    lam=np.where(days_since_last_purchase <= 180, 0.5, 0.2)
)

# rating distribution skewed to 4 and 5
rating_last_purchase = np.random.choice(
    [1, 2, 3, 4, 5],
    size=NUM_CUSTOMERS,
    p=[0.05, 0.1, 0.2, 0.35, 0.3]
)

# NPS-like 0–10
NPS_score = np.random.choice(
    np.arange(0, 11),
    size=NUM_CUSTOMERS,
    p=[0.02, 0.03, 0.05, 0.07, 0.08, 0.15, 0.15, 0.17, 0.13, 0.1, 0.05]
)

customer_support = pd.DataFrame({
    "customer_id": customer_id,
    "complaints_last_6_months": complaints_last_6_months,
    "support_tickets_last_6_months": support_tickets_last_6_months,
    "rating_last_purchase": rating_last_purchase,
    "NPS_score": NPS_score
})

# save to CSVs
customer_profile.to_csv("customer_profile.csv", index=False)
purchase_behavior.to_csv("purchase_behavior.csv", index=False)
customer_support.to_csv("customer_support.csv", index=False)

