"""
DataFlowX Distributed Lease Lock Primitives
Implements optimistic concurrency locks with TTL timeouts, owner UUID tokens, and fence tokens to prevent split-brain dual-execution.
"""

from datetime import datetime, timezone
import time
from typing import Any, Dict, Optional
import uuid
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class LeaseLockToken(BaseModel):
    resource_id: str
    owner_id: str
    fence_token: int
    expires_at_unix: float


class DistributedLockManager:
    """Manages distributed mutually exclusive locks."""

    def __init__(self):
        self._locks: Dict[str, LeaseLockToken] = {}
        self._fence_counter = 1000

    def acquire_lock(self, resource_id: str, owner_id: str, ttl_seconds: int = 60) -> Optional[LeaseLockToken]:
        now = time.time()
        curr_lock = self._locks.get(resource_id)

        if curr_lock and curr_lock.expires_at_unix > now and curr_lock.owner_id != owner_id:
            # Lock is held by another active owner
            return None

        self._fence_counter += 1
        token = LeaseLockToken(
            resource_id=resource_id,
            owner_id=owner_id,
            fence_token=self._fence_counter,
            expires_at_unix=now + ttl_seconds
        )
        self._locks[resource_id] = token
        logger.info(f"Owner '{owner_id}' acquired lock for '{resource_id}' (fence={token.fence_token})")
        return token

    def release_lock(self, resource_id: str, owner_id: str) -> bool:
        curr_lock = self._locks.get(resource_id)
        if curr_lock and curr_lock.owner_id == owner_id:
            del self._locks[resource_id]
            logger.info(f"Owner '{owner_id}' released lock on '{resource_id}'")
            return True
        return False
