"""
AI Database Optimizer & Autonomous DBA Suite
============================================
Multi-engine query diagnostic and indexing optimization engine.
Supports PostgreSQL (Phase 1), with extensions for SQL Server and Oracle.
"""

from .models.schemas import (
    DatabaseEngine,
    DiagnosticSeverity,
    SlowQueryRecord,
    PlanNode,
    DiagnosticFinding,
    OptimizationRecommendation
)
from .connectors.postgres import PostgresDiagnosticConnector
from .knowledge.dba_knowledge_base import DBAKnowledgeBase
from .analyzer.optimizer_engine import AutonomousDBAOptimizer

__all__ = [
    "DatabaseEngine",
    "DiagnosticSeverity",
    "SlowQueryRecord",
    "PlanNode",
    "DiagnosticFinding",
    "OptimizationRecommendation",
    "PostgresDiagnosticConnector",
    "DBAKnowledgeBase",
    "AutonomousDBAOptimizer"
]
