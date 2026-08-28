"""
DataFlowX Lakehouse Branch & Tag Metadata Manager
Enables Git-style table versioning, named experimental branches, and immutable audit tags on Lakehouse tables.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SnapshotRef(BaseModel):
    ref_name: str
    snapshot_id: int
    ref_type: str  # BRANCH or TAG
    max_ref_age_ms: Optional[int] = None
    max_snapshot_age_ms: Optional[int] = None
    min_snapshots_to_keep: Optional[int] = None


class BranchTagManager:
    """Manages named branches and tags pointing to snapshot IDs."""

    def __init__(self):
        # table_name -> ref_name -> SnapshotRef
        self.refs: Dict[str, Dict[str, SnapshotRef]] = {}

    def create_tag(self, table_name: str, tag_name: str, snapshot_id: int, max_age_ms: Optional[int] = None) -> SnapshotRef:
        if table_name not in self.refs:
            self.refs[table_name] = {}

        ref = SnapshotRef(
            ref_name=tag_name,
            snapshot_id=snapshot_id,
            ref_type="TAG",
            max_ref_age_ms=max_age_ms
        )
        self.refs[table_name][tag_name] = ref
        return ref

    def create_branch(self, table_name: str, branch_name: str, snapshot_id: int) -> SnapshotRef:
        if table_name not in self.refs:
            self.refs[table_name] = {}

        ref = SnapshotRef(
            ref_name=branch_name,
            snapshot_id=snapshot_id,
            ref_type="BRANCH"
        )
        self.refs[table_name][branch_name] = ref
        return ref

    def get_ref(self, table_name: str, ref_name: str) -> Optional[SnapshotRef]:
        return self.refs.get(table_name, {}).get(ref_name)

    def list_refs(self, table_name: str) -> List[SnapshotRef]:
        return list(self.refs.get(table_name, {}).values())
