"""
Institutional DBA Knowledge Base & Vector Retrieval Engine
==========================================================
Maintains high-precision database tuning rules, execution plan node archetypes,
and indexing heuristics. Provides semantic vector search (cosine similarity / pgvector)
to match execution plan antipatterns against proven architectural remediations.
"""

import math
import re
from typing import List, Dict, Any, Tuple
from ..models.schemas import DatabaseEngine, DiagnosticSeverity


class TuningRule:
    def __init__(
        self,
        rule_id: str,
        engine: DatabaseEngine,
        category: str,
        title: str,
        trigger_pattern: str,
        severity: DiagnosticSeverity,
        antipattern_summary: str,
        remediation_strategy: str,
        ddl_template: str,
        config_template: str,
        keywords: List[str]
    ):
        self.rule_id = rule_id
        self.engine = engine
        self.category = category
        self.title = title
        self.trigger_pattern = trigger_pattern
        self.severity = severity
        self.antipattern_summary = antipattern_summary
        self.remediation_strategy = remediation_strategy
        self.ddl_template = ddl_template
        self.config_template = config_template
        self.keywords = keywords
        # Precomputed bag-of-words / TF representation for local vector matching
        self.feature_vector = self._compute_feature_vector()

    def _compute_feature_vector(self) -> Dict[str, float]:
        text = f"{self.title} {self.category} {self.antipattern_summary} {' '.join(self.keywords)}".lower()
        tokens = re.findall(r"\w+", text)
        freq: Dict[str, float] = {}
        for t in tokens:
            freq[t] = freq.get(t, 0.0) + 1.0
        # Normalize vector length
        length = math.sqrt(sum(v * v for v in freq.values()))
        if length > 0:
            for k in freq:
                freq[k] /= length
        return freq


