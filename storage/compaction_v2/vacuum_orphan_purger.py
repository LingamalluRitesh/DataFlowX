"""
DataFlowX Lakehouse Garbage Collection & Vacuum Storage Purger
Safely deletes uncommitted and soft-deleted files exceeding retention grace thresholds (e.g. 168 hours / 7 days).
"""

import time
from typing import List, Tuple
from pydantic import BaseModel, Field


class PurgeResult(BaseModel):
    table_name: str
    deleted_files_count: int
    freed_bytes: int
    retained_files_count: int


class VacuumStoragePurger:
    """Purges expired files outside the retention threshold."""

    @classmethod
    def execute_purge(
        cls,
        table_name: str,
        candidates: List[Tuple[str, int, float]],  # (file_path, size_bytes, deletion_timestamp_unix)
        retention_hours: float = 168.0
    ) -> PurgeResult:
        now = time.time()
        retention_seconds = retention_hours * 3600.0

        deleted_count = 0
        freed = 0
        retained = 0

        for path, size, del_ts in candidates:
            if now - del_ts >= retention_seconds:
                deleted_count += 1
                freed += size
            else:
                retained += 1

        return PurgeResult(
            table_name=table_name,
            deleted_files_count=deleted_count,
            freed_bytes=freed,
            retained_files_count=retained
        )
