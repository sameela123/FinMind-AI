import unittest
import os
import json
import tempfile
from backend.agent_engine import FinMindAgentEngine

class TestFinMindAgentEngine(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
        self.engine = FinMindAgentEngine(data_path=self.data_path)

    def test_expense_auditor_standard(self):
        """Test Expense Auditor Agent on standard dataset."""
        result = self.engine.run_expense_auditor()
        self.assertEqual(result["agent"], "Expense Auditor Agent")
        self.assertEqual(result["status"], "ACTIVE")
        self.assertGreater(result["anomalies_detected"], 0)
        self.assertIn("z_score_outliers", result)
        self.assertIsInstance(result["annual_potential_savings"], (int, float))
        self.assertIn("Audited", result["summary"])

    def test_expense_auditor_empty_data(self):
        """Edge Case: Test Expense Auditor Agent with empty data file."""
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8") as f:
            json.dump({}, f)
            temp_name = f.name
        try:
            empty_engine = FinMindAgentEngine(data_path=temp_name)
            res = empty_engine.run_expense_auditor()
            self.assertEqual(res["anomalies_detected"], 0)
            self.assertEqual(res["annual_potential_savings"], 0.0)
            self.assertEqual(len(res["unused_subscriptions"]), 0)
        finally:
            os.remove(temp_name)

    def test_expense_auditor_malformed_transactions(self):
        """Edge Case: Test Expense Auditor Agent with missing fields in transactions."""
        dummy_data = {
            "transactions": [
                {"id": "T1", "amount": 100}, # Missing category, is_anomaly, is_recurring
                {"id": "T2", "amount": 50, "category": "Subscriptions & SaaS", "is_recurring": True, "merchant": "Gym Sub"},
                {"id": "T3", "amount": 200, "is_anomaly": True}
            ]
        }
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8") as f:
            json.dump(dummy_data, f)
            temp_name = f.name
        try:
            engine = FinMindAgentEngine(data_path=temp_name)
            res = engine.run_expense_auditor()
            self.assertEqual(res["anomalies_detected"], 1)
            self.assertEqual(res["annual_potential_savings"], 600.0) # 50 * 12
        finally:
            os.remove(temp_name)

    def test_cash_flow_predictor_standard(self):
        """Test Cash Flow Predictor Agent on standard dataset."""
        res = self.engine.run_cash_flow_predictor()
        self.assertEqual(res["agent"], "Cash Flow Predictor Agent")
        self.assertEqual(res["status"], "ACTIVE")
        self.assertEqual(res["forecast_days"], 30)
        self.assertGreater(res["current_balance"], 0)
        self.assertLessEqual(res["lowest_projected_balance"], res["current_balance"])

    def test_cash_flow_predictor_negative_balance(self):
        """Edge Case: Test Cash Flow Predictor Agent when balance dips into high risk."""
        dummy_data = {
            "current_balance": 500.0,
            "forecasts": [
                {"date": "2026-09-01", "predicted_balance": 100.0, "risk_level": "HIGH"},
                {"date": "2026-09-02", "predicted_balance": -150.0, "risk_level": "HIGH"}
            ]
        }
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8") as f:
            json.dump(dummy_data, f)
            temp_name = f.name
        try:
            engine = FinMindAgentEngine(data_path=temp_name)
            res = engine.run_cash_flow_predictor()
            self.assertEqual(res["high_risk_alerts"], 2)
            self.assertEqual(res["lowest_projected_balance"], -150.0)
        finally:
            os.remove(temp_name)

    def test_scenario_simulator_engine(self):
        """Test What-If Scenario simulation calculation logic."""
        res = self.engine.run_scenario_simulation(major_purchase=10000.0, monthly_expense_delta=500.0, income_delta=1000.0)
        self.assertIn("adjusted_balance", res)
        self.assertEqual(res["scenario"]["major_purchase"], 10000.0)
        self.assertIn("projected_30d_balance", res)
        self.assertIn("risk_level", res)

        # Critical scenario test (draining balance)
        res_critical = self.engine.run_scenario_simulation(major_purchase=50000.0, monthly_expense_delta=10000.0)
        self.assertEqual(res_critical["risk_level"], "CRITICAL (Cash Deficit)")

    def test_wealth_advisor_fallback_queries(self):
        """Test Wealth Advisor fallback agent responses for various user prompt intents."""
        # Scenario Query
        scenario_res = self.engine.query_wealth_advisor_agent("What if I buy a car for $15,000?")
        self.assertIn("scenario engine", scenario_res["response"].lower())

        # Savings Query
        savings_res = self.engine.query_wealth_advisor_agent("How can I save more money?")
        self.assertIn("savings rate", savings_res["response"].lower())

        # Investment Query
        invest_res = self.engine.query_wealth_advisor_agent("What is my investment strategy?")
        self.assertIn("index funds", invest_res["response"].lower())

        # Forecast Query
        forecast_res = self.engine.query_wealth_advisor_agent("Will I face a cash crunch next month?")
        self.assertIn("forecast", forecast_res["response"].lower())

        # Generic / Unknown Query
        generic_res = self.engine.query_wealth_advisor_agent("Tell me a random tip")
        self.assertIn("finmind ai co-pilot", generic_res["response"].lower())

    def test_wealth_advisor_empty_and_special_prompts(self):
        """Edge Case: Test Wealth Advisor handling empty or special character inputs."""
        res_empty = self.engine.query_wealth_advisor_agent("")
        self.assertIn("response", res_empty)
        
        res_special = self.engine.query_wealth_advisor_agent("<script>alert('test')</script> %$$#")
        self.assertIn("response", res_special)

if __name__ == "__main__":
    unittest.main()
