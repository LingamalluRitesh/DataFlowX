"""
DataFlowX Lakehouse Git-Like Snapshot Branching Manager
Implements Iceberg and Delta Lake table branching: creates isolated write branches from historical snapshots without copying physical Parquet files.
"""

from datetime import datetime, timezone
import time
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class TableBranch(BaseModel):
    branch_name: str
    base_snapshot_id: int
    head_snapshot_id: int
    created_at_utc: str
    is_main: bool = False


class LakehouseBranchManager:
    """Manages table snapshot branches."""

    def __init__(self, table_name: str, main_snapshot_id: int = 1):
        self.table_name = table_name
        self.branches: Dict[str, TableBranch] = {
            "main": TableBranch(
                branch_name="main",
                base_snapshot_id=main_snapshot_id,
                head_snapshot_id=main_snapshot_id,
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                is_main=True
            )
        }

    def create_branch(self, branch_name: str, from_snapshot_id: Optional[int] = None) -> TableBranch:
        if branch_name in self.branches:
            raise ValueError(f"Branch '{branch_name}' already exists in table '{self.table_name}'")

        base_id = from_snapshot_id or self.branches["main"].head_snapshot_id
        branch = TableBranch(
            branch_name=branch_name,
            base_snapshot_id=base_id,
            head_snapshot_id=base_id,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            is_main=False
        )
        self.branches[branch_name] = branch
        logger.info(f"Created Lakehouse branch '{branch_name}' from snapshot {base_id} on table '{self.table_name}'")
        return branch
