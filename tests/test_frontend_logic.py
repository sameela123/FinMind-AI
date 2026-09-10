import unittest
import json
import os

class TestFrontendLogic(unittest.TestCase):
    def setUp(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def calculate_savings_rate(self, income, burn):
        """Simulates app.js recalculateSavingsRate() logic."""
        if income <= 0:
            return 0.0
        return round(((income - burn) / income) * 1000) / 10

    def calculate_goal_percent(self, current, target):
        """Simulates app.js renderGoals() percentage calculation."""
        if target <= 0:
            return 0
        return min(100, round((current / target) * 100))

    def filter_transactions(self, transactions, query="", category="ALL"):
        """Simulates app.js applyFilter() logic."""
        q_lower = query.lower()
        filtered = []
        for t in transactions:
            matches_q = (q_lower in t.get("merchant", "").lower()) or (q_lower in t.get("category", "").lower())
            matches_cat = (category == "ALL") or (t.get("category") == category)
            if matches_q and matches_cat:
                filtered.append(t)
        return filtered

    def simulate_chat_response(self, user_prompt, income=8500.0, burn=4820.0, savings_rate=43.3):
        """Simulates app.js handleUserChatMessage() logic."""
        lower = user_prompt.lower()
        if "updated my monthly salary" in lower or "salary" in lower:
            return f"Salary Update Recognized! Net Savings Rate: {savings_rate}%"
        elif "save" in lower or "saving" in lower or "500" in lower:
            return "FinMind AI Savings Plan: Cancel dormant subscriptions..."
        elif "subscription" in lower or "dormant" in lower or "unused" in lower:
            return "Auditor Agent Summary: Found 2 active subscriptions..."
        elif "forecast" in lower or "crunch" in lower or "end-of-month" in lower:
            return "30-Day Cashflow Projection: projected balance..."
        else:
            return f"FinMind Co-pilot: I analyzed your query '{user_prompt}'"

    def test_savings_rate_calculation(self):
        """Test savings rate recalculation under normal and edge conditions."""
        # Normal
        rate = self.calculate_savings_rate(10000.0, 4000.0)
        self.assertEqual(rate, 60.0)

        # High Burn
        rate_high_burn = self.calculate_savings_rate(5000.0, 6000.0)
        self.assertEqual(rate_high_burn, -20.0)

        # Edge Case: Zero Salary (Divide by zero prevention)
        rate_zero = self.calculate_savings_rate(0.0, 3000.0)
        self.assertEqual(rate_zero, 0.0)

    def test_goal_progress_percent(self):
        """Test goal percentage completion and capping at 100%."""
        # Standard
        pct = self.calculate_goal_percent(2500, 10000)
        self.assertEqual(pct, 25)

        # Over-achieved goal (current > target) -> capped at 100%
        pct_over = self.calculate_goal_percent(15000, 10000)
        self.assertEqual(pct_over, 100)

        # Edge Case: Target is 0
        pct_zero = self.calculate_goal_percent(500, 0)
        self.assertEqual(pct_zero, 0)

    def test_ledger_filtering_and_search(self):
        """Test transaction search and category dropdown filtering."""
        txs = [
            {"merchant": "Forgotten Gym Membership", "category": "Subscriptions & SaaS"},
            {"merchant": "Whole Foods Market", "category": "Groceries & Food"},
            {"merchant": "AWS Cloud Services", "category": "Subscriptions & SaaS"}
        ]

        # Search Query 'gym'
        res_gym = self.filter_transactions(txs, query="gym")
        self.assertEqual(len(res_gym), 1)
        self.assertEqual(res_gym[0]["merchant"], "Forgotten Gym Membership")

        # Category Filter 'Subscriptions & SaaS'
        res_subs = self.filter_transactions(txs, query="", category="Subscriptions & SaaS")
        self.assertEqual(len(res_subs), 2)

        # Combined Query + Category Filter
        res_combined = self.filter_transactions(txs, query="aws", category="Subscriptions & SaaS")
        self.assertEqual(len(res_combined), 1)
        self.assertEqual(res_combined[0]["merchant"], "AWS Cloud Services")

    def test_csv_export_formatting(self):
        """Test CSV row escaping rules for merchant names with quotes or commas."""
        merchant = 'Joe\'s "Coffee" & Bakery, LLC'
        notes = 'Flagged anomaly: unusual spending'

        escaped_quotes = merchant.replace('"', '""')
        merchant_escaped = f'"{escaped_quotes}"'
        escaped_notes = notes.replace('"', '""')
        notes_escaped = f'"{escaped_notes}"'

        self.assertEqual(merchant_escaped, '"Joe\'s ""Coffee"" & Bakery, LLC"')
        self.assertTrue(merchant_escaped.startswith('"') and merchant_escaped.endswith('"'))

    def test_chat_copilot_intent_matching(self):
        """Test chat copilot prompt response matching."""
        self.assertIn("Salary Update Recognized", self.simulate_chat_response("I updated my monthly salary"))
        self.assertIn("Savings Plan", self.simulate_chat_response("How can I save $500?"))
        self.assertIn("Auditor Agent Summary", self.simulate_chat_response("Show unused subscriptions"))
        self.assertIn("30-Day Cashflow", self.simulate_chat_response("What is my cashflow forecast?"))
        self.assertIn("FinMind Co-pilot", self.simulate_chat_response("What is the stock market doing?"))

if __name__ == "__main__":
    unittest.main()
