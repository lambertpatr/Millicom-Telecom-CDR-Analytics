"""
Database Diagnostic Connector - Abstract Base Interface
========================================================
Defines uniform contract for telemetry extraction, query plan retrieval,
missing index inspection, and lock detection across PostgreSQL, SQL Server, and Oracle.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..models.schemas import SlowQueryRecord, DatabaseEngine, PlanNode


class BaseDiagnosticConnector(ABC):
    def __init__(self, engine: DatabaseEngine):
        self.engine = engine

    @abstractmethod
    def test_connection(self) -> bool:
        """Verifies connectivity to the target database."""
        pass

    @abstractmethod
    def fetch_slow_queries(self, limit: int = 10, min_time_ms: float = 50.0) -> List[SlowQueryRecord]:
        """Extracts top slow queries from query store (e.g. pg_stat_statements)."""
        pass

    @abstractmethod
    def explain_query_plan(self, query_sql: str) -> Dict[str, Any]:
        """Executes EXPLAIN (FORMAT JSON, BUFFERS) and returns raw execution plan tree."""
        pass

    @abstractmethod
    def inspect_missing_indexes(self) -> List[Dict[str, Any]]:
        """Identifies unindexed foreign keys or tables with high sequential scan ratios."""
        pass

    @abstractmethod
    def inspect_table_bloat(self) -> List[Dict[str, Any]]:
        """Detects dead tuples and storage bloat."""
        pass

    @abstractmethod
    def inspect_active_locks(self) -> List[Dict[str, Any]]:
        """Detects blocking queries, lock wait queues, and contention."""
        pass
