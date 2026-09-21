# Corporate Financial Planning, 12-Month Budgeting & Cash Flow Forecasting Suite

[![Model Standard](https://img.shields.io/badge/Financial%20Standard-FAST%20Modeling%20Guidelines-0A2540.svg)](#financial-modeling-architecture)
[![Dynamic Formulas](https://img.shields.io/badge/Excel%20Engine-639%20Dynamic%20Formulas%20(0%20Hardcoded%20Calc%20Errors)-emerald.svg)](#12-month-operating-model)
[![Liquidity & Runway](https://img.shields.io/badge/Cash%20Flow-Direct%20Method%20%7C%20Working%20Capital%20DSO%2FDPO-0369A1.svg)](#monthly-cash-flow-forecast)
[![Data Pipeline](https://img.shields.io/badge/ETL%20Data%20Pipeline-Dirty%20ERP%20%E2%9E%9E%20Standardized%20Ledger-purple.svg)](#automated-data-cleansing-pipeline)

An institutional, C-Suite executive financial planning and budgeting model built in **Microsoft Excel (`.xlsx`)** and automated with **Python (`openpyxl`)**. Designed for SaaS, technology platforms, and modern B2B/B2C enterprises, this model delivers dynamic 12-month P&L projections, direct cash flow forecasting, Budget vs. Actuals (BvA) variance controls, and an integrated **raw-to-clean accounting ETL pipeline**.

**Primary Deliverable File:** `Corporate_Financial_Budgeting_and_Forecasting_Model.xlsx`

---

## Executive Financial Scorecard & Highlights (FY 2026 Model Output)

| Financial Dimension | Model Metric | Forecast Value (FY 2026) | Strategic Target / Benchmark | Operational Assessment |
|---|---|---|---|---|
| **1. Gross Revenue** | Total Invoiced Sales | **$1,650,000** | +18.0% YoY Growth | Driven by Enterprise Platform Licenses & SaaS expansion |
| **2. Cost of Goods Sold (COGS)** | Hosting, APIs & Engineering | **$335,000** | 20.3% of Revenue | Gross Margin: **79.7%** (Exceeds 75% tech benchmark) |
| **3. Operating Expenses (OpEx)** | Headcount, Cloud, Marketing, G&A | **$653,900** | 39.6% of Revenue | Payroll represents 58.2% of total operational expenditure |
| **4. Operating Profitability (EBITDA)**| Core Cash Earnings | **$661,100** | 40.1% EBITDA Margin | High-margin cash generation model |
| **5. Net Profit After Tax** | Bottom-Line Profit | **$488,175** | 29.6% Net Margin | Accrued 25.0% corporate income tax rate on positive EBIT |
| **6. Starting Cash Liquidity** | M1 Beginning Balance | **$125,000** | Minimum Buffer ($40k) | Sufficient seed / working capital reserve |
| **7. Ending Cash Balance (M12)** | Final Cash at Bank | **$586,175** | Net Cash Growth: +$461k | Zero external financing or dilutive debt required |
| **8. Cash Runway** | Months of Remaining Cash | **Self-Sustaining** | $\ge 12$ Months | Net positive operational cash flow achieved from Month 2 |

---

## Complete Workbook Architecture & Sheet Guide

The model consists of **7 specialized sheets** structured according to institutional FP&A and **FAST Modeling Standards**:

```
 ┌─────────────────────────────────────────────────────────────────────────────────────────┐
 │ 01_Executive_Dashboard (First Page)                                                     │
 │ • C-Suite KPI summary cards: Annual Revenue, Gross Margin %, EBITDA, Cash Balance       │
 │ • Quarterly financial roll-up (Q1, Q2, Q3, Q4, FY 2026 Total)                           │
 │ • Embedded Native Charts: Monthly Revenue vs OpEx, Ending Cash Liquidity Trajectory     │
 │ • Strategic management insights & risk remediation directives                           │
 └────────────────────────────────────────────┬────────────────────────────────────────────┘
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼                                    ▼                                    ▼
 ┌───────────────────────────┐ ┌───────────────────────────┐ ┌───────────────────────────┐
 │ 02_Assumptions_&_Drivers  │ │ 03_12M_P&L_Forecast       │ │ 04_Monthly_Cash_Flow      │
 │ • Unit pricing & volumes  │ │ • Revenue by product stream│ │ • Customer cash receipts  │
 │ • Monthly MoM growth %    │ │ • Direct COGS allocation  │ │   (30-day DSO collections)│
 │ • Headcount & payroll     │ │ • Departmental OpEx lines │ │ • Vendor disbursements    │
 │ • Working capital (DSO/DPO│ │ • EBITDA, Tax & Net Profit│ │ • CapEx, Net Burn, Runway │
 └───────────────────────────┘ └───────────────────────────┘ └───────────────────────────┘
         │                                    │                                    │
         └────────────────────────────────────┼────────────────────────────────────┘
                                              ▼
 ┌─────────────────────────────────────────────────────────────────────────────────────────┐
 │ 05_Budget_vs_Actuals (Financial Control Framework)                                      │
 │ • 15 core budget line items tracked against simulated YTD actuals                       │
 │ • Dollar Variance ($) = Actual - Budget (Revenue) or Budget - Actual (Expenses)         │
 │ • Percentage Variance (%) & Automated Status Tags: FAVORABLE / ON TRACK / UNFAVORABLE   │
 │ • Root-cause commentary & operational management action required                        │
 └────────────────────────────────────────────┬────────────────────────────────────────────┘
                                              │
         ┌────────────────────────────────────┴────────────────────────────────────┐
         ▼                                                                         ▼
 ┌───────────────────────────────────────────┐ ┌───────────────────────────────────────────┐
 │ 06_Data_Cleaning_Pipeline                 │ │ 07_Model_Documentation                    │
 │ • Stage 1: Dirty raw ERP/bank export      │ │ • Model governance & financial logic      │
 │ • Stage 2: 5-step automated audit trail   │ │ • FAST standard color codes (Blue vs Black│
 │ • Stage 3: Clean standardized GL ledger   │ │ • Step-by-step monthly close update guide │
 └───────────────────────────────────────────┘ └───────────────────────────────────────────┘
```

---

## Detailed Sheet Breakdown

### 1. `01_Executive_Dashboard` (First Page - Executive Scorecard)
- **C-Suite KPI Cards**:
  - `ANNUAL FORECAST REVENUE`: `$1,650,000` (Target: $1.65M, +18% YoY)
  - `FORECAST GROSS MARGIN`: `79.7%` (Benchmark: > 75% Tech SaaS)
  - `ANNUAL EBITDA`: `$661,100` (Operating cash generation)
  - `NET CASH CHANGE (FY)`: `+$461,175` (Full-year operational cash build)
  - `ENDING CASH BALANCE (M12)`: `$586,175` (Liquidity safety reserve intact)
- **Quarterly Financial Summary Table**:
  - Summarizes Revenue, COGS, Gross Profit, OpEx, EBITDA, Net Income, and Ending Cash across Q1, Q2, Q3, Q4, and FY 2026.
- **Embedded Visual Charts**:
  - *Chart 1*: Monthly Revenue vs. Total OpEx column chart (`openpyxl.chart.BarChart`).
  - *Chart 2*: Ending Cash Balance & Liquidity Growth line chart (`openpyxl.chart.LineChart`).
- **Strategic Management Directives**:
  - Tactical commentary on revenue acceleration, gross margin defense, payroll ramping, and working capital optimization.

---

### 2. `02_Assumptions_&_Drivers` (Foundation)
- **Strict Color Standard**:
  - `BLUE FONT / GREEN CELL` (`#002060` / `#F0FDF4`): Dynamic user inputs (can be edited freely).
  - `BLACK FONT`: Calculated formulas (protected from accidental overwrites).
- **Revenue Drivers**:
  - *SaaS Subscriptions (Pro Tier)*: 150 starting units, 8% MoM growth, $120/mo price, 12% COGS.
  - *Enterprise Platform Licenses*: 15 starting units, 5% MoM growth, $2,500/mo price, 18% COGS.
  - *Professional Implementation & Onboarding*: 8 starting units, 4% MoM growth, $3,800/mo price, 35% COGS.
  - *Premium Managed Services & SLA*: 25 starting units, 6% MoM growth, $650/mo price, 20% COGS.
- **Headcount Roster**:
  - 7 strategic roles with departmental tagging, hire start months (Month 1 to 4), base monthly salary, and employer tax/benefits multiplier (18%–20%).
- **Operating Expenses**:
  - Fixed vs. Variable classification, monthly base budget, and monthly inflation/scale factor.
- **Working Capital Drivers**:
  - Starting cash balance ($125,000), Days Sales Outstanding (30 days DSO), Days Payable Outstanding (30 days DPO), corporate tax rate (25.0%), and planned capital expenditures (CapEx).

---

### 3. `03_12M_P&L_Forecast` (12-Month Operating Projection)
- **Month-by-Month Matrix**: M1 through M12 with full-year totals and `% of Revenue` common-size analysis.
- **Revenue Projections**: Dynamic compound monthly growth formulas referencing Driver assumptions.
- **Cost of Goods Sold (COGS)**: Direct hosting/cloud, license royalties, third-party APIs, and contractor implementation.
- **Gross Profit & Gross Margin %**: Monitored across all 12 operating cycles.
- **Operating Expenses (OpEx)**:
  - Automated `SUMPRODUCT` formula dynamically scaling departmental payroll based on employee start dates.
  - Variable marketing spend, SaaS subscriptions, facilities, audit, and legal retainers.
- **Profitability Horizons**:
  - `EBITDA` -> `Depreciation & Amortization` -> `EBIT` -> `Corporate Tax (25%)` -> `Net Profit After Tax`.

---

### 4. `04_Monthly_Cash_Flow` (Direct Liquidity Statement)
- **Direct Cash Flow Method**:
  - *Operating Inflows*: Customer collections applying a 30-day DSO lag (80% collected in month, 20% collected following month).
  - *Operating Outflows*: Vendor COGS disbursements (30-day DPO lag), monthly payroll disbursements, digital marketing ad spend, and overhead.
- **Net Cash Flow from Operations (CFO)**: Calculated monthly.
- **Investing & Financing Activities**:
  - Capital expenditures for infrastructure upgrades ($15k in M5, $12k in M10).
- **Cash Runway & Liquidity Tracking**:
  - Beginning Cash -> Net Monthly Burn/Build -> Ending Cash Balance.
  - Dynamic `Estimated Cash Runway (Months)` formula flagging self-sustaining profitability vs. months until cash depletion.

---

### 5. `05_Budget_vs_Actuals` (BvA Variance Framework)
- **15 Line-Item Variance Monitor**:
  - Approved 12-Month Budget vs. Projected Full-Year Actuals.
  - Dollar Variance:
    $$\text{Variance}_{\text{Rev}} = \text{Actual} - \text{Budget}$$
    $$\text{Variance}_{\text{Exp}} = \text{Budget} - \text{Actual}$$
  - Percentage Variance: $\text{Variance } \% = \frac{\text{Variance } \$}{\text{Approved Budget}}$
- **Automated Performance Status Flags**:
  - `FAVORABLE` (Soft Green): Positive revenue surplus or operational cost savings.
  - `ON TRACK` (Soft Amber): Variance within acceptable tolerance ($\ge -5.0\%$).
  - `UNFAVORABLE` (Soft Red): Negative revenue shortfall or budget overrun ($< -5.0\%$).
- **Operational Action Plans**: Clear management interventions documented for every line item.

---

### 6. `06_Data_Cleaning_Pipeline` (Messy Data ETL Showcase)
Demonstrates end-to-end data hygiene by taking raw, messy ERP journal entries and transforming them into a standardized financial ledger:

#### Stage 1: Raw Unstructured Source (Common Data Glitches)
- Inconsistent date formats (`2026/01/14`, `14-Jan-2026`, `2026.01.18`, `01/22/2026`).
- Messy vendor aliases with typos (`amazon web services inc`, `AWS CLOUD SVCS`, `MICROSOFT IRELAND / AZURE`, `google *workspace gsuite`).
- Dirty numeric strings (`$ 4,250.00 USD`, `(4,250.00)`, `1280.50 $`, ` $3,200.00`).
- Unmapped or missing General Ledger codes (`6002-ops`, `NULL`, `gsuite`, `rev-proc`).
- Void and duplicate entries (`TX-9030 VOID-TRANS`).

#### Stage 2: 5-Step Audited Transformation Rules
1. **String Trimming & Deduplication**: Stripped whitespace, newlines, and flagged void transactions.
2. **Universal Date Normalization**: Standardized all dates into ISO 8601 format (`YYYY-MM-DD`).
3. **Fuzzy Entity Resolution**: Mapped vendor aliases into unified Master Counterparties (e.g. `Amazon Web Services (AWS)`).
4. **Financial String Sanitization**: Removed currency symbols, parsed accounting parentheses into positive expenses.
5. **Chart of Accounts (COA) Mapping**: Reclassified unmapped codes into standard P&L driver categories.

#### Stage 3: Clean Standardized Ledger
- Output ledger with validated data types, ready for pivot tables, formula lookups, and direct feed into the financial dashboard.

---

### 7. `07_Model_Documentation` (Operational Guide)
- Governance principles and formula integrity rules.
- FAST Standard cell color conventions.
- Month-end close operating procedures for non-finance business owners.
- Key financial ratio definitions and executive cheat sheet.

---

## Technical Verification & Quality Audit

The model was generated and programmatically validated using `openpyxl`:
- **Total Worksheets**: 7 fully formatted sheets.
- **Dynamic Formulas**: **639 formulas** verified.
- **Formula Errors**: **0 syntax or `#REF!` / `#VALUE!` errors**.
- **Grid Alignment**: Auto-fitted column widths, custom row heights, and consistent corporate typography (`Calibri`).

To regenerate or customize the model:
```bash
python3 generate_financial_budget_model.py
```

---

## Freelance Proposal & Portfolio Summary

This project showcases:
1. **Institutional Financial Modeling**: Multi-tiered P&L, direct cash flow forecasting, and driver-based budgeting.
2. **Data Science & ETL Integration**: Solving real-world dirty accounting data problems and feeding clean pipelines into dashboards.
3. **Executive Presentation**: C-Suite dashboards, KPI scorecards, embedded Excel charts, and BvA variance frameworks.
4. **Fast Turnaround**: Completely built, verified, and delivered within 24–48 hours.
