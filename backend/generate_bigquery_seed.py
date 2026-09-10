import os
import json

# FinMind AI Complete BigQuery Seed Generator
# Project ID: velvety-mason-417105
# Dataset: finmind_analytics

PROJECT_ID = "velvety-mason-417105"
DATASET_ID = "finmind_analytics"

def generate_bigquery_sql_seed():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sql_output_path = os.path.join(os.path.dirname(__file__), "populate_all_bigquery.sql")

    with open(sql_output_path, "w", encoding="utf-8") as f:
        f.write(f"-- FinMind AI Complete BigQuery Setup Script\n")
        f.write(f"-- Project ID: {PROJECT_ID}\n")
        f.write(f"-- Copy & Paste this entire script into BigQuery Console Query Editor\n\n")

        # 1. Create Dataset Schema
        f.write(f"CREATE SCHEMA IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}`\n")
        f.write(f"OPTIONS(location='us-central1');\n\n")

        # 2. Table 1: finmind_transactions
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

        txs = data.get("transactions", [])[:40]
        if txs:
            f.write(f"INSERT INTO `{PROJECT_ID}.{DATASET_ID}.finmind_transactions` VALUES\n")
            tx_values = []
            for t in txs:
                merchant_escaped = t['merchant'].replace("'", "\\'")
                notes_escaped = t.get('notes', '').replace("'", "\\'")
                val = f"('{t['id']}', DATE('{t['date']}'), {t['amount']}, '{t['type']}', '{t['category']}', '{merchant_escaped}', {str(t['is_recurring']).upper()}, {str(t['is_anomaly']).upper()}, '{notes_escaped}')"
                tx_values.append(val)
            f.write(",\n".join(tx_values) + ";\n\n")

        # 3. Table 2: finmind_forecasts
        f.write(f"CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.finmind_forecasts` (\n")
        f.write(f"  forecast_date DATE,\n")
        f.write(f"  predicted_balance NUMERIC,\n")
        f.write(f"  risk_level STRING\n")
        f.write(f");\n\n")

        forecasts = data.get("forecasts", [])
        if forecasts:
            f.write(f"INSERT INTO `{PROJECT_ID}.{DATASET_ID}.finmind_forecasts` VALUES\n")
            fc_values = []
            for fc in forecasts:
                val = f"(DATE('{fc['date']}'), {fc['predicted_balance']}, '{fc['risk_level']}')"
                fc_values.append(val)
            f.write(",\n".join(fc_values) + ";\n\n")

        # 4. Table 3: finmind_categories
        f.write(f"CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.finmind_categories` (\n")
        f.write(f"  category_name STRING,\n")
        f.write(f"  monthly_budget NUMERIC,\n")
        f.write(f"  color_code STRING\n")
        f.write(f");\n\n")

        categories = data.get("categories", [])
        if categories:
            f.write(f"INSERT INTO `{PROJECT_ID}.{DATASET_ID}.finmind_categories` VALUES\n")
            cat_values = []
            for c in categories:
                val = f"('{c['name']}', {c['budget']}, '{c['color']}')"
                cat_values.append(val)
            f.write(",\n".join(cat_values) + ";\n")

    print(f"Successfully generated complete BigQuery seed script at: {os.path.abspath(sql_output_path)}")

if __name__ == "__main__":
    generate_bigquery_sql_seed()
