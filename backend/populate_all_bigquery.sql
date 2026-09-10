-- FinMind AI Complete BigQuery Setup Script
-- Project ID: velvety-mason-417105
-- Copy & Paste this entire script into BigQuery Console Query Editor

CREATE SCHEMA IF NOT EXISTS `velvety-mason-417105.finmind_analytics`
OPTIONS(location='US');

CREATE TABLE IF NOT EXISTS `velvety-mason-417105.finmind_analytics.finmind_transactions` (
  transaction_id STRING,
  date DATE,
  amount NUMERIC,
  type STRING,
  category STRING,
  merchant STRING,
  is_recurring BOOLEAN,
  is_anomaly BOOLEAN,
  notes STRING
);

INSERT INTO `velvety-mason-417105.finmind_analytics.finmind_transactions` VALUES
('TXN-1001', DATE('2026-02-18'), 103.13, 'EXPENSE', 'Travel & Rideshare', 'Lyft Ride', FALSE, FALSE, 'Daily transaction'),
('TXN-1002', DATE('2026-02-20'), 77.93, 'EXPENSE', 'Travel & Rideshare', 'Delta Air Lines', FALSE, FALSE, 'Daily transaction'),
('TXN-1003', DATE('2026-02-21'), 38.99, 'EXPENSE', 'Travel & Rideshare', 'Uber Trip', FALSE, FALSE, 'Daily transaction'),
('TXN-1004', DATE('2026-02-22'), 106.11, 'EXPENSE', 'Dining out & Entertainment', 'Chipotle Mexican Grill', FALSE, FALSE, 'Daily transaction'),
('TXN-1005', DATE('2026-02-22'), 88.43, 'EXPENSE', 'Travel & Rideshare', 'Uber Trip', FALSE, FALSE, 'Daily transaction'),
('TXN-1006', DATE('2026-02-23'), 83.79, 'EXPENSE', 'Dining out & Entertainment', 'Starbucks Coffee', FALSE, FALSE, 'Daily transaction'),
('TXN-1007', DATE('2026-02-23'), 92.19, 'EXPENSE', 'Dining out & Entertainment', 'AMC Movie Theater', FALSE, FALSE, 'Daily transaction'),
('TXN-1008', DATE('2026-02-24'), 99.16, 'EXPENSE', 'Groceries & Food', 'Trader Joe\'s', FALSE, FALSE, 'Daily transaction'),
('TXN-1009', DATE('2026-02-24'), 57.78, 'EXPENSE', 'Groceries & Food', 'Whole Foods Market', FALSE, FALSE, 'Daily transaction'),
('TXN-1010', DATE('2026-02-24'), 115.71, 'EXPENSE', 'Dining out & Entertainment', 'AMC Movie Theater', FALSE, FALSE, 'Daily transaction'),
('TXN-1011', DATE('2026-02-25'), 20.56, 'EXPENSE', 'Travel & Rideshare', 'Chevron Gas Station', FALSE, FALSE, 'Daily transaction'),
('TXN-1012', DATE('2026-02-26'), 35.36, 'EXPENSE', 'Travel & Rideshare', 'Chevron Gas Station', FALSE, FALSE, 'Daily transaction'),
('TXN-1013', DATE('2026-02-26'), 96.57, 'EXPENSE', 'Dining out & Entertainment', 'AMC Movie Theater', FALSE, FALSE, 'Daily transaction'),
('TXN-1014', DATE('2026-02-27'), 67.27, 'EXPENSE', 'Travel & Rideshare', 'Uber Trip', FALSE, FALSE, 'Daily transaction'),
('TXN-1015', DATE('2026-02-27'), 65.12, 'EXPENSE', 'Dining out & Entertainment', 'Starbucks Coffee', FALSE, FALSE, 'Daily transaction'),
('TXN-1016', DATE('2026-02-28'), 40.73, 'EXPENSE', 'Dining out & Entertainment', 'Chipotle Mexican Grill', FALSE, FALSE, 'Daily transaction'),
('TXN-1017', DATE('2026-03-01'), 4250.0, 'INCOME', 'Salary & Income', 'Tech Corp Payroll', TRUE, FALSE, 'Bi-weekly paycheck deposit'),
('TXN-1018', DATE('2026-03-01'), 2400.0, 'EXPENSE', 'Housing & Rent', 'Skyline Apartments LLC', TRUE, FALSE, 'Monthly apartment rent payment'),
('TXN-1019', DATE('2026-03-01'), 30.25, 'EXPENSE', 'Travel & Rideshare', 'Delta Air Lines', FALSE, FALSE, 'Daily transaction'),
('TXN-1020', DATE('2026-03-01'), 54.54, 'EXPENSE', 'Travel & Rideshare', 'Delta Air Lines', FALSE, FALSE, 'Daily transaction'),
('TXN-1021', DATE('2026-03-02'), 82.38, 'EXPENSE', 'Dining out & Entertainment', 'Chipotle Mexican Grill', FALSE, FALSE, 'Daily transaction'),
('TXN-1022', DATE('2026-03-02'), 34.17, 'EXPENSE', 'Dining out & Entertainment', 'Sushi Zen Restaurant', FALSE, FALSE, 'Daily transaction'),
('TXN-1023', DATE('2026-03-03'), 28.02, 'EXPENSE', 'Groceries & Food', 'Whole Foods Market', FALSE, FALSE, 'Daily transaction'),
('TXN-1024', DATE('2026-03-05'), 14.99, 'EXPENSE', 'Subscriptions & SaaS', 'Netflix Monthly', TRUE, FALSE, 'Regular active subscription'),
('TXN-1025', DATE('2026-03-05'), 9.99, 'EXPENSE', 'Subscriptions & SaaS', 'Spotify Premium', TRUE, FALSE, 'Regular active subscription'),
('TXN-1026', DATE('2026-03-05'), 49.99, 'EXPENSE', 'Subscriptions & SaaS', 'Forgotten Gym Membership', TRUE, TRUE, 'Flagged unused subscription'),
('TXN-1027', DATE('2026-03-05'), 89.0, 'EXPENSE', 'Subscriptions & SaaS', 'AWS Cloud Services', TRUE, TRUE, 'Flagged unused subscription'),
('TXN-1028', DATE('2026-03-06'), 27.22, 'EXPENSE', 'Groceries & Food', 'Whole Foods Market', FALSE, FALSE, 'Daily transaction'),
('TXN-1029', DATE('2026-03-06'), 96.41, 'EXPENSE', 'Groceries & Food', 'Trader Joe\'s', FALSE, FALSE, 'Daily transaction'),
('TXN-1030', DATE('2026-03-06'), 113.98, 'EXPENSE', 'Groceries & Food', 'Local Organic Market', FALSE, FALSE, 'Daily transaction'),
('TXN-1031', DATE('2026-03-08'), 77.95, 'EXPENSE', 'Dining out & Entertainment', 'Sushi Zen Restaurant', FALSE, FALSE, 'Daily transaction'),
('TXN-1032', DATE('2026-03-09'), 103.26, 'EXPENSE', 'Travel & Rideshare', 'Delta Air Lines', FALSE, FALSE, 'Daily transaction'),
('TXN-1033', DATE('2026-03-10'), 102.08, 'EXPENSE', 'Groceries & Food', 'Whole Foods Market', FALSE, FALSE, 'Daily transaction'),
('TXN-1034', DATE('2026-03-12'), 52.53, 'EXPENSE', 'Groceries & Food', 'Local Organic Market', FALSE, FALSE, 'Daily transaction'),
('TXN-1035', DATE('2026-03-13'), 71.66, 'EXPENSE', 'Groceries & Food', 'Local Organic Market', FALSE, FALSE, 'Daily transaction'),
('TXN-1036', DATE('2026-03-14'), 18.92, 'EXPENSE', 'Groceries & Food', 'Trader Joe\'s', FALSE, FALSE, 'Daily transaction'),
('TXN-1037', DATE('2026-03-14'), 41.48, 'EXPENSE', 'Travel & Rideshare', 'Uber Trip', FALSE, FALSE, 'Daily transaction'),
('TXN-1038', DATE('2026-03-15'), 4250.0, 'INCOME', 'Salary & Income', 'Tech Corp Payroll', TRUE, FALSE, 'Bi-weekly paycheck deposit'),
('TXN-1039', DATE('2026-03-16'), 104.6, 'EXPENSE', 'Groceries & Food', 'Costco Wholesale', FALSE, FALSE, 'Daily transaction'),
('TXN-1040', DATE('2026-03-16'), 54.61, 'EXPENSE', 'Dining out & Entertainment', 'AMC Movie Theater', FALSE, FALSE, 'Daily transaction');

