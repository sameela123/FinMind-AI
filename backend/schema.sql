-- FinMind AI: BigQuery Database Schema DDL
-- Project ID: velvety-mason-417105
-- Dataset: finmind_analytics

CREATE SCHEMA IF NOT EXISTS `velvety-mason-417105.finmind_analytics`
OPTIONS(
  location="US",
  description="FinMind AI Financial Ledger & Multi-Agent Analytics Schema"
);

-- Table 1: Financial Transactions Ledger
CREATE TABLE IF NOT EXISTS `velvety-mason-417105.finmind_analytics.finmind_transactions` (
  transaction_id STRING NOT NULL,
  account_id STRING,
  date DATE NOT NULL,
  amount NUMERIC NOT NULL,
  type STRING NOT NULL,
  category STRING NOT NULL,
  merchant STRING NOT NULL,
  is_recurring BOOLEAN DEFAULT FALSE,
  is_anomaly BOOLEAN DEFAULT FALSE,
  notes STRING
);

-- Table 2: Category Monthly Budgets
CREATE TABLE IF NOT EXISTS `velvety-mason-417105.finmind_analytics.finmind_categories` (
  category_name STRING NOT NULL,
  monthly_budget NUMERIC NOT NULL,
  color_code STRING NOT NULL
);

-- Table 3: 30-Day Cash Flow Predictions & Anomaly Logs
CREATE TABLE IF NOT EXISTS `velvety-mason-417105.finmind_analytics.finmind_forecasts` (
  forecast_date DATE NOT NULL,
  predicted_balance NUMERIC NOT NULL,
  risk_level STRING NOT NULL
);
