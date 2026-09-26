"""
Microsoft SQL Server Diagnostic Telemetry Connector (Stub & Architecture)
========================================================================
Connects to SQL Server Dynamic Management Views (DMVs):
- sys.dm_exec_query_stats
- sys.dm_db_missing_index_details / sys.dm_db_missing_index_columns
- sys.dm_tran_locks & sys.dm_os_waiting_tasks
"""

from typing import List, Dict, Any, Optional
from .base import BaseDiagnosticConnector
from ..models.schemas import SlowQueryRecord, DatabaseEngine


class SqlServerDiagnosticConnector(BaseDiagnosticConnector):
    def __init__(self, host: Optional[str] = None, port: int = 1433, dbname: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        super().__init__(engine=DatabaseEngine.SQL_SERVER)
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password

    def test_connection(self) -> bool:
        return True

    def fetch_slow_queries(self, limit: int = 10, min_time_ms: float = 50.0) -> List[SlowQueryRecord]:
        return [
            SlowQueryRecord(
                query_id="Q-MSSQL-201",
                engine=DatabaseEngine.SQL_SERVER,
                query_text="SELECT TOP 100 p.PatientID, p.NationalID, b.BookingDate, b.FlightNumber FROM Booking b WITH (NOLOCK) JOIN Passenger p ON b.PassengerID = p.PassengerID WHERE b.BookingDate >= '2026-09-01' ORDER BY b.BookingDate DESC;",
                calls=24500,
                total_exec_time_ms=18375000.0,
                mean_exec_time_ms=750.0,
                max_exec_time_ms=2100.0,
                rows_returned_avg=100.0,
                cache_hit_ratio_pct=88.5,
                shared_blks_read=54000,
                shared_blks_hit=410000,
                temp_blks_written=0
            )
        ]

    def explain_query_plan(self, query_sql: str) -> Dict[str, Any]:
        return {
            "Plan": {
                "Node Type": "Clustered Index Scan",
                "Table": "Booking",
                "Actual Total Time": 750.0,
                "Estimated Cost": 84.5,
                "MissingIndexImpact": 92.4,
                "EqualityColumns": ["BookingDate"],
                "IncludeColumns": ["FlightNumber", "PassengerID"]
            }
        }

    def inspect_missing_indexes(self) -> List[Dict[str, Any]]:
        return [
            {
                "table_name": "Booking",
                "equality_columns": ["BookingDate"],
                "include_columns": ["FlightNumber", "PassengerID"],
                "user_seeks": 24500,
                "avg_user_impact": 92.4,
                "suggested_sql": "CREATE NONCLUSTERED INDEX IX_Booking_BookingDate_Inc ON dbo.Booking (BookingDate DESC) INCLUDE (FlightNumber, PassengerID) WITH (ONLINE = ON);"
            }
        ]

    def inspect_table_bloat(self) -> List[Dict[str, Any]]:
        return []

    def inspect_active_locks(self) -> List[Dict[str, Any]]:
        return []
