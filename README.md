# Millicom (Tigo Tanzania) Telecommunications CDR Analytics & Network Intelligence Platform

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Operator Standard](https://img.shields.io/badge/Operator-Tigo%20Tanzania%20%7C%20Millicom%20Group-002B49.svg)](https://www.tigo.co.tz/)
[![TCRA Standard](https://img.shields.io/badge/Regulatory%20Standard-TCRA%20QoS%20Regulations-emerald.svg)](https://www.tcra.go.tz/)
[![Excel Audit Pack](https://img.shields.io/badge/Excel%20Model-OpenPyXL%20Institutional-orange.svg)](#institutional-excel-reporting-pack)
[![Interactive Dashboard](https://img.shields.io/badge/Executive%20UI-Tailwind%20%2B%20Leaflet%20%2B%20Chart.js-cyan.svg)](#interactive-executive-html5-dashboard)

An institutional Telecommunications Data Science, Network Quality of Service (QoS/QoE), Revenue Assurance & Fraud Management (RAFM), and C-Suite Executive Analytics suite developed for **MIC Tanzania PLC (Tigo Tanzania / Millicom Group - MCC 640, MNC 02)**.

The platform continuously processes multi-service Call Detail Records (CDRs) across **Circuit-Switched Voice & VoLTE**, **Packet Data Protocol (PDP) Contexts (4G/LTE & 5G)**, and **Tigo Pesa Mobile Financial Services**, auditing network performance against **Tanzania Communications Regulatory Authority (TCRA)** statutory standards.

---

## Executive Summary & Telecommunications Audit Highlights

| Dimension | Audited Metric | Performance Value | TCRA Benchmark / Target | Regulatory & Commercial Status |
|---|---|---|---|---|
| **1. Total Audited Subscribers** | Active SIM profiles | 1,499 Subscribers | Representative Sample | Multi-tier segmentation (VIP, SME, Streamers) |
| **2. Cell Tower Infrastructure** | Monitored BTS / eNodeB / gNodeB | 54 Operational Sites | 14 Tanzanian Regions | 5G (Dar, Dom, Arusha, Mza), 4G Metro & 3G |
| **3. Voice Traffic Volume** | Audited Calls & Holding Time | 9,356 Calls (21,091 Mins) | 2.09 Erlangs Mean | Diurnal Peak: 3.79 Erlangs @ 20:00 HRS |
| **4. Answer Seizure Ratio (ASR)** | Call Setup Efficiency | **68.42%** | $\ge 65.00\%$ | **COMPLIANT** (Excellent trunk seizure rate) |
| **5. Call Completion Rate (CCR)** | Successfully Terminated Calls | **93.94%** | $\ge 98.00\%$ | **MARGINAL SLA GAP** (Radio link drop remediation) |
| **6. Call Drop Rate (CDR)** | Abnormal Disconnections | **6.45%** | $< 0.80\%$ | **CRITICAL REMEDIATION** (Fringe cell interference) |
| **7. Trunk Congestion Block** | Erlang B Channel Saturation | **1.08%** | $< 1.50\%$ | **COMPLIANT** (Within statutory maximum ceiling) |
| **8. RAFM SIM-Box Fraud** | Grey-route bypass gateways | **9 SIM-Boxes** | Zero Tolerance | **TZS 756,338 ($289 USD)** Direct MTR leakage |
| **9. Total Gross Revenue** | Voice + Data + Tigo Pesa | **TZS 15.61 Million** | $5,956 USD Gross | **Blended ARPU: TZS 10,411** / subscriber |

---

## Telecommunications Engineering & Architecture

```
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ 1. INGESTION & NETWORK SWITCHING TELEMETRY                                  │
 │ • MSC / HLR / VLR / PGW / UPF / SMSC / USSD Gateway Ingestion               │
 │ • CGI Topology: MCC 640 (Tanzania), MNC 02 (Tigo), LAC, Cell Identity (CI) │
 │ • Multi-Service: VoLTE, CSFB, 3G CS, 4G LTE PDP, 5G NR, Tigo Pesa Mobile    │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        │
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ 2. TELECOM ANALYTICS & MACHINE LEARNING CORE                                │
 │ • Traffic Engineering: Erlang Load, Busy Hour Traffic (BHT), Erlang B Model │
 │ • Regulatory SLA Auditing: ASR, CCR, CDR against TCRA Targets               │
 │ • Revenue Assurance & Fraud (RAFM): SIM-Box Bypass, Wangiri, Cloned SIMs   │
 │ • Customer Science: RFM Segmentation, Churn Propensity, Influencer Hubs     │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
 ┌─────────────────────────────────────┐ ┌─────────────────────────────────────┐
 │ 3. INSTITUTIONAL EXCEL AUDIT PACK   │ │ 4. INTERACTIVE EXECUTIVE DASHBOARD  │
 │ • Multi-Tab OpenPyXL C-Suite Model  │ │ • Standalone Responsive Dark UI     │
 │ • TCRA SLA Scorecards & Dynamic Sums│ │ • Leaflet BTS Tanzania Coverage Map │
 │ • National Interconnect MTR Clearing│ │ • 24-Hour Diurnal Erlang Curves     │
 │ • SIM-Box Blacklist Dossier         │ │ • Live Forensic Searchable Explorer │
 └─────────────────────────────────────┘ └─────────────────────────────────────┘
```

---

## Mathematical Formulations & Telecom Domain Models

### 1. Traffic Intensity (Erlang)
The continuous dimensionless traffic load carried by a cell or group of circuits:
$$A = \frac{\sum_{i=1}^N t_i}{T} = \frac{\lambda \times h}{3600}$$
Where:
- $\lambda$ is the call arrival rate per hour.
- $h$ is the average call holding duration in seconds.

### 2. Erlang B Trunk Blocking Probability Model
Used to determine the probability that an incoming call finds all $C$ channels busy on a carrier:
$$B(C, A) = \frac{\frac{A^C}{C!}}{\sum_{k=0}^C \frac{A^k}{k!}}$$
Implemented in the engine via stable reciprocal iteration:
$$\text{InvB}(k) = 1 + \frac{k}{A} \cdot \text{InvB}(k-1), \quad B(C, A) = \frac{1}{\text{InvB}(C)}$$

### 3. TCRA Key Telecommunication Performance Indicators (KTPIs)
- **Answer Seizure Ratio (ASR)**:
  $$\text{ASR} = \frac{\text{Answered Calls}}{\text{Total Call Seizures (Attempts)}} \times 100\% \quad (\text{TCRA Benchmark: } \ge 65\%)$$
- **Call Completion Rate (CCR)**:
  $$\text{CCR} = \frac{\text{Normally Cleared Calls}}{\text{Answered Calls} + \text{Dropped Calls}} \times 100\% \quad (\text{TCRA Target: } \ge 98.0\%)$$
- **Call Drop Rate (CDR)**:
  $$\text{CDR} = \frac{\text{Dropped Calls (Abnormal Clearing)}}{\text{Answered Calls}} \times 100\% \quad (\text{TCRA Target: } < 0.8\%)$$

### 4. SIM-Box / International Bypass Fraud Heuristic Scoring
SIM-boxes bypass international incoming gateways by terminating traffic through consumer prepaid SIM cards to avoid paying national Mobile Termination Rates (MTR):
$$S_{\text{simbox}} = w_1 \cdot \mathbb{I}(\text{Ratio}_{\text{out/in}} > 15) + w_2 \cdot \mathbb{I}(\text{Mobility Cells} \le 1) + w_3 \cdot \mathbb{I}(\overline{d} \in [150, 450]) + w_4 \cdot \mathbb{I}(\text{IMEI TAC} \in \text{Gateway})$$
$$\text{Sanction Rule: } S_{\text{simbox}} \ge 0.70 \implies \text{Immediate IMEI/IMSI Blacklisting}$$

### 5. Impossible Travel / Cloned SIM Speed Anomaly
Evaluates physical feasibility of sequential call origins using Haversine geodesic distance:
$$v_{\text{apparent}} = \frac{D_{\text{haversine}}(\text{Tower}_1, \text{Tower}_2)}{\Delta t_{\text{seconds}}} \times 3600 \text{ km/h}$$
If $v_{\text{apparent}} > 850 \text{ km/h}$, flag as **Cloned SIM / IMSI Spoofing Fraud**.

---

## Deliverables & File Structure

```
/Users/lambert/Desktop/fast-api/Data-Science/Millicom-Company/
├── millicom_executive_cdr_dashboard.html           # Standalone Interactive C-Suite HTML5 Dashboard
├── Millicom_Tigo_Executive_CDR_Analytics_Pack.xlsx  # Institutional OpenPyXL Excel Audit Pack (6 Sheets)
├── millicom_telecom_metrics.json                   # Consolidated Telecommunications Audit JSON
├── generate_millicom_cdr_data.py                  # Enterprise Multi-Service CDR Ingestion & Mediation Engine
├── telecom_cdr_analytics_engine.py                 # Core Telecom Engineering, QoS, Fraud & ML Engine
├── generate_cdr_excel_pack.py                      # OpenPyXL Financial & Network Reporting Generator
├── generate_executive_dashboard.py                 # HTML5 / Leaflet / Chart.js Dashboard Compiler
├── run_pipeline.py                                 # Automated Master Pipeline Orchestrator
├── millicom_cell_towers_infrastructure.csv         # 54 Cell Towers (CGI, GPS, Erlangs, Azimuth, Tech)
├── millicom_subscribers_master.csv                 # 1,500 Subscriber Profiles (IMSI, IMEI, Segment, ARPU)
├── millicom_cdr_voice.csv                          # 9,356 Voice CDRs (VoLTE, CS, Dropped, Route)
├── millicom_cdr_data_sessions.csv                  # 5,000 Data PDP Sessions (4G/5G, APN, Latency, Loss)
├── millicom_cdr_tigo_pesa_momo.csv                 # 3,500 Tigo Pesa Mobile Money Transactions
├── millicom_interconnect_operator_rates.csv        # TCRA Regulated Interconnect MTR Clearing Matrix
│
├── DATA_CLEANING_PORTFOLIO.md                      # Comprehensive Data Cleaning & Format Portfolio Case Study
├── data_cleaning_portfolio_showcase.html           # Interactive Before-vs-After Data Quality & Benchmark UI
├── run_data_cleaning_pipeline.py                   # Master Orchestrator for Messy Data Cleaning & Benchmarks
├── generate_very_messy_data.py                     # Realistic High-Entropy Messy Data Synthesizer
├── clean_messy_data_engine.py                      # High-Performance E.164, ISO-8601 & Quality Audit Engine
├── pandas_bamboolib_cleaner.py                     # Vectorized Pandas .pipe() & Bamboolib Low-Code Recipes
├── benchmark_file_formats.py                       # Benchmarks for CSV, JSON, JSONL, Parquet, Feather, SQLite
├── raw_messy_telecom_data.csv                      # Synthesized Raw Messy CSV (Phone, Currencies, Typos)
├── clean_telecom_data.csv                          # Clean Production CSV
├── clean_telecom_data.json                         # Clean Production JSON Records
├── clean_telecom_events.jsonl                      # Clean Production JSON-Lines (Streaming)
└── clean_telecom_data.db                           # Clean SQLite Database with Typed B-Tree Indexes
```

---

## Data Cleaning, Pandas, Bamboolib & Format Engineering Suite

For senior data science and data engineering portfolios, this repository includes a dedicated module transforming **very messy, high-entropy telecommunications records** into validated production formats:

- **E.164 Phone Normalization**: Parses 10+ dirty dialects (`+255 714...`, `0714-...`, `+255(0)...`, `tel:...`) to E.164.
- **Resilient Datetime Parsing**: Unifies 7+ chaotic formats (ISO, US, UK, named months, Unix epochs) to ISO-8601 UTC.
- **Financial Token Sanitization**: Strips currency prefixes (`TZS 15,000/=`, `$ 6.20 USD`, commas, negatives) into clean floats.
- **Vectorized Pandas `.pipe()`**: Eliminates fragmentation using declarative method chaining and `category` dtypes.
- **Bamboolib Low-Code Integration**: Demonstrates GUI-based exploratory cleaning and zero-lock-in Pandas code generation.
- **File Format Speed Benchmarking**: Compares CSV, Gzip, JSON, JSONL, Parquet, Feather, and SQLite on storage, write speed, read speed, and schema fidelity.
- **Interactive Before-vs-After Showcase**: Open `data_cleaning_portfolio_showcase.html` in any browser to inspect row-level diffs, interactive benchmark charts, and quality scorecards.

To run the data cleaning suite:
```bash
python3 run_data_cleaning_pipeline.py
```

---

## How to Run & Present

### 1. Execute End-to-End Pipeline
Run the complete automated pipeline in under 1 second:
```bash
python3 run_pipeline.py
```

### 2. View the Interactive Executive Dashboard
Simply double-click or open `millicom_executive_cdr_dashboard.html` in any web browser:
- **Interactive Leaflet Map**: Click any of the 54 cell sites across Tanzania to view live Erlangs, Erlang-B blocking, and technology layers.
- **Diurnal Curves**: 24-hour voice and data traffic patterns with busy hour detection.
- **TCRA Radar**: Instant SLA gap analysis and regulatory compliance verification.
- **RAFM Fraud Center**: Review SIM-box bypass detections and financial loss metrics.
- **Forensic Explorer**: Filter and search individual Voice, Data, and Mobile Money CDRs.

### 3. Open the Excel Audit Pack
Open `Millicom_Tigo_Executive_CDR_Analytics_Pack.xlsx` in Microsoft Excel:
- Designed with corporate Millicom Blue (`#002B49`) and Tigo Gold styling.
- Features dynamic Excel formulas (`SUM`, `AVERAGE`), conditional audit highlights, and TCRA SLA benchmarks.

---

## Corporate Financial Planning & 12-Month Budgeting Model

For FP&A, corporate finance, and executive advisory portfolios, this repository includes an institutional financial modeling suite:

- **Executive Dashboard (First Page)**: C-Suite KPI cards (Revenue, Gross Margin %, EBITDA, Net Burn, Ending Liquidity), quarterly performance roll-up, and native embedded charts (`BarChart`, `LineChart`).
- **Dynamic 12-Month Forecast**: Monthly P&L model cascading from driver-based revenue and cost assumptions with zero hardcoded math.
- **Direct Cash Flow Forecast**: Working capital schedules modeling 30-day DSO customer collection lags and 30-day DPO vendor payment terms.
- **Budget vs. Actuals (BvA) Framework**: 15 monitored operational lines with variance dollar/percentage calculations and automated conditional alert tags (`FAVORABLE` / `ON TRACK` / `UNFAVORABLE`).
- **Messy Data Cleaned Pipeline**: Demonstrates an end-to-end automated ETL audit trail converting raw unstructured ERP extracts into a standardized accounting ledger.
- **Documentation**: Detailed guide and architecture in [FINANCIAL_BUDGETING_PORTFOLIO.md](FINANCIAL_BUDGETING_PORTFOLIO.md).

To regenerate the financial model workbook:
```bash
python3 generate_financial_budget_model.py
```
Outputs: `Corporate_Financial_Budgeting_and_Forecasting_Model.xlsx` (639 validated dynamic formulas, 0 formula errors).

---

## Greater Washington, D.C. Real Estate Scope Estimator Engine

An executive-ready, protected, and fully automated **Master Estimator Workbook** designed for on-site field estimators evaluating residential property transitions across the Greater D.C. Metropolitan Area:

- **Tab 1: Front-End Field Scope & Estimate Generator (UI)**: On-site property profile (Target ZIP Code, Square Footage, Asset Tier), 21-day cosmetic transition scope builder, live Speed Zone classification (Alpha/Beta/Gamma based on MDOM), and dynamic ROI multiples.
- **Tab 2: Master SKU & Material Price Database**: Structured procurement catalog linking live Home Depot, Floor & Decor, and Amazon pricing tiers ($/SF, $/EA) via native `XLOOKUP` / `INDEX-MATCH` formulas.
- **Tab 3: Parametric Rules & Regional Tier Multipliers**: 16 submarket ZIP codes across D.C., Northern Virginia, and Maryland with regional labor multipliers (1.00x–1.55x) and historical value-add multipliers.
- **Bulletproof Protection**: Sheet-level locking with only 20 field input cells unlocked, strictly preventing formula breakage.
- **Documentation**: Detailed architecture in [REAL_ESTATE_SCOPE_ESTIMATOR_PORTFOLIO.md](REAL_ESTATE_SCOPE_ESTIMATOR_PORTFOLIO.md).

To regenerate the Master Estimator workbook:
```bash
python3 build_dc_real_estate_estimator.py
```
Outputs: `Greater_DC_Property_Transition_Master_Estimator.xlsx` (3 interconnected locked tabs).

---

## DuckDB Vectorized OLAP & Out-of-Core Performance Benchmark

An empirical benchmark evaluating **DuckDB's vectorized columnar C++ engine** on **1,000,000 telecommunications records**:

- **Direct Parquet Aggregation**: **52.97 ms** across 1M rows with only 0.01 MB Python RAM overhead.
- **SIMD Columnar Pushdown**: **14.00 ms** to aggregate selective columns, skipping 80% of unneeded I/O.
- **Vectorized Window Functions**: **116.94 ms** for multi-partition rolling moving averages.
- **Out-of-Core Resilience**: Enforced an artificial **32 MB RAM limit** (`SET max_memory = '32MB'`) — executed in **18.08 ms** with zero out-of-memory errors.
- **Native Columnar Storage**: Stored 1M rows in **25.76 MB** with subsequent queries resolving in **0.82 ms**.
- **Documentation**: Detailed case study in [DUCKDB_OUT_OF_CORE_PORTFOLIO.md](DUCKDB_OUT_OF_CORE_PORTFOLIO.md).

To run the benchmark:
```bash
python3 benchmark_duckdb_vs_pandas.py
```
Outputs: `duckdb_benchmark_results.json`

