"""
DataFlowX Pushdown Sub-Plan Optimizer
Extracts predicate filters, aggregations, and column projections to push down into remote database connectors, minimizing data transfer volume.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PushdownSubPlan(BaseModel):
    connector_type: str
    physical_table: str
    pushed_columns: List[str] = Field(default_factory=list)
    pushed_filters: List[str] = Field(default_factory=list)
    limit: Optional[int] = None


class PushdownPlanner:
    """Generates source-specific pushdown sub-plans."""

    @classmethod
    def generate_subplan(
        cls,
        connector_type: str,
        physical_table: str,
        projections: List[str],
        filters: List[str],
        limit: Optional[int] = None
    ) -> PushdownSubPlan:
        return PushdownSubPlan(
            connector_type=connector_type,
            physical_table=physical_table,
            pushed_columns=projections,
            pushed_filters=filters,
            limit=limit
        )
