import unittest
import os
import json
import re
from datetime import datetime
from backend.push_to_bigquery import generate_bigquery_sql_script

class TestDataIntegrity(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
        self.assertTrue(os.path.exists(self.data_path), f"data.json not found at {self.data_path}")
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def test_gcp_project_and_dataset_ids(self):
        """Verify GCP Project ID and BigQuery Dataset ID strictly adhere to specs."""
        self.assertEqual(self.data.get("project_id"), "velvety-mason-417105")
        self.assertEqual(self.data.get("dataset_id"), "finmind_analytics")

    def test_financial_kpi_metrics(self):
        """Validate presence and reasonable numeric ranges for top-level KPIs."""
        self.assertIn("current_balance", self.data)
        self.assertIn("monthly_income", self.data)
        self.assertIn("monthly_burn", self.data)
        self.assertIn("savings_rate", self.data)

        self.assertIsInstance(self.data["current_balance"], (int, float))
        self.assertIsInstance(self.data["monthly_income"], (int, float))
        self.assertIsInstance(self.data["monthly_burn"], (int, float))
        self.assertGreater(self.data["monthly_income"], 0)
        self.assertGreater(self.data["monthly_burn"], 0)

        # Verify savings rate calculation consistency
        calc_savings = round(((self.data["monthly_income"] - self.data["monthly_burn"]) / self.data["monthly_income"]) * 100, 1)
        self.assertAlmostEqual(self.data["savings_rate"], calc_savings, delta=0.5)

    def test_transactions_schema_and_uniqueness(self):
        """Validate transaction records, unique transaction IDs, and date formats."""
        transactions = self.data.get("transactions", [])
        self.assertGreater(len(transactions), 0, "Transactions array should not be empty")

        txn_ids = set()
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

        for txn in transactions:
            self.assertIn("id", txn)
            self.assertNotIn(txn["id"], txn_ids, f"Duplicate transaction ID found: {txn['id']}")
            txn_ids.add(txn["id"])

            self.assertIn("date", txn)
            self.assertTrue(date_pattern.match(txn["date"]), f"Invalid date format in txn {txn['id']}: {txn['date']}")

            self.assertIn("amount", txn)
            self.assertGreaterEqual(txn["amount"], 0, f"Negative transaction amount in txn {txn['id']}")

            self.assertIn("type", txn)
            self.assertIn(txn["type"], ["INCOME", "EXPENSE"], f"Invalid transaction type in txn {txn['id']}")

            self.assertIn("category", txn)
            self.assertIn("merchant", txn)

    def test_forecasts_structure(self):
        """Validate 30-day forecast entries and risk levels."""
        forecasts = self.data.get("forecasts", [])
        self.assertEqual(len(forecasts), 30, "Forecasts should contain 30 daily predictions")

        valid_risks = {"LOW", "MEDIUM", "HIGH"}
        for f in forecasts:
            self.assertIn("date", f)
            self.assertIn("predicted_balance", f)
            self.assertIn("risk_level", f)
            self.assertIn(f["risk_level"], valid_risks, f"Invalid risk level: {f['risk_level']}")

    def test_goals_structure(self):
        """Validate financial goal vaults structure."""
        goals = self.data.get("goals", [])
        self.assertGreater(len(goals), 0, "Goals list should contain goal vault items")

        for g in goals:
            self.assertIn("id", g)
            self.assertIn("title", g)
            self.assertIn("target_amount", g)
            self.assertIn("current_amount", g)
            self.assertIn("monthly_contribution", g)
            self.assertGreater(g["target_amount"], 0)
            self.assertGreaterEqual(g["current_amount"], 0)

    def test_bigquery_sql_generator(self):
        """Test BigQuery SQL script generator tool."""
        generate_bigquery_sql_script()
        sql_path = os.path.join(os.path.dirname(__file__), "..", "backend", "populate_bigquery.sql")
        self.assertTrue(os.path.exists(sql_path), "populate_bigquery.sql should be generated")

        with open(sql_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("CREATE SCHEMA IF NOT EXISTS `velvety-mason-417105.finmind_analytics`", content)
        self.assertIn("CREATE TABLE IF NOT EXISTS `velvety-mason-417105.finmind_analytics.finmind_transactions`", content)
        self.assertIn("INSERT INTO `velvety-mason-417105.finmind_analytics.finmind_transactions`", content)

if __name__ == "__main__":
    unittest.main()
