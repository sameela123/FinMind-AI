import os
import json
import csv

# FinMind AI CSV Generator for BigQuery Sandbox Free Upload
def export_csv():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    if not os.path.exists(data_path):
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    csv_path = os.path.join(os.path.dirname(__file__), "transactions.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["transaction_id", "date", "amount", "type", "category", "merchant", "is_recurring", "is_anomaly", "notes"])

        for t in data.get("transactions", []):
            writer.writerow([
                t["id"],
                t["date"],
                t["amount"],
                t["type"],
                t["category"],
                t["merchant"],
                t["is_recurring"],
                t["is_anomaly"],
                t.get("notes", "")
            ])

    print(f"Exported clean CSV for BigQuery Sandbox upload: {os.path.abspath(csv_path)}")

if __name__ == "__main__":
    export_csv()