# Institutional Tuning Rules Catalog
RULES_CATALOG: List[TuningRule] = [
    TuningRule(
        rule_id="PG-IDX-001",
        engine=DatabaseEngine.POSTGRESQL,
        category="Missing Index",
        title="Full Sequential Scan on Large Relation",
        trigger_pattern="Seq Scan on table with actual_rows > 5000",
        severity=DiagnosticSeverity.CRITICAL,
        antipattern_summary="Postgres is performing a full table scan, reading 100% of 8KB disk blocks because no selective B-Tree index exists for the WHERE filter clause.",
        remediation_strategy="Create a non-blocking concurrent composite B-Tree index covering the equality and range filter columns to convert the Seq Scan into an Index Scan.",
        ddl_template="CREATE INDEX CONCURRENTLY idx_{table}_{columns} ON {table} ({columns_list});",
        config_template="SET enable_seqscan = off; -- (Testing only in dev session)",
        keywords=["seq scan", "sequential scan", "filter", "full table scan", "missing index", "disk blocks", "high latency"]
    ),
    TuningRule(
        rule_id="PG-MEM-002",
        engine=DatabaseEngine.POSTGRESQL,
        category="Disk Spill (work_mem)",
        title="Hash Join / Sort Memory Spill to Disk",
        trigger_pattern="Sort Method: external merge Disk or Hash Batches > 1",
        severity=DiagnosticSeverity.WARNING,
        antipattern_summary="The query memory requirement exceeded the session 'work_mem'. PostgreSQL spilled intermediate tuples to temporary disk files, creating high I/O wait latency.",
        remediation_strategy="Increase work_mem for reporting or batch queries, or add indexed ordering to avoid runtime quicksort or external merge disk spills.",
        ddl_template="-- Optimize ordering column index:\nCREATE INDEX CONCURRENTLY idx_{table}_sort ON {table} ({order_column});",
        config_template="SET work_mem = '64MB'; -- Or ALTER USER app_reporter SET work_mem = '128MB';",
        keywords=["external merge disk", "work_mem", "disk spill", "hash join", "hash batches", "sort method", "temp_blks_written", "temp file"]
    ),
    TuningRule(
        rule_id="PG-STAT-003",
        engine=DatabaseEngine.POSTGRESQL,
        category="Stale Statistics",
        title="Severe Row Estimate Disparity (Planner Miscalculation)",
        trigger_pattern="abs(plan_rows - actual_rows) > 10000 or ratio > 10x",
        severity=DiagnosticSeverity.WARNING,
        antipattern_summary="PostgreSQL query planner misestimated row cardinality due to stale statistics or multi-column data correlation, picking an inefficient join strategy (e.g. Nested Loop instead of Hash Join).",
        remediation_strategy="Run ANALYZE on the table, increase default_statistics_target, or create extended multivariate statistics for correlated columns.",
        ddl_template="CREATE STATISTICS stat_{table}_{cols} ON {columns_list} FROM {table};\nANALYZE {table};",
        config_template="ALTER TABLE {table} ALTER COLUMN {column} SET STATISTICS 500;\nANALYZE {table};",
        keywords=["plan rows", "actual rows", "row disparity", "miscalculation", "stale statistics", "analyze", "nested loop", "cardinality"]
    ),
    TuningRule(
        rule_id="PG-BLOAT-004",
        engine=DatabaseEngine.POSTGRESQL,
        category="Table & Index Bloat",
        title="High Dead Tuple Ratio / Vacuum Starvation",
        trigger_pattern="n_dead_tup / n_live_tup > 0.20",
        severity=DiagnosticSeverity.WARNING,
        antipattern_summary="High volume of UPDATE/DELETE operations created thousands of dead MVCC tuples that autovacuum has not reclaimed, inflating 8KB table pages and degrading cache hit ratios.",
        remediation_strategy="Tune autovacuum thresholds for high-churn tables to trigger vacuuming earlier, and run non-blocking pg_repack if physical disk footprint is bloated.",
        ddl_template="ALTER TABLE {table} SET (autovacuum_vacuum_scale_factor = 0.05, autovacuum_vacuum_cost_limit = 1000);",
        config_template="VACUUM (ANALYZE, VERBOSE) {table};",
        keywords=["dead tuples", "bloat", "autovacuum", "mvcc", "vacuum starvation", "cache hit ratio", "n_dead_tup", "repack"]
    ),
    TuningRule(
        rule_id="PG-LOCK-005",
        engine=DatabaseEngine.POSTGRESQL,
        category="Unindexed Foreign Key Lock Escalation",
        title="Unindexed Foreign Key Causing Cascade Table Locks",
        trigger_pattern="Foreign key column without backing B-Tree index",
        severity=DiagnosticSeverity.CRITICAL,
        antipattern_summary="Deleting or updating rows in the parent table forces a sequential scan and SHARE ROW EXCLUSIVE lock on the child table, blocking concurrent writes and inducing deadlocks.",
        remediation_strategy="Create a supporting B-Tree index on the child referencing foreign key column.",
        ddl_template="CREATE INDEX CONCURRENTLY idx_{child_table}_{fk_col} ON {child_table} ({fk_col});",
        config_template="-- Verify locking queries:\nSELECT pid, query, mode, granted FROM pg_locks l JOIN pg_stat_activity a ON l.pid = a.pid WHERE NOT granted;",
        keywords=["foreign key", "fk", "table lock", "deadlock", "cascade delete", "referential integrity", "blocking query"]
    ),
    TuningRule(
        rule_id="PG-HOT-006",
        engine=DatabaseEngine.POSTGRESQL,
        category="8KB Page & Fillfactor Tuning",
        title="High Update Churn / Index Write Amplification",
        trigger_pattern="High UPDATE volume with default fillfactor=100 causing non-HOT updates",
        severity=DiagnosticSeverity.WARNING,
        antipattern_summary="Every UPDATE on a 100% full 8KB page forces a new page allocation and writes to all secondary indexes. Setting fillfactor=85 leaves 15% head-room, enabling Heap-Only Tuple (HOT) updates that bypass index modifications.",
        remediation_strategy="Lower table fillfactor to 80-85 to enable in-page HOT updates, and repack the table to reclaim fragmented bloat.",
        ddl_template="ALTER TABLE {table} SET (fillfactor = 85);\n-- Vacuum to re-align page layout:\nVACUUM (ANALYZE) {table};",
        config_template="-- Check HOT update efficiency (healthy > 85%):\nSELECT relname, n_tup_upd, n_tup_hot_upd, ROUND(100.0 * n_tup_hot_upd / NULLIF(n_tup_upd, 0), 2) AS hot_ratio_pct FROM pg_stat_user_tables WHERE n_tup_upd > 1000;",
        keywords=["fillfactor", "hot update", "heap only tuple", "write amplification", "8kb page", "update bloat", "index maintenance"]
    ),
    TuningRule(
        rule_id="PG-SSD-007",
        engine=DatabaseEngine.POSTGRESQL,
        category="Hardware Planner Alignment",
        title="Outdated Spinning Disk Cost Model on Modern SSD/NVMe",
        trigger_pattern="random_page_cost = 4.0 on NVMe/EBS storage",
        severity=DiagnosticSeverity.WARNING,
        antipattern_summary="Default random_page_cost=4.0 assumes spinning mechanical HDDs with high seek penalties. On modern NVMe SSDs, random access is almost as fast as sequential access. The planner wrongly favors sequential scans over fast index seeks.",
        remediation_strategy="Calibrate random_page_cost to 1.1 and enable asynchronous I/O prefetching to reflect real NVMe hardware capability.",
        ddl_template="-- Applies to database session or system level:\nALTER SYSTEM SET random_page_cost = 1.1;\nALTER SYSTEM SET effective_io_concurrency = 200;\nSELECT pg_reload_conf();",
        config_template="SET random_page_cost = 1.1;\nSET effective_io_concurrency = 200;",
        keywords=["random_page_cost", "effective_io_concurrency", "ssd", "nvme", "planner cost model", "index seek avoidance", "hdd"]
    ),
    TuningRule(
        rule_id="PG-WAL-008",
        engine=DatabaseEngine.POSTGRESQL,
        category="Checkpoint & WAL I/O Smoothing",
        title="Frequent Forced Checkpoints & Buffer Write Spikes",
        trigger_pattern="Checkpoints occurring more frequently than checkpoint_timeout due to low max_wal_size",
        severity=DiagnosticSeverity.ADVISORY,
        antipattern_summary="Default max_wal_size=1GB causes frequent forced checkpoints during bulk writes, abruptly flushing dirty shared_buffers to disk and creating periodic latency freezes.",
        remediation_strategy="Increase max_wal_size to 16GB-32GB and set checkpoint_completion_target=0.9 to spread I/O evenly across the checkpoint window.",
        ddl_template="-- System-level configuration:\nALTER SYSTEM SET max_wal_size = '16GB';\nALTER SYSTEM SET checkpoint_completion_target = 0.9;\nALTER SYSTEM SET wal_compression = on;\nSELECT pg_reload_conf();",
        config_template="-- Check checkpoint frequency in logs or pg_stat_bgwriter:\nSELECT checkpoints_timed, checkpoints_req, checkpoint_write_time, checkpoint_sync_time FROM pg_stat_bgwriter;",
        keywords=["max_wal_size", "checkpoint", "wal", "checkpoint_completion_target", "bgwriter", "io spike", "wal_compression"]
    ),
    # Multi-Engine: SQL Server
    TuningRule(
        rule_id="MS-IDX-001",
        engine=DatabaseEngine.SQL_SERVER,
        category="Missing Index",
        title="SQL Server Clustered / Non-Clustered Table Scan",
        trigger_pattern="Table Scan or Clustered Index Scan with high cost",
        severity=DiagnosticSeverity.CRITICAL,
        antipattern_summary="SQL Server optimizer flagged high impact in sys.dm_db_missing_index_details due to full table scans on large tables.",
        remediation_strategy="Create targeted Non-Clustered Index with INCLUDE columns to enable covering index lookups.",
        ddl_template="CREATE NONCLUSTERED INDEX IX_{table}_{cols} ON dbo.{table} ({cols}) INCLUDE ({include_cols}) WITH (ONLINE = ON);",
        config_template="SET STATISTICS IO ON;\nSET STATISTICS TIME ON;",
        keywords=["sql server", "table scan", "clustered index scan", "sys.dm_db_missing_index_details", "include", "nonclustered index"]
    ),
    # Multi-Engine: Oracle Database
    TuningRule(
        rule_id="ORA-IDX-001",
        engine=DatabaseEngine.ORACLE,
        category="Missing Index",
        title="Oracle Full Table Scan (TABLE ACCESS FULL)",
        trigger_pattern="TABLE ACCESS FULL on high cardinality segment",
        severity=DiagnosticSeverity.CRITICAL,
        antipattern_summary="Oracle Cost-Based Optimizer (CBO) initiated a multiblock read full table scan on large segment, creating high 'db file scattered read' wait events in AWR/ASH.",
        remediation_strategy="Create selective B-Tree or Composite Index and gather fresh table statistics with DBMS_STATS.",
        ddl_template="CREATE INDEX idx_{table}_{cols} ON {table} ({cols}) ONLINE NOLOGGING;",
        config_template="EXEC DBMS_STATS.GATHER_TABLE_STATS(ownname => '{schema}', tabname => '{table}', estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE, cascade => TRUE);",
        keywords=["oracle", "table access full", "dbms_stats", "db file scattered read", "cbo", "awr", "ash", "v$sql_plan"]
    )
]


