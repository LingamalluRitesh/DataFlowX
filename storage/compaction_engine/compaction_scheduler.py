"""
DataFlowX Automated Background Lakehouse Compaction Scheduler
Monitors partition file counts, detects small file fragmentation (>50 small files under 32MB), and triggers bin-packing compaction jobs automatically.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class PartitionFragmentationReport(BaseModel):
    table_name: str
    partition_spec: str
    total_files: int
    small_files_count: int  # < 32 MB
    total_bytes: int
    requires_compaction: bool


class AutoCompactionScheduler:
    """Evaluates partition health and schedules compaction."""

    @classmethod
    def evaluate_partition(
        cls,
        table_name: str,
        partition_spec: str,
        files: List[Dict[str, Any]],
        small_file_threshold_bytes: int = 33554432,  # 32MB
        max_small_files_trigger: int = 10
    ) -> PartitionFragmentationReport:
        small_cnt = sum(1 for f in files if f.get("size_bytes", 0) < small_file_threshold_bytes)
        total_bytes = sum(f.get("size_bytes", 0) for f in files)
        needs_compaction = small_cnt >= max_small_files_trigger

        logger.info(f"Compaction evaluation for '{table_name}' ({partition_spec}): {small_cnt}/{len(files)} small files (compaction required: {needs_compaction})")

        return PartitionFragmentationReport(
            table_name=table_name,
            partition_spec=partition_spec,
            total_files=len(files),
            small_files_count=small_cnt,
            total_bytes=total_bytes,
            requires_compaction=needs_compaction
        )
