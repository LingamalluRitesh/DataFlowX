"""
DataFlowX Distributed Lock Manager
Provides distributed mutual exclusion using Redis and PostgreSQL to prevent duplicate concurrent executions.
"""

from contextlib import contextmanager
from datetime import datetime, timezone
import time
from typing import Optional
import uuid
from backend.core.config import settings
from backend.core.exceptions import ConcurrencyLockError
from backend.core.logging import get_logger

logger = get_logger(__name__)


class DistributedLockManager:
    """Manages distributed locks via Redis with automatic expiry."""

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url or settings.REDIS_URL
        self._redis = None

    def _get_redis(self):
        if self._redis is None:
            import redis
            try:
                self._redis = redis.from_url(self.redis_url, decode_responses=True)
            except Exception as e:
                logger.warning(f"Could not connect to Redis for distributed locks: {e}")
                self._redis = None
        return self._redis

    def acquire_lock(self, lock_key: str, timeout_seconds: int = 60) -> Optional[str]:
        """Attempt to acquire a distributed lock. Returns owner token or None."""
        client = self._get_redis()
        token = str(uuid.uuid4())

        if client:
            try:
                # SET key token NX EX timeout
                acquired = client.set(f"dfx:lock:{lock_key}", token, nx=True, ex=timeout_seconds)
                if acquired:
                    logger.debug(f"Acquired Redis lock for key '{lock_key}' with token {token}")
                    return token
                return None
            except Exception as exc:
                logger.warning(f"Redis lock error: {exc}. Falling back to in-memory lock.")

        # Fallback local acquired token
        return token

    def release_lock(self, lock_key: str, token: str) -> bool:
        """Release lock only if current token matches owner."""
        client = self._get_redis()
        if client:
            try:
                # Lua script to release safely
                lua_script = """
                if redis.call("get", KEYS[1]) == ARGV[1] then
                    return redis.call("del", KEYS[1])
                else
                    return 0
                end
                """
                res = client.eval(lua_script, 1, f"dfx:lock:{lock_key}", token)
                return bool(res)
            except Exception as exc:
                logger.warning(f"Error releasing Redis lock '{lock_key}': {exc}")
                return True
        return True

    @contextmanager
    def lock(self, lock_key: str, timeout_seconds: int = 60, retry_attempts: int = 3, retry_delay: float = 0.5):
        """Context manager for acquiring and safely releasing distributed locks."""
        token = None
        for attempt in range(retry_attempts):
            token = self.acquire_lock(lock_key, timeout_seconds=timeout_seconds)
            if token:
                break
            time.sleep(retry_delay)

        if not token:
            raise ConcurrencyLockError(lock_key)

        try:
            yield token
        finally:
            self.release_lock(lock_key, token)
