"""
Millicom Enterprise Telecom CDR Analytics Suite - Master Pipeline Orchestrator
=============================================================================
Project: Millicom (Tigo Tanzania) Enterprise Telecom CDR Intelligence Suite
Author: Principal Telecommunications Data Scientist & Modern Web Solutions Architect
Operator: MIC Tanzania PLC (Tigo Tanzania) - MCC 640, MNC 02

Executes end-to-end data pipeline:
1. Data Ingestion & Mediation: Infrastructure, Subscribers, Voice CDRs, Data PDP sessions, Tigo Pesa.
2. Analytics Engine: Erlang traffic, Erlang B model, TCRA QoS, RAFM Fraud, ML Churn, MTR.
3. Excel Reporting Pack: Institutional multi-tab workbook with formulas and styling.
4. Executive Dashboard: Standalone interactive HTML5 dashboard with Leaflet map & Chart.js.
"""

import os
import sys
import time
from generate_millicom_cdr_data import generate_data
from telecom_cdr_analytics_engine import run_telecom_analytics
from generate_cdr_excel_pack import build_excel_pack
from generate_executive_dashboard import build_dashboard

def main():
    t0 = time.time()
    print("=" * 80)
    print("MILLICOM (TIGO TANZANIA) TELECOM CDR INTELLIGENCE SUITE - PIPELINE EXECUTION")
    print("=" * 80)
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directory: {os.path.dirname(os.path.abspath(__file__))}\n")

    # Step 1: Data Generation
    print("[PHASE 1/4] Running Telecommunications Ingestion & Mediation Engine...")
    s1 = time.time()
    generate_data()
    print(f" -> Completed in {time.time() - s1:.2f}s\n")

    # Step 2: Analytics & QoS Engine
    print("[PHASE 2/4] Executing Telecom QoS, RAFM Fraud, ML Churn & Interconnect Engine...")
    s2 = time.time()
    metrics = run_telecom_analytics()
    print(f" -> Completed in {time.time() - s2:.2f}s\n")

    # Step 3: Excel Pack
    print("[PHASE 3/4] Generating C-Suite OpenPyXL Excel Audit Pack...")
    s3 = time.time()
    build_excel_pack()
    print(f" -> Completed in {time.time() - s3:.2f}s\n")

    # Step 4: Executive Dashboard
    print("[PHASE 4/4] Compiling Standalone Interactive Executive HTML5 Dashboard...")
    s4 = time.time()
    build_dashboard()
    print(f" -> Completed in {time.time() - s4:.2f}s\n")

    total_time = time.time() - t0
    macro = metrics.get('macro_kpis', {})
    tcra = metrics.get('tcra_qos_compliance', {})
    rafm = metrics.get('rafm_fraud_metrics', {})

    print("=" * 80)
    print("EXECUTIVE AUDIT SUMMARY")
    print("=" * 80)
    print(f"Total Active Subscribers Audited : {macro.get('total_subscribers', 0):,}")
    print(f"Total Monitored Cell Towers      : {macro.get('total_cell_towers', 0)} (5G, 4G, 3G across Tanzania)")
    print(f"Total Voice CDRs Audited         : {macro.get('total_voice_cdrs_audited', 0):,}")
    print(f"Gross Audited Revenue            : TZS {macro.get('total_gross_revenue_tzs', 0):,.0f} (${macro.get('total_gross_revenue_usd', 0):,.0f} USD)")
    print(f"Answer Seizure Ratio (ASR)       : {tcra.get('answer_seizure_ratio_asr_pct', 0):.2f}% ({tcra.get('asr_compliance_status', '')})")
    print(f"Call Completion Rate (CCR)       : {tcra.get('call_completion_rate_ccr_pct', 0):.2f}% ({tcra.get('ccr_compliance_status', '')})")
    print(f"Call Drop Rate (CDR)             : {tcra.get('call_drop_rate_cdr_pct', 0):.2f}% ({tcra.get('cdr_compliance_status', '')})")
    print(f"SIM-Box Fraud Nodes Intercepted  : {rafm.get('simbox_detected_count', 0)} (Loss: TZS {rafm.get('bypass_revenue_loss_tzs', 0):,.0f})")
    print(f"Wangiri Predators Detected       : {rafm.get('wangiri_detected_count', 0)}")
    print(f"Total Pipeline Execution Time    : {total_time:.2f} seconds")
    print("=" * 80)
    print("Platform ready for presentation to Client and C-Suite Leadership!\n")

if __name__ == '__main__':
    main()
