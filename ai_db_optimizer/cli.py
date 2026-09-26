"""
AI Database Optimizer - Command Line Interface (CLI)
===================================================
Run diagnostic audits, analyze execution plans, and synthesize non-blocking index fixes.
Usage:
  python3 -m ai_db_optimizer.cli --audit
  python3 -m ai_db_optimizer.cli --query-id Q-PG-101
"""

import sys
import json
import argparse
from .models.schemas import DatabaseEngine
from .connectors.postgres import PostgresDiagnosticConnector
from .analyzer.optimizer_engine import AutonomousDBAOptimizer


def run_cli():
    parser = argparse.ArgumentParser(description="AI Database Optimizer & Autonomous DBA Engine")
    parser.add_argument("--engine", default="PostgreSQL", choices=["PostgreSQL", "SQL Server", "Oracle"], help="Target database engine")
    parser.add_argument("--audit", action="store_true", help="Run full diagnostic telemetry audit across pg_stat_statements")
    parser.add_argument("--query-id", help="Analyze specific slow query ID and generate DDL fix")
    parser.add_argument("--json", action="store_true", help="Output findings as structured JSON")

    args = parser.parse_args()

    print("=================================================================")
    print("⚡ AI DATABASE OPTIMIZER & AUTONOMOUS DBA ENGINE (PHASE 1)")
    print(f"🎯 Target Engine: {args.engine}")
    print("=================================================================\n")

    connector = PostgresDiagnosticConnector()
    optimizer = AutonomousDBAOptimizer()

    slow_queries = connector.fetch_slow_queries(limit=5)
    print(f"🔍 Discovered {len(slow_queries)} slow queries requiring optimization:\n")

    for q in slow_queries:
        print(f"  • [{q.query_id}] Mean Latency: {q.mean_exec_time_ms:,.1f} ms | Calls: {q.calls:,} | Cache Hit: {q.cache_hit_ratio_pct:.1f}%")
        print(f"    SQL: {q.query_text[:90]}...\n")

    # Pick query to analyze
    target_q = slow_queries[0]
    if args.query_id:
        for sq in slow_queries:
            if sq.query_id == args.query_id:
                target_q = sq
                break

    print(f"🔬 Running Autonomous Deep-Plan Analysis on Target Query [{target_q.query_id}]...")
    plan_json = connector.explain_query_plan(target_q.query_text)
    recommendation = optimizer.analyze_query_and_plan(
        query_record=target_q,
        raw_plan=plan_json,
        engine=DatabaseEngine.POSTGRESQL
    )

    if args.json:
        print(json.dumps(recommendation.dict(), indent=2))
        return

    print("\n-----------------------------------------------------------------")
    print("📋 AUTONOMOUS DBA DIAGNOSTIC REPORT & ACTION PLAN")
    print("-----------------------------------------------------------------")
    print(f"Diagnosis: {recommendation.summary_explanation}\n")

    print("🚨 Operational Bottlenecks Detected:")
    for f in recommendation.findings:
        print(f"  [{f.severity.value}] {f.title}")
        print(f"    • Root Cause: {f.root_cause}")
        print(f"    • Impact: {f.description}\n")

    if recommendation.suggested_ddl:
        print("🛠️ Recommended Production DDL Fix (Non-Blocking):")
        print("```sql")
        print(recommendation.suggested_ddl)
        print("```\n")

    if recommendation.suggested_config_tuning:
        print("⚙️ Recommended Configuration Tuning:")
        print("```sql")
        print(recommendation.suggested_config_tuning)
        print("```\n")

    print(f"🚀 Estimated Optimization Impact: {recommendation.estimated_speedup_factor} ({recommendation.estimated_latency_reduction_pct:.1f}% latency drop)")
    
    print("\n📚 Vector Knowledge RAG Citations:")
    for c in recommendation.vector_knowledge_citations:
        print(f"  • {c}")
    print("=================================================================\n")


if __name__ == "__main__":
    run_cli()
