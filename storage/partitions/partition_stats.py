"""
DataFlowX Partition Statistics Collector
Collects partition record counts, storage sizes, file counts, and write velocities for storage optimization.
"""

from typing import Dict, List
from pydantic import BaseModel


class PartitionStatistics(BaseModel):
    table_name: str
    partition_value: str
    file_count: int
    total_rows: int
    total_bytes: int


class PartitionStatsCollector:
    """Collects partition level metrics."""

    @classmethod
    def get_stats(cls, table_name: str, partition_value: str, file_count: int, rows: int, bytes_size: int) -> PartitionStatistics:
        return PartitionStatistics(
            table_name=table_name,
            partition_value=partition_value,
            file_count=file_count,
            total_rows=rows,
            total_bytes=bytes_size
        )
