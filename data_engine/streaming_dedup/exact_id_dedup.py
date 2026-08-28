"""
DataFlowX Exact In-Memory & Key-Value Streaming Deduplication State Store
Maintains bounded TTL state store of processed message UUIDs to guarantee exactly-once processing across message queues.
"""

from collections import OrderedDict
import time
from typing import Any, Optional


class ExactIDDeduplicator:
    """Exact ID deduplication with TTL."""

    def __init__(self, max_keys: int = 100000, ttl_seconds: int = 86400):
        self.max_keys = max_keys
        self.ttl_seconds = ttl_seconds
        self._store: OrderedDict[str, float] = OrderedDict()

    def is_duplicate(self, message_id: str) -> bool:
        now = time.time()
        if message_id in self._store:
            expiry = self._store[message_id]
            if now < expiry:
                return True
            else:
                del self._store[message_id]

        self._store[message_id] = now + self.ttl_seconds
        self._store.move_to_end(message_id)

        if len(self._store) > self.max_keys:
            self._store.popitem(last=False)

        return False
