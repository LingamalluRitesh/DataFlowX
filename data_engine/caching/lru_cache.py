"""
DataFlowX Thread-Safe LRU In-Memory Cache with Memory Footprint Caps
Maintains doubly-linked hash map of cached query batches with byte memory limits, TTL expiration, and hit/miss counters.
"""

from collections import OrderedDict
import threading
import time
from typing import Any, Dict, Optional, Tuple


class ThreadSafeLRUCache:
    """Thread-safe LRU cache with memory size tracking."""

    def __init__(self, max_entries: int = 1000, max_memory_bytes: int = 104857600):  # 100MB default
        self.max_entries = max_entries
        self.max_memory_bytes = max_memory_bytes
        self._cache: OrderedDict[str, Tuple[Any, float, int]] = OrderedDict()  # key -> (value, expiry_unix, size_bytes)
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        now = time.time()
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            val, expiry, size = self._cache[key]
            if expiry > 0 and now > expiry:
                del self._cache[key]
                self._misses += 1
                return None
            self._cache.move_to_end(key)
            self._hits += 1
            return val

    def put(self, key: str, value: Any, ttl_seconds: int = 3600, size_bytes: int = 1024) -> None:
        expiry = time.time() + ttl_seconds if ttl_seconds > 0 else 0
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (value, expiry, size_bytes)
            while len(self._cache) > self.max_entries:
                self._cache.popitem(last=False)
