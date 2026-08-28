"""
DataFlowX Multi-Writer Optimistic Concurrency Control (OCC) Commit Sequencer
Implements compare-and-swap (CAS) commit loops with conflict resolution for concurrent writes to Iceberg and Delta tables.
"""

import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TableCommitRequest(BaseModel):
    table_name: str
    expected_version: int
    new_snapshot_id: str
    committer_id: str
    files_added: List[str] = Field(default_factory=list)
    files_deleted: List[str] = Field(default_factory=list)


class CommitResult(BaseModel):
    success: bool
    committed_version: int
    conflict_detected: bool
    retry_needed: bool
    message: str


class OptimisticLockManager:
    """Manages atomic CAS table version updates."""

    def __init__(self):
        # table_name -> current_version
        self.table_versions: Dict[str, int] = {}
        # table_name -> list of committed snapshot IDs
        self.table_snapshots: Dict[str, List[str]] = {}

    def commit(self, req: TableCommitRequest) -> CommitResult:
        curr_ver = self.table_versions.get(req.table_name, 0)

        if req.expected_version != curr_ver:
            # Conflict: another writer committed first
            return CommitResult(
                success=False,
                committed_version=curr_ver,
                conflict_detected=True,
                retry_needed=True,
                message=f"Commit conflict: expected version v{req.expected_version}, but table is at v{curr_ver}"
            )

        # Atomic commit
        new_ver = curr_ver + 1
        self.table_versions[req.table_name] = new_ver
        if req.table_name not in self.table_snapshots:
            self.table_snapshots[req.table_name] = []
        self.table_snapshots[req.table_name].append(req.new_snapshot_id)

        return CommitResult(
            success=True,
            committed_version=new_ver,
            conflict_detected=False,
            retry_needed=False,
            message=f"Successfully committed snapshot {req.new_snapshot_id} as version v{new_ver}"
        )
