-- FinMind AI BigQuery Population Script
-- Project: velvety-mason-417105
-- Run this directly in Google Cloud Console BigQuery Query Editor

CREATE SCHEMA IF NOT EXISTS `velvety-mason-417105.finmind_analytics`
OPTIONS(location='us-central1');

CREATE TABLE IF NOT EXISTS `velvety-mason-417105.finmind_analytics.user_profiles` (
  profile_id STRING,
  monthly_income NUMERIC,
  monthly_burn NUMERIC,
  savings_rate NUMERIC,
  updated_at TIMESTAMP
);

INSERT INTO `velvety-mason-417105.finmind_analytics.user_profiles` VALUES
('USER-001', 8500.0, 4820.0, 43.3, CURRENT_TIMESTAMP());

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
('TXN-TODAY-001', CURRENT_DATE(), 18.50, 'EXPENSE', 'Dining out & Entertainment', 'Starbucks Morning Coffee', FALSE, FALSE, 'Today live transaction'),
('TXN-TODAY-002', CURRENT_DATE(), 145.20, 'EXPENSE', 'Groceries & Food', 'Whole Foods Organic Groceries', FALSE, FALSE, 'Today live transaction'),
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
('TXN-1030', DATE('2026-03-06'), 113.98, 'EXPENSE', 'Groceries & Food', 'Local Organic Market', FALSE, FALSE, 'Daily transaction');
