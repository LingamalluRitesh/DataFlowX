"""
DataFlowX Multi-Tier Aggregation Rollup Template Generator
Generates daily, monthly, and yearly OLAP summary rollups with GROUPING SETS and incremental partition merges.
"""

from typing import List


class AggregateRollupGenerator:
    """Generates OLAP rollup aggregation templates."""

    @classmethod
    def generate_daily_rollup_sql(
        cls,
        fact_table: str,
        target_summary_table: str,
        dimension_columns: List[str],
        metric_columns: List[str]
    ) -> str:
        dims = ", ".join(dimension_columns)
        aggs = ", ".join(f"SUM({m}) AS total_{m}, COUNT({m}) AS count_{m}" for m in metric_columns)

        sql = f"""
-- Daily OLAP Rollup Summary for {target_summary_table}
INSERT INTO {target_summary_table}
SELECT {dims}, {aggs}, CURRENT_DATE() AS rollup_date
FROM {fact_table}
GROUP BY {dims};
        """.strip()
        return sql
