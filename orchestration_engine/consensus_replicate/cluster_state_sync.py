"""
DataFlowX Replicated State Machine Synchronizer
Applies committed log entries to the local in-memory catalog and pipeline run table across all cluster followers.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class ClusterNodeInfo(BaseModel):
    node_id: str
    address: str
    role: str  # LEADER, FOLLOWER, CANDIDATE
    last_heartbeat_unix: float
    last_log_index: int


class ClusterStateSynchronizer:
    """Synchronizes cluster membership and state machine transitions."""

    def __init__(self, local_node_id: str):
        self.local_node_id = local_node_id
        self.nodes: Dict[str, ClusterNodeInfo] = {}

    def register_node(self, node: ClusterNodeInfo) -> None:
        self.nodes[node.node_id] = node
        logger.info(f"Registered cluster node '{node.node_id}' ({node.role}) at '{node.address}'")

    def get_cluster_status(self) -> List[ClusterNodeInfo]:
        return list(self.nodes.values())
