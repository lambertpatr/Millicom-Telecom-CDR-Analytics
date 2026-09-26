"""
PostgreSQL JSON Execution Plan Parser & Tree Traversal Engine
============================================================
Recursively parses EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) outputs
into structured PlanNode hierarchies. Pinpoints the exact operational bottlenecks:
- Heavy Sequential Scans with high row rejection
- Memory spills (external merge Disk / Hash Batches > 1)
- Significant cardinality estimation errors (stale statistics)
- Buffer read thrashing (low cache hit ratio)
"""

from typing import Dict, Any, List, Optional
from ..models.schemas import PlanNode


class ExecutionPlanParser:
    @classmethod
    def parse_postgres_json(cls, raw_explain: Dict[str, Any]) -> PlanNode:
        """
        Extracts the root PlanNode from standard PostgreSQL EXPLAIN JSON.
        """
        root_data = raw_explain
        if "Plan" in raw_explain:
            root_data = raw_explain["Plan"]
        elif isinstance(raw_explain, list) and len(raw_explain) > 0 and "Plan" in raw_explain[0]:
            root_data = raw_explain[0]["Plan"]

        return cls._parse_node(root_data)

    @classmethod
    def _parse_node(cls, node_dict: Dict[str, Any]) -> PlanNode:
        node = PlanNode(
            node_type=node_dict.get("Node Type", "Unknown"),
            relation_name=node_dict.get("Relation Name"),
            alias=node_dict.get("Alias"),
            startup_cost=float(node_dict.get("Startup Cost", 0.0)),
            total_cost=float(node_dict.get("Total Cost", 0.0)),
            plan_rows=int(node_dict.get("Plan Rows", 0)),
            actual_rows=int(node_dict.get("Actual Rows", 0)),
            actual_time_ms=float(node_dict.get("Actual Total Time", 0.0)),
            filter_condition=node_dict.get("Filter"),
            index_name=node_dict.get("Index Name"),
            index_cond=node_dict.get("Index Cond"),
            buffers_hit=int(node_dict.get("Shared Hit Blocks", 0)),
            buffers_read=int(node_dict.get("Shared Read Blocks", 0)),
            buffers_dirtied=int(node_dict.get("Shared Dirtied Blocks", 0)),
            hash_batches=node_dict.get("Hash Batches"),
            sort_method=node_dict.get("Sort Method")
        )

        # Recursively parse child plans
        child_plans = node_dict.get("Plans", [])
        for cp in child_plans:
            node.children.append(cls._parse_node(cp))

        return node

    @classmethod
    def flatten_nodes(cls, root: PlanNode) -> List[PlanNode]:
        """Flattens the tree into a list of all executed nodes for anomaly scanning."""
        nodes = [root]
        for child in root.children:
            nodes.extend(cls.flatten_nodes(child))
        return nodes
