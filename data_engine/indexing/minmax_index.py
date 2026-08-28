"""
DataFlowX Parquet Min/Max Zone-Map Index
Maintains minimum, maximum, and null-count metadata per row-group page to prune entire blocks without disk I/O.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ColumnZoneMap(BaseModel):
    column_name: str
    min_value: Any
    max_value: Any
    null_count: int = 0


class RowGroupZoneMap(BaseModel):
    row_group_id: int
    total_records: int
    column_stats: Dict[str, ColumnZoneMap] = Field(default_factory=dict)


class ZoneMapPruner:
    """Evaluates predicate pushdown against Min/Max statistics."""

    @classmethod
    def can_prune_row_group(cls, stats: ColumnZoneMap, op: str, literal_val: Any) -> bool:
        if stats.min_value is None or stats.max_value is None:
            return False

        if op == ">" and literal_val >= stats.max_value:
            return True  # Prune: all values in group are <= literal_val
        elif op == ">=" and literal_val > stats.max_value:
            return True
        elif op == "<" and literal_val <= stats.min_value:
            return True  # Prune: all values in group are >= literal_val
        elif op == "<=" and literal_val < stats.min_value:
            return True
        elif op in ("=", "==") and (literal_val < stats.min_value or literal_val > stats.max_value):
            return True  # Prune: target value outside min/max range

        return False
