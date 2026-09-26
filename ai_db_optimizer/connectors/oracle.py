"""
Oracle Database Diagnostic Telemetry Connector (Stub & Architecture)
===================================================================
Connects to Oracle Dynamic Performance Views (V$) & AWR/ASH:
- V$SQL / V$SQLSTATS
- V$SQL_PLAN / DBMS_XPLAN.DISPLAY_CURSOR
- V$ACTIVE_SESSION_HISTORY (ASH) & DBA_HIST_SQLSTAT
"""

from typing import List, Dict, Any, Optional
from .base import BaseDiagnosticConnector
from ..models.schemas import SlowQueryRecord, DatabaseEngine


class OracleDiagnosticConnector(BaseDiagnosticConnector):
    def __init__(self, host: Optional[str] = None, port: int = 1521, service_name: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        super().__init__(engine=DatabaseEngine.ORACLE)
        self.host = host
        self.port = port
        self.service_name = service_name
        self.user = user
        self.password = password

    def test_connection(self) -> bool:
        return True

    def fetch_slow_queries(self, limit: int = 10, min_time_ms: float = 50.0) -> List[SlowQueryRecord]:
        return [
            SlowQueryRecord(
                query_id="Q-ORA-301",
                engine=DatabaseEngine.ORACLE,
                query_text="SELECT e.EMPLOYEE_ID, e.FIRST_NAME, e.SALARY, d.DEPARTMENT_NAME FROM HR.EMPLOYEES e JOIN HR.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID WHERE e.HIRE_DATE >= TO_DATE('2024-01-01', 'YYYY-MM-DD');",
                calls=9800,
                total_exec_time_ms=8624000.0,
                mean_exec_time_ms=880.0,
                max_exec_time_ms=2400.0,
                rows_returned_avg=450.0,
                cache_hit_ratio_pct=76.2,
                shared_blks_read=42000,
                shared_blks_hit=190000,
                temp_blks_written=0
            )
        ]

    def explain_query_plan(self, query_sql: str) -> Dict[str, Any]:
        return {
            "Plan": {
                "Node Type": "TABLE ACCESS FULL",
                "Table": "EMPLOYEES",
                "Actual Total Time": 880.0,
                "Estimated Cost": 1240,
                "WaitEvent": "db file scattered read",
                "Filter": "HIRE_DATE >= TO_DATE('2024-01-01', 'YYYY-MM-DD')"
            }
        }

    def inspect_missing_indexes(self) -> List[Dict[str, Any]]:
        return [
            {
                "table_name": "EMPLOYEES",
                "columns": ["HIRE_DATE", "DEPARTMENT_ID"],
                "suggested_sql": "CREATE INDEX HR.IDX_EMP_HIRE_DEPT ON HR.EMPLOYEES (HIRE_DATE, DEPARTMENT_ID) ONLINE NOLOGGING;"
            }
        ]

    def inspect_table_bloat(self) -> List[Dict[str, Any]]:
        return []

    def inspect_active_locks(self) -> List[Dict[str, Any]]:
        return []
