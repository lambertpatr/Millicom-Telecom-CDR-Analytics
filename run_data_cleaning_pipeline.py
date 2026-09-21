"""
Master Data Cleaning & Format Benchmarking Orchestrator
======================================================
Executes end-to-end data cleaning, quality auditing, format benchmarking,
and interactive HTML portfolio dashboard generation.

Author: Principal Telecommunications Data Scientist & Modern Solutions Architect
Operator: MIC Tanzania PLC (Tigo Tanzania) / Millicom Group
"""

import time
import os
import json

from generate_very_messy_data import generate_all_messy_data
from clean_messy_data_engine import clean_dataset_and_audit
from pandas_bamboolib_cleaner import run_pandas_demo
from benchmark_file_formats import run_benchmarks
from generate_cleaning_showcase import build_showcase_html

def main():
    t_start = time.time()
    print("=" * 80)
    print("ENTERPRISE DATA CLEANING & PERFORMANCE BENCHMARKING PIPELINE")
    print("=" * 80)
    print(f"Directory: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Step 1: Synthesize Messy Real-World Data
    print("[PHASE 1/5] Synthesizing High-Entropy Messy Telecom & Fintech Dataset...")
    s1 = time.time()
    generate_all_messy_data()
    print(f" -> Completed Phase 1 in {time.time() - s1:.2f}s\n")

    # Step 2: High-Performance Data Cleaning & Standardization
    print("[PHASE 2/5] Executing High-Speed Cleaning, Standardization & Deduplication...")
    s2 = time.time()
    audit_report = clean_dataset_and_audit()
    print(f" -> Completed Phase 2 in {time.time() - s2:.2f}s\n")

    # Step 3: Pandas & Bamboolib Recipes
    print("[PHASE 3/5] Inspecting Vectorized Pandas Pipeline & Bamboolib Low-Code Recipes...")
    s3 = time.time()
    run_pandas_demo()
    print(f" -> Completed Phase 3 in {time.time() - s3:.2f}s\n")

    # Step 4: Multi-Format Speed & Storage Benchmarks
    print("[PHASE 4/5] Benchmarking CSV, JSON, JSONL, SQLite, Parquet & Feather...")
    s4 = time.time()
    benchmarks = run_benchmarks()
    print(f" -> Completed Phase 4 in {time.time() - s4:.2f}s\n")

    # Step 5: Interactive HTML Portfolio Showcase
    print("[PHASE 5/5] Compiling Interactive HTML5 Portfolio Showcase...")
    s5 = time.time()
    showcase_path = build_showcase_html()
    print(f" -> Completed Phase 5 in {time.time() - s5:.2f}s\n")

    total_time = time.time() - t_start
    metrics = audit_report.get("metrics", {})
    dq = metrics.get("data_quality_scores", {})
    before_score = dq.get("before", {}).get("composite_quality_index", 0)
    after_score = dq.get("after", {}).get("composite_quality_index", 0)

    print("=" * 80)
    print("DATA CLEANING PORTFOLIO PIPELINE - EXECUTIVE SUMMARY")
    print("=" * 80)
    print(f"Total Raw Rows Processed         : {metrics.get('raw_total_rows', 0):,}")
    print(f"Clean Unique Records Produced    : {metrics.get('clean_total_rows', 0):,}")
    print(f"Duplicate Records Rectified      : {metrics.get('duplicates_dropped', 0):,}")
    print(f"Phone Numbers Normalized (E.164) : {metrics.get('phone_formatting_errors_fixed', 0):,}")
    print(f"Timestamps Standardized (ISO8601): {metrics.get('timestamps_standardized', 0):,}")
    print(f"Currencies & Decimals Cleaned    : {metrics.get('currency_symbols_stripped', 0):,}")
    print(f"Composite Data Quality Score     : {before_score}% -> {after_score}% (+{after_score - before_score:.1f}%)")
    print(f"Total Pipeline Latency           : {total_time:.2f} seconds")
    print(f"Interactive Portfolio Showcase   : file://{showcase_path}")
    print("=" * 80)
    print("SUCCESS: Ready for Portfolio Presentation, GitHub publication, and Technical Interviews!\n")

if __name__ == "__main__":
    main()