CREATE TABLE IF NOT EXISTS `velvety-mason-417105.finmind_analytics.finmind_forecasts` (
  forecast_date DATE,
  predicted_balance NUMERIC,
  risk_level STRING
);

INSERT INTO `velvety-mason-417105.finmind_analytics.finmind_forecasts` VALUES
(DATE('2026-08-18'), 24145.0, 'LOW'),
(DATE('2026-08-19'), 24032.5, 'LOW'),
(DATE('2026-08-20'), 23920.0, 'LOW'),
(DATE('2026-08-21'), 23807.5, 'LOW'),
(DATE('2026-08-22'), 23695.0, 'LOW'),
(DATE('2026-08-23'), 23582.5, 'LOW'),
(DATE('2026-08-24'), 23470.0, 'LOW'),
(DATE('2026-08-25'), 23357.5, 'LOW'),
(DATE('2026-08-26'), 23245.0, 'LOW'),
(DATE('2026-08-27'), 23132.5, 'LOW'),
(DATE('2026-08-28'), 23020.0, 'LOW'),
(DATE('2026-08-29'), 22907.5, 'LOW'),
(DATE('2026-08-30'), 22795.0, 'LOW'),
(DATE('2026-08-31'), 22682.5, 'LOW'),
(DATE('2026-09-01'), 24420.0, 'LOW'),
(DATE('2026-09-02'), 24307.5, 'LOW'),
(DATE('2026-09-03'), 24195.0, 'LOW'),
(DATE('2026-09-04'), 24082.5, 'LOW'),
(DATE('2026-09-05'), 23970.0, 'LOW'),
(DATE('2026-09-06'), 23857.5, 'LOW'),
(DATE('2026-09-07'), 23745.0, 'LOW'),
(DATE('2026-09-08'), 23632.5, 'LOW'),
(DATE('2026-09-09'), 23520.0, 'LOW'),
(DATE('2026-09-10'), 23407.5, 'LOW'),
(DATE('2026-09-11'), 23295.0, 'LOW'),
(DATE('2026-09-12'), 23182.5, 'LOW'),
(DATE('2026-09-13'), 23070.0, 'LOW'),
(DATE('2026-09-14'), 22957.5, 'LOW'),
(DATE('2026-09-15'), 27095.0, 'LOW'),
(DATE('2026-09-16'), 26982.5, 'LOW');

CREATE TABLE IF NOT EXISTS `velvety-mason-417105.finmind_analytics.finmind_categories` (
  category_name STRING,
  monthly_budget NUMERIC,
  color_code STRING
);

INSERT INTO `velvety-mason-417105.finmind_analytics.finmind_categories` VALUES
('Salary & Income', 8500.0, '#10B981'),
('Housing & Rent', 2400.0, '#6366F1'),
('Groceries & Food', 800.0, '#F59E0B'),
('Subscriptions & SaaS', 150.0, '#EF4444'),
('Dining out & Entertainment', 450.0, '#EC4899'),
('Utilities & Bills', 350.0, '#3B82F6'),
('Travel & Rideshare', 300.0, '#8B5CF6'),
('Investments & Stocks', 1500.0, '#14B8A6');
