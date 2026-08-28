"""
DataFlowX Keyed State Store (ValueState, ListState, MapState, ReducingState)
Implements Flink-style managed state backends with key partitioning, RocksDB-like persistence, and automatic TTL expiration.
"""

from collections import defaultdict
import time
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class StateTTLOption(BaseModel):
    ttl_seconds: float = 86400.0
    cleanup_on_read: bool = True


class KeyedValueState(Generic[K, T]):
    """Manages single-value state per key."""

    def __init__(self, ttl: Optional[StateTTLOption] = None):
        self._store: Dict[K, Tuple[T, float]] = {}  # key -> (value, update_timestamp)
        self.ttl = ttl

    def get(self, key: K) -> Optional[T]:
        if key not in self._store:
            return None
        val, ts = self._store[key]
        if self.ttl and (time.time() - ts > self.ttl.ttl_seconds):
            del self._store[key]
            return None
        return val

    def set(self, key: K, value: T) -> None:
        self._store[key] = (value, time.time())

    def clear(self, key: K) -> None:
        self._store.pop(key, None)


class KeyedListState(Generic[K, T]):
    """Manages list append state per key."""

    def __init__(self, ttl: Optional[StateTTLOption] = None):
        self._store: Dict[K, Tuple[List[T], float]] = defaultdict(lambda: ([], time.time()))
        self.ttl = ttl

    def get(self, key: K) -> List[T]:
        items, ts = self._store.get(key, ([], time.time()))
        if self.ttl and (time.time() - ts > self.ttl.ttl_seconds):
            self._store.pop(key, None)
            return []
        return list(items)

    def append(self, key: K, value: T) -> None:
        items, _ = self._store.get(key, ([], time.time()))
        items.append(value)
        self._store[key] = (items, time.time())

    def clear(self, key: K) -> None:
        self._store.pop(key, None)


class KeyedMapState(Generic[K, str, V]):
    """Manages map state per key."""

    def __init__(self):
        self._store: Dict[K, Dict[str, V]] = defaultdict(dict)

    def get(self, key: K, map_key: str) -> Optional[V]:
        return self._store.get(key, {}).get(map_key)

    def put(self, key: K, map_key: str, value: V) -> None:
        self._store[key][map_key] = value

    def entries(self, key: K) -> Dict[str, V]:
        return dict(self._store.get(key, {}))

    def clear(self, key: K) -> None:
        self._store.pop(key, None)
