"""
DataFlowX Cross-Engine Dialect Function Rewriter
Converts abstract SQL AST functions into target connector SQL dialects for remote pushdown execution.
"""

from typing import Dict
from data_engine.federation.pushdown_planner import PushdownSubPlan


class DialectRewriter:
    """Renders pushdown sub-plan into remote dialect SQL string."""

    @classmethod
    def render_sql(cls, plan: PushdownSubPlan) -> str:
        cols = ", ".join(plan.pushed_columns) if plan.pushed_columns else "*"
        sql = f"SELECT {cols} FROM {plan.physical_table}"
        if plan.pushed_filters:
            sql += " WHERE " + " AND ".join(plan.pushed_filters)
        if plan.limit is not None:
            sql += f" LIMIT {plan.limit}"
        return sql
