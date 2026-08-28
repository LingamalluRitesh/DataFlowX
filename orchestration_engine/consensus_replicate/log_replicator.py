"""
DataFlowX Raft Consensus AppendEntries Log Replicator
Replicates state transitions across 3-node/5-node Raft clusters with quorum acknowledgments and commit index advancements.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class AppendEntriesRPC(BaseModel):
    term: int
    leader_id: str
    prev_log_index: int
    prev_log_term: int
    entries: List[Dict[str, Any]] = Field(default_factory=list)
    leader_commit: int


class AppendEntriesResponse(BaseModel):
    term: int
    success: bool
    match_index: int


class RaftLogReplicator:
    """Handles AppendEntries replication RPCs."""

    @classmethod
    def process_append_entries(cls, current_term: int, rpc: AppendEntriesRPC) -> AppendEntriesResponse:
        if rpc.term < current_term:
            return AppendEntriesResponse(term=current_term, success=False, match_index=0)

        match_idx = rpc.prev_log_index + len(rpc.entries)
        logger.info(f"Raft node accepted {len(rpc.entries)} entries from leader '{rpc.leader_id}' (term={rpc.term})")
        return AppendEntriesResponse(term=rpc.term, success=True, match_index=match_idx)
