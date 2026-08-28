"""
DataFlowX Idempotent CDC WAL Merge Pipeline Template Generator
Generates deduplicated, idempotent SQL MERGE operations for Debezium CDC change feeds handling INSERT, UPDATE, and DELETE operations.
"""

from typing import List


class CDCMergeGenerator:
    """Generates CDC WAL merge templates."""

    @classmethod
    def generate_cdc_merge_sql(
        cls,
        target_table: str,
        cdc_staging_table: str,
        primary_keys: List[str],
        column_list: List[str]
    ) -> str:
        pk_join = " AND ".join(f"t.{k} = s.{k}" for k in primary_keys)
        update_set = ", ".join(f"t.{c} = s.{c}" for c in column_list if c not in primary_keys)
        insert_cols = ", ".join(column_list)
        insert_vals = ", ".join(f"s.{c}" for c in column_list)

        sql = f"""
-- Idempotent CDC Upsert/Delete Merge for {target_table}
MERGE INTO {target_table} AS t
USING (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY {', '.join(primary_keys)} ORDER BY _cdc_lsn DESC) AS _rn
  FROM {cdc_staging_table}
) AS s
ON {pk_join} AND s._rn = 1
WHEN MATCHED AND s._op = 'd' THEN
  DELETE
WHEN MATCHED AND s._op IN ('u', 'r') THEN
  UPDATE SET {update_set}
WHEN NOT MATCHED AND s._op IN ('c', 'r', 'u') THEN
  INSERT ({insert_cols}) VALUES ({insert_vals});
        """.strip()
        return sql
