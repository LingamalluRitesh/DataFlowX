"""
DataFlowX Partition Pruning & Predicate Filter
Evaluates query WHERE clauses against partition values to prune entire partition directories from physical execution scans.
"""

from typing import Any, Dict, List


class PartitionPruner:
    """Prunes unneeded partitions based on query filters."""

    @classmethod
    def prune_partitions(cls, all_partitions: List[Dict[str, Any]], filter_col: str, filter_val: Any) -> List[Dict[str, Any]]:
        matching = []
        for p in all_partitions:
            p_val = p.get(filter_col)
            if p_val is not None and str(p_val) == str(filter_val):
                matching.append(p)
        return matching
