import os
import json
import random
import datetime

# FinMind AI Synthetic Financial Ledger & Goals Generator
PROJECT_ID = "velvety-mason-417105"
DATASET_ID = "finmind_analytics"

def generate_financial_dataset():
    print(f"Generating FinMind AI transaction dataset & goals for project {PROJECT_ID}...")
    
    categories = [
        {"name": "Salary & Income", "budget": 8500.0, "color": "#10B981"},
        {"name": "Housing & Rent", "budget": 2400.0, "color": "#6366F1"},
        {"name": "Groceries & Food", "budget": 800.0, "color": "#F59E0B"},
        {"name": "Subscriptions & SaaS", "budget": 150.0, "color": "#EF4444"},
        {"name": "Dining out & Entertainment", "budget": 450.0, "color": "#EC4899"},
        {"name": "Utilities & Bills", "budget": 350.0, "color": "#3B82F6"},
        {"name": "Travel & Rideshare", "budget": 300.0, "color": "#8B5CF6"},
        {"name": "Investments & Stocks", "budget": 1500.0, "color": "#14B8A6"}
    ]
    
    goals = [
        {
            "id": "GOAL-1",
            "title": "🏡 Home Down Payment",
            "target_amount": 50000.0,
            "current_amount": 32500.0,
            "monthly_contribution": 1250.0,
            "target_date": "2027-06-30",
            "category": "Real Estate",
            "color": "#10B981"
        },
        {
            "id": "GOAL-2",
            "title": "✈️ Europe Summer Trip",
            "target_amount": 6500.0,
            "current_amount": 4200.0,
            "monthly_contribution": 500.0,
            "target_date": "2027-05-15",
            "category": "Travel",
            "color": "#6366F1"
        },
        {
            "id": "GOAL-3",
            "title": "🛡️ 6-Month Emergency Vault",
            "target_amount": 25000.0,
            "current_amount": 21000.0,
            "monthly_contribution": 800.0,
            "target_date": "2026-12-31",
            "category": "Safety",
            "color": "#F59E0B"
        }
    ]
    
    merchants = {
        "Salary & Income": ["Tech Corp Payroll", "Consulting Direct Deposit", "Dividend Yield"],
        "Housing & Rent": ["Skyline Apartments LLC", "Property Mgmt Co"],
        "Groceries & Food": ["Whole Foods Market", "Trader Joe's", "Costco Wholesale", "Local Organic Market"],
        "Subscriptions & SaaS": ["Netflix Monthly", "Spotify Premium", "GitHub Copilot", "ChatGPT Plus", "AWS Cloud Services", "Forgotten Gym Membership"],
        "Dining out & Entertainment": ["Starbucks Coffee", "Sushi Zen Restaurant", "Chipotle Mexican Grill", "AMC Movie Theater"],
        "Utilities & Bills": ["ConEd Electric", "Verizon Fios Fiber", "City Water Authority"],
        "Travel & Rideshare": ["Uber Trip", "Lyft Ride", "Delta Air Lines", "Chevron Gas Station"],
        "Investments & Stocks": ["Vanguard S&P 500 ETF", "Fidelity Index Fund", "Robinhood Deposit"]
    }
    
    start_date = datetime.date.today() - datetime.timedelta(days=180)
    transactions = []
    
    current_balance = 12450.0
    tx_id_counter = 1000
    
    for day_offset in range(180):
        current_date = start_date + datetime.timedelta(days=day_offset)
        
        if current_date.day in (1, 15):
            tx_id_counter += 1
            salary_amt = 4250.0
            current_balance += salary_amt
            transactions.append({
                "id": f"TXN-{tx_id_counter}",
                "date": current_date.isoformat(),
                "amount": salary_amt,
                "type": "INCOME",
                "category": "Salary & Income",
                "merchant": "Tech Corp Payroll",
                "is_recurring": True,
                "is_anomaly": False,
                "notes": "Bi-weekly paycheck deposit"
            })
            
        if current_date.day == 1:
            tx_id_counter += 1
            rent_amt = 2400.0
            current_balance -= rent_amt
            transactions.append({
                "id": f"TXN-{tx_id_counter}",
                "date": current_date.isoformat(),
                "amount": rent_amt,
                "type": "EXPENSE",
                "category": "Housing & Rent",
                "merchant": "Skyline Apartments LLC",
                "is_recurring": True,
                "is_anomaly": False,
                "notes": "Monthly apartment rent payment"
            })

        if current_date.day == 5:
            for sub_merchant in ["Netflix Monthly", "Spotify Premium", "Forgotten Gym Membership", "AWS Cloud Services"]:
                tx_id_counter += 1
                cost = 14.99 if "Netflix" in sub_merchant else (9.99 if "Spotify" in sub_merchant else (49.99 if "Gym" in sub_merchant else 89.00))
                is_unused = "Gym" in sub_merchant or "AWS" in sub_merchant
                current_balance -= cost
                transactions.append({
                    "id": f"TXN-{tx_id_counter}",
                    "date": current_date.isoformat(),
                    "amount": cost,
                    "type": "EXPENSE",
                    "category": "Subscriptions & SaaS",
                    "merchant": sub_merchant,
                    "is_recurring": True,
                    "is_anomaly": is_unused,
                    "notes": "Flagged unused subscription" if is_unused else "Regular active subscription"
                })

        num_daily_tx = random.choices([0, 1, 2, 3], weights=[0.2, 0.4, 0.3, 0.1])[0]
        for _ in range(num_daily_tx):
            tx_id_counter += 1
            cat_choice = random.choice(["Groceries & Food", "Dining out & Entertainment", "Travel & Rideshare"])
            merchant_choice = random.choice(merchants[cat_choice])
            amount = round(random.uniform(5.50, 120.00), 2)
            
            is_anomaly = False
            if random.random() < 0.03:
                amount = round(random.uniform(450.00, 1200.00), 2)
                is_anomaly = True
                merchant_choice = "Luxury Goods Store" if random.random() > 0.5 else "Emergency Electronics Repair"
                cat_choice = "Dining out & Entertainment"

            current_balance -= amount
            transactions.append({
                "id": f"TXN-{tx_id_counter}",
                "date": current_date.isoformat(),
                "amount": amount,
                "type": "EXPENSE",
                "category": cat_choice,
                "merchant": merchant_choice,
                "is_recurring": False,
                "is_anomaly": is_anomaly,
                "notes": "Unusual high spending spike flagged by Auditor Agent" if is_anomaly else "Daily transaction"
            })
            
    forecast_points = []
    projected_balance = current_balance
    daily_burn_avg = 112.50
    
    for fc_day in range(1, 31):
        fc_date = datetime.date.today() + datetime.timedelta(days=fc_day)
        
        if fc_date.day in (1, 15):
            projected_balance += 4250.0
            
        if fc_date.day == 1:
            projected_balance -= 2400.0
            
        projected_balance -= daily_burn_avg
        
        risk_level = "LOW"
        if projected_balance < 3000.0:
            risk_level = "HIGH"
        elif projected_balance < 6000.0:
            risk_level = "MEDIUM"
            
        forecast_points.append({
            "date": fc_date.isoformat(),
            "predicted_balance": round(projected_balance, 2),
            "risk_level": risk_level
        })
        
    dataset = {
        "project_id": PROJECT_ID,
        "dataset_id": DATASET_ID,
        "current_balance": round(current_balance, 2),
        "monthly_income": 8500.0,
        "monthly_burn": 4820.0,
        "savings_rate": 43.3,
        "risk_score": "HEALTHY",
        "categories": categories,
        "goals": goals,
        "transactions": transactions,
        "forecasts": forecast_points
    }
    
    output_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
        
    print(f"Saved dataset with goals to {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_financial_dataset()
