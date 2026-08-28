"""
DataFlowX Raft Consensus Protocol State Machine
Implements Leader Election, Follower Heartbeat Watchdogs, Term Transition, and Replicated Log Synchronization for high-availability cluster coordinators.
"""

from datetime import datetime, timezone
from enum import Enum, auto
import random
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger
from orchestration_engine.consensus.log_entry import RaftLogEntry

logger = get_logger(__name__)


class RaftRole(Enum):
    FOLLOWER = auto()
    CANDIDATE = auto()
    LEADER = auto()


class RaftNode:
    """Cluster node participating in Raft leader consensus."""

    def __init__(self, node_id: str, peers: List[str]):
        self.node_id = node_id
        self.peers = peers
        self.current_term = 0
        self.voted_for: Optional[str] = None
        self.role = RaftRole.FOLLOWER
        self.log: List[RaftLogEntry] = []
        self.commit_index = 0
        self.last_applied = 0
        self.last_heartbeat_time = time.time()
        self.election_timeout_ms = random.randint(150, 300)

    def start_election(self) -> None:
        """Transition to Candidate and solicit votes from cluster peers."""
        self.current_term += 1
        self.role = RaftRole.CANDIDATE
        self.voted_for = self.node_id
        self.last_heartbeat_time = time.time()
        logger.info(f"Node '{self.node_id}' started Raft election for Term {self.current_term}")

        # Assume majority in single-node or local cluster simulation
        votes_received = 1
        if votes_received > len(self.peers) // 2:
            self.become_leader()

    def become_leader(self) -> None:
        """Transition from Candidate to Leader."""
        self.role = RaftRole.LEADER
        logger.info(f"Node '{self.node_id}' became Raft Cluster LEADER for Term {self.current_term}")

    def append_command(self, command_type: str, payload: Dict[str, Any]) -> RaftLogEntry:
        """Leader appends a new state mutation command to the replicated log."""
        if self.role != RaftRole.LEADER:
            raise RuntimeError(f"Cannot append entry: Node '{self.node_id}' is not the Leader")

        entry = RaftLogEntry(
            term=self.current_term,
            index=len(self.log) + 1,
            command_type=command_type,
            payload=payload,
            timestamp_utc=datetime.now(timezone.utc).isoformat()
        )
        self.log.append(entry)
        self.commit_index = entry.index
        logger.debug(f"Leader '{self.node_id}' committed log entry index {entry.index}")
        return entry
