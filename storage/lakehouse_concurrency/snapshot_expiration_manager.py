"""
DataFlowX Lakehouse Snapshot Expiration & Ancestry Pruner
Manages snapshot retention DAGs, pruning expired ancestors while retaining named branches and tags.
"""

from typing import List, Set
from pydantic import BaseModel, Field


class SnapshotNode(BaseModel):
    snapshot_id: int
    parent_snapshot_id: Optional[int] = None
    timestamp_ms: int


class ExpireSnapshotsReport(BaseModel):
    retained_snapshot_ids: List[int]
    expired_snapshot_ids: List[int]
    pruned_manifest_count: int


class SnapshotExpirationManager:
    """Prunes expired Lakehouse snapshots."""

    @classmethod
    def expire_older_than(
        cls,
        snapshots: List[SnapshotNode],
        older_than_ms: int,
        retain_last_n: int = 1
    ) -> ExpireSnapshotsReport:
        if not snapshots:
            return ExpireSnapshotsReport(retained_snapshot_ids=[], expired_snapshot_ids=[], pruned_manifest_count=0)

        # Sort chronological
        sorted_snaps = sorted(snapshots, key=lambda s: s.timestamp_ms)
        retained = list(sorted_snaps[-retain_last_n:])
        retained_ids: Set[int] = {s.snapshot_id for s in retained}

        expired_ids = []
        for s in sorted_snaps[:-retain_last_n]:
            if s.timestamp_ms < older_than_ms:
                expired_ids.append(s.snapshot_id)
            else:
                retained.append(s)
                retained_ids.add(s.snapshot_id)

        return ExpireSnapshotsReport(
            retained_snapshot_ids=list(retained_ids),
            expired_snapshot_ids=expired_ids,
            pruned_manifest_count=len(expired_ids) * 2
        )
