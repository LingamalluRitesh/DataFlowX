"""
DataFlowX Multi-Source Federated Query Planner
Decomposes cross-system queries across Snowflake, PostgreSQL, BigQuery, and Lakehouse storage into sub-queries.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class FederatedSubqueryPlan(BaseModel):
    plan_id: str
    target_data_source: str  # POSTGRES, SNOWFLAKE, BIGQUERY, LAKEHOUSE_S3
    sql_text: str
    estimated_rows: int
    pushdown_filters: List[str] = Field(default_factory=list)


class FederatedExecutionPlan(BaseModel):
    query_id: str
    subplans: List[FederatedSubqueryPlan] = Field(default_factory=list)
    join_strategy: str = "BROADCAST_HASH_JOIN"
    final_projections: List[str] = Field(default_factory=list)


class FederatedPlanner:
    """Plans federated multi-source queries."""

    @classmethod
    def plan_federation(cls, query_id: str, table_source_map: Dict[str, str], sql: str) -> FederatedExecutionPlan:
        subplans = []
        for i, (tbl, ds) in enumerate(table_source_map.items()):
            subplans.append(FederatedSubqueryPlan(
                plan_id=f"sub_{i}_{tbl}",
                target_data_source=ds,
                sql_text=f"SELECT * FROM {tbl}",
                estimated_rows=100000,
                pushdown_filters=[]
            ))

        return FederatedExecutionPlan(
            query_id=query_id,
            subplans=subplans,
            join_strategy="BROADCAST_HASH_JOIN",
            final_projections=["*"]
        )
