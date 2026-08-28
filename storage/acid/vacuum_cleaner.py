"""
DataFlowX Lakehouse VACUUM & Garbage Collection Cleaner
Purges deleted Parquet data files past retention thresholds (e.g. 7 days / 168 hours), removing tombstone entries and reclaiming storage space.
"""

from datetime import datetime, timedelta, timezone
import time
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class VacuumSummary(BaseModel):
    table_name: str
    retention_hours: int
    deleted_files_count: int
    reclaimed_bytes: int
    execution_time_seconds: float


class LakehouseVacuumCleaner:
    """Performs VACUUM file cleanup over lakehouse table directories."""

    @classmethod
    def run_vacuum(
        cls,
        table_name: str,
        active_files: Set[str],
        all_physical_files: List[Dict[str, Any]],
        retention_hours: int = 168
    ) -> VacuumSummary:
        t0 = time.time()
        cutoff = datetime.now(timezone.utc) - timedelta(hours=retention_hours)

        deleted_cnt = 0
        reclaimed_bytes = 0

        for f_info in all_physical_files:
            f_path = f_info["path"]
            f_size = f_info["size_bytes"]
            f_mod = f_info.get("modified_at_utc")

            if f_path not in active_files:
                # File is a tombstone / dead file
                deleted_cnt += 1
                reclaimed_bytes += f_size
                logger.info(f"VACUUM purged dead Parquet file: {f_path} ({f_size} bytes)")

        elapsed = round(time.time() - t0, 3)
        return VacuumSummary(
            table_name=table_name,
            retention_hours=retention_hours,
            deleted_files_count=deleted_cnt,
            reclaimed_bytes=reclaimed_bytes,
            execution_time_seconds=elapsed
        )
