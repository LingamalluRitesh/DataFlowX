"""
DataFlowX Batched Lakehouse DataLoader
Batches key lookups across nested GraphQL field resolvers into single IN-predicate SQL queries to prevent N+1 performance bottlenecks.
"""

from typing import Any, Callable, Dict, List, Optional
import pandas as pd


class LakehouseDataLoader:
    """Batch key loader for GraphQL nested relationships."""

    def __init__(self, batch_load_fn: Callable[[List[str]], Dict[str, Any]]):
        self.batch_load_fn = batch_load_fn
        self._queue: List[str] = []
        self._cache: Dict[str, Any] = {}

    def load(self, key: str) -> Optional[Any]:
        if key in self._cache:
            return self._cache[key]
        self._queue.append(key)
        return None

    def execute_batch(self) -> Dict[str, Any]:
        if not self._queue:
            return self._cache
        loaded = self.batch_load_fn(self._queue)
        self._cache.update(loaded)
        self._queue.clear()
        return self._cache
