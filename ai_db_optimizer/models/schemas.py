"""
AI Database Optimizer & Autonomous DBA Engine - Core Schemas
============================================================
Dataclass-based schemas defining database telemetry, execution plan trees,
diagnostic findings, and AI optimization recommendations.
Zero external dependency: runs natively on standard Python 3.10+.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


class DatabaseEngine(str, Enum):
    POSTGRESQL = "PostgreSQL"
    SQL_SERVER = "Microsoft SQL Server"
    ORACLE = "Oracle Database"


class DiagnosticSeverity(str, Enum):
    CRITICAL = "CRITICAL"    # Immediate production risk (e.g. table locks, 100% CPU Seq Scan on 10M rows)
    WARNING = "WARNING"      # High latency, missing composite index, memory disk spill
    ADVISORY = "ADVISORY"    # Autovacuum tuning, minor configuration drift
    OPTIMAL = "OPTIMAL"      # Well-tuned, index hit ratio > 99%


@dataclass
class SlowQueryRecord:
    query_id: str
    query_text: str
    calls: int
    total_exec_time_ms: float
    mean_exec_time_ms: float
    max_exec_time_ms: float
    rows_returned_avg: float
    cache_hit_ratio_pct: float
    engine: DatabaseEngine = DatabaseEngine.POSTGRESQL
    database_name: str = "production"
    shared_blks_read: int = 0
    shared_blks_hit: int = 0
    temp_blks_written: int = 0  # Indicates disk spilling (work_mem exhaustion)


@dataclass
class PlanNode:
    node_type: str                  # e.g., "Seq Scan", "Index Scan", "Hash Join", "Sort"
    relation_name: Optional[str] = None
    alias: Optional[str] = None
    startup_cost: float = 0.0
    total_cost: float = 0.0
    plan_rows: int = 0
    actual_rows: int = 0
    actual_time_ms: float = 0.0
    filter_condition: Optional[str] = None
    index_name: Optional[str] = None
    index_cond: Optional[str] = None
    buffers_hit: int = 0
    buffers_read: int = 0
    buffers_dirtied: int = 0
    hash_batches: Optional[int] = None
    sort_method: Optional[str] = None
    children: List['PlanNode'] = field(default_factory=list)


@dataclass
class DiagnosticFinding:
    finding_id: str
    severity: DiagnosticSeverity
    category: str  # e.g. "Missing Index", "Disk Spill (work_mem)", "High Row Disparity", "Table Bloat"
    title: str
    description: str
    affected_object: str  # Table, query, or configuration parameter
    root_cause: str


@dataclass
class OptimizationRecommendation:
    recommendation_id: str
    engine: DatabaseEngine
    findings: List[DiagnosticFinding]
    summary_explanation: str
    estimated_speedup_factor: str                 # e.g. "25x - 40x speedup"
    estimated_latency_reduction_pct: float        # e.g. 96.5%
    query_id: Optional[str] = None
    suggested_ddl: Optional[str] = None           # e.g. CREATE INDEX CONCURRENTLY ...
    suggested_config_tuning: Optional[str] = None # e.g. SET work_mem = '64MB';
    suggested_query_rewrite: Optional[str] = None # e.g. Replace correlated subquery with JOIN
    vector_knowledge_citations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass hierarchy to dictionary for JSON output."""
        return {
            "recommendation_id": self.recommendation_id,
            "engine": self.engine.value,
            "query_id": self.query_id,
            "summary_explanation": self.summary_explanation,
            "estimated_speedup_factor": self.estimated_speedup_factor,
            "estimated_latency_reduction_pct": self.estimated_latency_reduction_pct,
            "suggested_ddl": self.suggested_ddl,
            "suggested_config_tuning": self.suggested_config_tuning,
            "suggested_query_rewrite": self.suggested_query_rewrite,
            "findings": [
                {
                    "finding_id": f.finding_id,
                    "severity": f.severity.value,
                    "category": f.category,
                    "title": f.title,
                    "description": f.description,
                    "affected_object": f.affected_object,
                    "root_cause": f.root_cause
                }
                for f in self.findings
            ],
            "vector_knowledge_citations": self.vector_knowledge_citations
        }
