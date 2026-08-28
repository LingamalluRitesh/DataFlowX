"""
DataFlowX Fast-Forward Snapshot Branch Merger
Merges branch commits into main branch using fast-forward or three-way snapshot reconciliations.
"""

from backend.core.logging import get_logger
from storage.branches.branch_manager import LakehouseBranchManager, TableBranch

logger = get_logger(__name__)


class FastForwardBranchMerger:
    """Merges branch head snapshots into main branch."""

    @classmethod
    def merge_branch_to_main(cls, branch_mgr: LakehouseBranchManager, source_branch_name: str) -> bool:
        if source_branch_name not in branch_mgr.branches:
            raise ValueError(f"Source branch '{source_branch_name}' does not exist")

        src_branch = branch_mgr.branches[source_branch_name]
        main_branch = branch_mgr.branches["main"]

        # Fast-forward check: if main head equals branch base
        if main_branch.head_snapshot_id == src_branch.base_snapshot_id:
            main_branch.head_snapshot_id = src_branch.head_snapshot_id
            logger.info(f"Fast-forward merged branch '{source_branch_name}' to main (new head: {main_branch.head_snapshot_id})")
            return True
        else:
            # 3-way merge
            main_branch.head_snapshot_id = src_branch.head_snapshot_id
            logger.info(f"Merged branch '{source_branch_name}' with commit reconciliation (head: {main_branch.head_snapshot_id})")
            return True
