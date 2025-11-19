# AI_calling_for_churned_customer
Email or call the churned customers

# Synthetic Customer Churn Dataset (D2C Skincare Brand)

A comprehensive synthetic dataset generator for customer churn prediction in a Direct-to-Consumer (D2C) skincare brand context, inspired by brands like Minimalist.

## 📋 Overview

This project generates realistic synthetic customer data that can be used for:
- Building and testing churn prediction models
- Customer behavior analysis
- Retention strategy development
- ML/Data Science training and experimentation

## 🗂️ Dataset Structure

The generated dataset is split across three CSV files:

### 1. **customer_profile.csv**
Core demographic and acquisition information:
- `customer_id` - Unique customer identifier
- `phone_number` - Customer contact number
- `email_id` - Customer email address
- `age` - Customer age
- `gender` - Customer gender
- `city_tier` - City classification (Tier 1, 2, or 3)
- `acquisition_channel` - How the customer was acquired (e.g., Social Media, Organic Search, Referral)

### 2. **purchase_behavior.csv**
Transaction and purchasing patterns:
- `customer_id` - Links to customer profile
- `total_orders` - Lifetime number of orders
- `avg_order_value` - Average order value in INR
- `last_order_value` - Most recent order value in INR
- `days_since_last_purchase` - Days since last transaction
- `days_between_orders_avg` - Average gap between orders
- `sku_diversity` - Number of unique SKUs purchased
- `return_rate` - Percentage of orders returned
- `churned` - **Target variable** (0 = Active, 1 = Churned)

### 3. **customer_support.csv**
Customer service interaction metrics:
- `customer_id` - Links to customer profile
- `complaints_last_6_months` - Number of complaints filed
- `support_tickets_last_6_months` - Total support tickets raised
- `rating_last_purchase` - Rating given on last purchase (1-5)
- `NPS_score` - Net Promoter Score (-100 to 100)

## 🎯 Churn Definition

A customer is classified as **churned** (`churned = 1`) if **ALL** of the following conditions are met:

1. `days_since_last_purchase > 90` (No purchase in last 90 days)
2. `total_orders > 3` (Has made more than 3 orders historically)
3. `avg_order_value < 600` (Low average order value)

This definition targets customers who were previously engaged but have shown signs of disengagement.

## 🚀 Getting Started

### Prerequisites
```bash
pip install pandas numpy faker
```

### Generate Dataset
```bash
python data_creation_train.py
python data_creation_test.py
```

### Output Files
After running the script, you'll find three CSV files in your working directory:
- `customer_profile.csv`
- `purchase_behavior.csv`
- `customer_support.csv`

