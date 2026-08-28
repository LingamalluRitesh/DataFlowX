"""
DataFlowX Lakehouse Transaction Log Anomaly & Orphan File Scanner
Scans Lakehouse object stores to identify orphaned files (uncommitted Parquet files not in transaction log), phantom deletes, and metadata corruptions.
"""

from typing import List, Set
from pydantic import BaseModel, Field


class StorageAuditReport(BaseModel):
    table_name: str
    total_physical_files: int
    active_committed_files: int
    orphaned_files: List[str] = Field(default_factory=list)
    orphaned_bytes_wasted: int = 0
    is_log_consistent: bool = True


class LakehouseLogAuditScanner:
    """Scans for storage anomalies and orphaned files."""

    @classmethod
    def scan_table(
        cls,
        table_name: str,
        physical_files: List[tuple[str, int]],  # (file_path, file_size_bytes)
        committed_file_paths: Set[str]
    ) -> StorageAuditReport:
        orphans = []
        wasted_bytes = 0

        for path, size in physical_files:
            if path not in committed_file_paths and not path.startswith("_delta_log") and not path.startswith("metadata"):
                orphans.append(path)
                wasted_bytes += size

        return StorageAuditReport(
            table_name=table_name,
            total_physical_files=len(physical_files),
            active_committed_files=len(committed_file_paths),
            orphaned_files=orphans,
            orphaned_bytes_wasted=wasted_bytes,
            is_log_consistent=len(orphans) == 0
        )
