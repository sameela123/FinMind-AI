import os
import json

# FinMind AI BigQuery Data Exporter & Inspector
# Project ID: velvety-mason-417105
# Dataset: finmind_analytics

PROJECT_ID = "velvety-mason-417105"
DATASET_ID = "finmind_analytics"

def generate_bigquery_sql_script():
    """Generates standalone BigQuery SQL script to create dataset, user profile table, and insert sample transactions up to CURRENT_DATE()."""
    
    data_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sql_output_path = os.path.join(os.path.dirname(__file__), "populate_bigquery.sql")

    with open(sql_output_path, "w", encoding="utf-8") as f:
        f.write(f"-- FinMind AI BigQuery Population Script\n")
        f.write(f"-- Project: {PROJECT_ID}\n")
        f.write(f"-- Run this directly in Google Cloud Console BigQuery Query Editor\n\n")

        f.write(f"CREATE SCHEMA IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}`\n")
        f.write(f"OPTIONS(location='us-central1');\n\n")

        # User Profile & Financial Target Table
        f.write(f"CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.user_profiles` (\n")
        f.write(f"  profile_id STRING,\n")
        f.write(f"  monthly_income NUMERIC,\n")
        f.write(f"  monthly_burn NUMERIC,\n")
        f.write(f"  savings_rate NUMERIC,\n")
        f.write(f"  updated_at TIMESTAMP\n")
        f.write(f");\n\n")

        f.write(f"INSERT INTO `{PROJECT_ID}.{DATASET_ID}.user_profiles` VALUES\n")
        f.write(f"('USER-001', {data.get('monthly_income', 10000.0)}, {data.get('monthly_burn', 6500.0)}, {data.get('savings_rate', 35.0)}, CURRENT_TIMESTAMP());\n\n")

        # Transactions Table
        f.write(f"CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.finmind_transactions` (\n")
        f.write(f"  transaction_id STRING,\n")
        f.write(f"  date DATE,\n")
        f.write(f"  amount NUMERIC,\n")
        f.write(f"  type STRING,\n")
        f.write(f"  category STRING,\n")
        f.write(f"  merchant STRING,\n")
        f.write(f"  is_recurring BOOLEAN,\n")
        f.write(f"  is_anomaly BOOLEAN,\n")
        f.write(f"  notes STRING\n")
        f.write(f");\n\n")

        # Insert batch transactions
        txs = data.get("transactions", [])[:30] # Top 30
        f.write(f"INSERT INTO `{PROJECT_ID}.{DATASET_ID}.finmind_transactions` VALUES\n")
        
        values = []
        # Add a specific transaction for CURRENT_DATE() today!
        values.append("('TXN-TODAY-001', CURRENT_DATE(), 18.50, 'EXPENSE', 'Dining out & Entertainment', 'Starbucks Morning Coffee', FALSE, FALSE, 'Today live transaction')")
        values.append("('TXN-TODAY-002', CURRENT_DATE(), 145.20, 'EXPENSE', 'Groceries & Food', 'Whole Foods Organic Groceries', FALSE, FALSE, 'Today live transaction')")

        for t in txs:
            merchant_escaped = t['merchant'].replace("'", "\\'")
            notes_escaped = t.get('notes', '').replace("'", "\\'")
            val = f"('{t['id']}', DATE('{t['date']}'), {t['amount']}, '{t['type']}', '{t['category']}', '{merchant_escaped}', {str(t['is_recurring']).upper()}, {str(t['is_anomaly']).upper()}, '{notes_escaped}')"
            values.append(val)

        f.write(",\n".join(values) + ";\n")

    print(f"Generated BigQuery SQL script: {os.path.abspath(sql_output_path)}")

if __name__ == "__main__":
    generate_bigquery_sql_script()
