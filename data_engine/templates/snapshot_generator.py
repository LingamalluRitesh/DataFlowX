"""
DataFlowX Point-in-Time Periodic Snapshot Pipeline Template Generator
Generates daily and hourly partitioned table snapshot pipelines with partition overwrite semantics.
"""

class SnapshotPipelineGenerator:
    """Generates snapshot extraction SQL."""

    @classmethod
    def generate_snapshot_sql(cls, source_table: str, snapshot_table: str, snapshot_date: str = "CURRENT_DATE()") -> str:
        sql = f"""
-- Partitioned Periodic Snapshot for {snapshot_table}
INSERT OVERWRITE {snapshot_table} PARTITION (snapshot_dt = {snapshot_date})
SELECT *, {snapshot_date} AS snapshot_dt
FROM {source_table};
        """.strip()
        return sql
