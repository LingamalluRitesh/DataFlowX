"""
DataFlowX Raft Leader Lease & Fencing Token Generator
Issues monotonic fencing tokens to prevent split-brain dual-leader writes during network partitions.
"""

from datetime import datetime, timezone
import time
from typing import Optional
from pydantic import BaseModel

from backend.core.logging import get_logger

logger = get_logger(__name__)


class LeaderLease(BaseModel):
    leader_id: str
    term: int
    fencing_token: int
    lease_expires_unix: float
    is_valid: bool = True


class LeaderLeaseManager:
    """Manages leader leases and monotonic fencing tokens."""

    def __init__(self, lease_duration_seconds: float = 5.0):
        self.lease_duration_seconds = lease_duration_seconds
        self._current_fencing_token = 1000

    def issue_lease(self, leader_id: str, term: int) -> LeaderLease:
        self._current_fencing_token += 1
        now = time.time()
        lease = LeaderLease(
            leader_id=leader_id,
            term=term,
            fencing_token=self._current_fencing_token,
            lease_expires_unix=now + self.lease_duration_seconds,
            is_valid=True
        )
        logger.info(f"Issued leader lease to '{leader_id}' (term={term}, fencing_token={lease.fencing_token})")
        return lease