class DBAKnowledgeBase:
    """Vector & semantic retrieval engine for database tuning playbooks."""

    def __init__(self, rules: List[TuningRule] = RULES_CATALOG):
        self.rules = rules

    def search_rules(self, query_text: str, engine: DatabaseEngine = DatabaseEngine.POSTGRESQL, top_k: int = 3) -> List[Tuple[TuningRule, float]]:
        """
        Performs semantic vector cosine similarity matching against DBA tuning rules.
        """
        query_tokens = re.findall(r"\w+", query_text.lower())
        query_freq: Dict[str, float] = {}
        for t in query_tokens:
            query_freq[t] = query_freq.get(t, 0.0) + 1.0

        q_len = math.sqrt(sum(v * v for v in query_freq.values()))
        if q_len > 0:
            for k in query_freq:
                query_freq[k] /= q_len

        scored_rules = []
        for r in self.rules:
            # Filter by engine (or universal rules)
            if r.engine != engine and r.engine != DatabaseEngine.POSTGRESQL:
                continue

            # Compute Cosine Similarity between query vector and rule feature vector
            dot_product = sum(query_freq.get(token, 0.0) * weight for token, weight in r.feature_vector.items())
            
            # Boost score if explicit keywords match
            for kw in r.keywords:
                if kw in query_text.lower():
                    dot_product += 0.35

            scored_rules.append((r, min(dot_product, 1.0)))

        scored_rules.sort(key=lambda x: x[1], reverse=True)
        return scored_rules[:top_k]
