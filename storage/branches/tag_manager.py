"""
DataFlowX Immutable Lakehouse Snapshot Tagging Manager
Creates permanent point-in-time named tags for regulatory audits, model training baselines, and historical financial reporting.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class SnapshotTag(BaseModel):
    tag_name: str
    snapshot_id: int
    created_at_utc: str
    description: Optional[str] = None
    retention_days: Optional[int] = None


class LakehouseTagManager:
    """Manages immutable snapshot tags."""

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.tags: Dict[str, SnapshotTag] = {}

    def create_tag(self, tag_name: str, snapshot_id: int, description: Optional[str] = None, retention_days: Optional[int] = None) -> SnapshotTag:
        tag = SnapshotTag(
            tag_name=tag_name,
            snapshot_id=snapshot_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            description=description,
            retention_days=retention_days
        )
        self.tags[tag_name] = tag
        logger.info(f"Tagged snapshot {snapshot_id} as '{tag_name}' on table '{self.table_name}'")
        return tag
