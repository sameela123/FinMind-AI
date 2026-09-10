## 1. Project Context
- **Project ID**: velvety-mason-417105
- **Domain**: This project is centralized around "FinMind AI", an autonomous personal finance, multi-agent wealth, and risk intelligence engine.
- **Data**: All financial transactions, monthly budgets, spending categories, and cash flow predictions are processed and stored in BigQuery and local ledgers.

## 2. Project Milestone Targets & Delivery Schedule
- **Milestone 1**: Problem Statement & Architecture Design — ✅ Completed (Aug 17, 2026)
- **Milestone 2**: BigQuery Data Schema DDL & Synthetic Data Pipeline — ✅ Completed (Aug 17, 2026)
- **Milestone 3**: Multi-Agent Engine (Expense Auditor, Predictor & Advisor) — ✅ Completed (Aug 17, 2026)
- **Milestone 4**: Dashboard UI & Data Visualizations (Chart.js + Goal Vaults + Export) — ✅ Completed (Aug 17, 2026)
- **Milestone 5**: Comprehensive User Testing & Edge Case Validation — ✅ Completed (Aug 29, 2026)
- **Milestone 6**: Production Deployment to Firebase Hosting / Cloud Run — ✅ Completed (Sep 5, 2026)

## 3. Execution & Data Processing Rules
- **CRITICAL RULE - Structured Specs**: The semantic and structured information extracted from project specifications should be strictly followed.
- **CRITICAL RULE - Customer Financial Data**: Existing FinMind financial transaction data resides in BigQuery in dataset `finmind_analytics`.
- **CRITICAL RULE - Ledger Data**: Transaction data is present in tables `finmind_transactions`, `finmind_categories`, and `finmind_forecasts`.
- **CRITICAL RULE - Multi-Agent System**: The Expense Auditor, Cash Flow Predictor, and Wealth Advisor agents operate on unified ledger streams.
- **CRITICAL RULE - General**: When you are referencing a dataset, ensure you are using it with your Project ID `velvety-mason-417105`.

## 4. Key UI Features & Application Specifications
- **Update Salary/Income & Monthly Budget Feature**: Users can click "✏️ Update Salary / Budget" in the UI header to dynamically adjust their monthly income/salary AND monthly burn rate/expense budget. This recalculates the Net Savings Rate, updates KPI cards, persists changes in `localStorage` (`finmind_income` and `finmind_burn`), and triggers an automated financial recalculation alert in the AI Chat Co-pilot.
- **Goal Vaults**: Allows dynamic creation and progress tracking of custom financial savings goals with target dates and visual completion bars.
- **Multi-Agent Chat Co-pilot**: Instant access to Expense Auditor, Cash Flow Predictor, and Wealth Advisor agent recommendations.
- **Ledger Export**: Supports exporting full transaction ledgers to CSV (`FinMind_BigQuery_Ledger_Export_*.csv`) and printing audit summary reports to PDF.

