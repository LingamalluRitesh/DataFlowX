"""
DataFlowX Slowly Changing Dimension Type 2 (SCD2) Pipeline Template Generator
Generates complete SQL MERGE statements and Python transformations for tracking historical record versions with effective_date, end_date, and is_current flags.
"""

from typing import List


class SCDType2Generator:
    """Generates SCD-2 dimension pipelines."""

    @classmethod
    def generate_merge_sql(
        cls,
        target_table: str,
        source_view: str,
        natural_keys: List[str],
        tracked_attributes: List[str]
    ) -> str:
        key_clause = " AND ".join(f"target.{k} = source.{k}" for k in natural_keys)
        attr_diff = " OR ".join(f"target.{a} != source.{a}" for a in tracked_attributes)

        sql = f"""
-- SCD Type 2 Merge Pipeline for {target_table}
MERGE INTO {target_table} AS target
USING {source_view} AS source
ON {key_clause} AND target.is_current = TRUE
WHEN MATCHED AND ({attr_diff}) THEN
  UPDATE SET target.end_date = CURRENT_TIMESTAMP(), target.is_current = FALSE;

INSERT INTO {target_table}
SELECT source.*, CURRENT_TIMESTAMP() AS effective_date, NULL AS end_date, TRUE AS is_current
FROM {source_view} AS source;
        """.strip()
        return sql
