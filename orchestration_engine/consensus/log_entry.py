"""
DataFlowX Raft Consensus Replicated Log Entry Model
Models term number, index, command payload, and commit state across cluster nodes.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class RaftLogEntry(BaseModel):
    term: int
    index: int
    command_type: str  # SCHEDULE_PIPELINE, CANCEL_TASK, ACQUIRE_LEASE, UPDATE_STATE
    payload: Dict[str, Any]
    timestamp_utc: str
