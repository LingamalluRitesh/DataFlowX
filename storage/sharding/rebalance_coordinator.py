"""
DataFlowX Zero-Downtime Shard Rebalance Coordinator
Coordinates online partition migration between storage nodes during cluster scaling without interrupting streaming ingestion or query execution.
"""

from typing import Dict, List
from pydantic import BaseModel
from backend.core.logging import get_logger

logger = get_logger(__name__)


class ShardMigrationTask(BaseModel):
    shard_id: str
    source_node: str
    target_node: str
    status: str = "IN_PROGRESS"


class RebalanceCoordinator:
    """Coordinates partition rebalancing across nodes."""

    @classmethod
    def plan_rebalance(cls, current_allocations: Dict[str, List[str]], new_node_id: str) -> List[ShardMigrationTask]:
        # Emulate rebalance plan
        tasks = []
        for node, shards in current_allocations.items():
            if len(shards) > 1:
                migrated_shard = shards[-1]
                tasks.append(ShardMigrationTask(shard_id=migrated_shard, source_node=node, target_node=new_node_id))
                logger.info(f"Planned migration of shard '{migrated_shard}' from '{node}' to new node '{new_node_id}'")

        return tasks
