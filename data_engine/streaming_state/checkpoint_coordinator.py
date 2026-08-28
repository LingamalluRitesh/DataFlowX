"""
DataFlowX Chandy-Lamport Distributed Checkpoint Coordinator
Coordinates synchronous and asynchronous barrier snapshots across streaming operators for exactly-once processing guarantees.
"""

from datetime import datetime, timezone
import time
from typing import Dict, List, Optional, Set
from pydantic import BaseModel, Field


class CheckpointBarrier(BaseModel):
    checkpoint_id: int
    timestamp_ms: int
    is_savepoint: bool = False


class OperatorCheckpointMeta(BaseModel):
    operator_id: str
    checkpoint_id: int
    state_size_bytes: int
    state_storage_path: str
    acknowledged_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CheckpointSnapshot(BaseModel):
    checkpoint_id: int
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    total_state_size_bytes: int = 0
    is_completed: bool = False
    operator_states: Dict[str, OperatorCheckpointMeta] = Field(default_factory=dict)


class CheckpointCoordinator:
    """Coordinates distributed Chandy-Lamport barrier alignment."""

    def __init__(self, registered_operators: List[str], checkpoint_interval_ms: int = 10000):
        self.registered_operators = set(registered_operators)
        self.checkpoint_interval_ms = checkpoint_interval_ms
        self.current_checkpoint_id = 0
        self.active_checkpoints: Dict[int, CheckpointSnapshot] = {}

    def trigger_checkpoint(self, is_savepoint: bool = False) -> CheckpointBarrier:
        self.current_checkpoint_id += 1
        cid = self.current_checkpoint_id
        snapshot = CheckpointSnapshot(checkpoint_id=cid)
        self.active_checkpoints[cid] = snapshot
        return CheckpointBarrier(
            checkpoint_id=cid,
            timestamp_ms=int(time.time() * 1000),
            is_savepoint=is_savepoint
        )

    def acknowledge_operator_checkpoint(self, meta: OperatorCheckpointMeta) -> bool:
        cid = meta.checkpoint_id
        if cid not in self.active_checkpoints:
            return False

        snap = self.active_checkpoints[cid]
        snap.operator_states[meta.operator_id] = meta
        snap.total_state_size_bytes += meta.state_size_bytes

        # Check if all operators acknowledged
        if set(snap.operator_states.keys()) == self.registered_operators:
            snap.is_completed = True
            snap.completed_at = datetime.now(timezone.utc)
            return True

        return False
