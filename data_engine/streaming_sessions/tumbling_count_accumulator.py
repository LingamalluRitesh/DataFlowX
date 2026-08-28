"""
DataFlowX Tumbling Count Accumulator with Early Triggers
Accumulates high-throughput streaming events up to fixed count thresholds (e.g. 10,000 events) or early periodic flushes.
"""

from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")
R = TypeVar("R")


class TumblingCountBatch(BaseModel):
    batch_id: int
    element_count: int
    is_early_trigger: bool


class TumblingCountAccumulator(Generic[T, R]):
    """Accumulates batches of size N."""

    def __init__(self, target_count: int = 1000, reduce_fn: Optional[Callable[[List[T]], R]] = None):
        self.target_count = target_count
        self.reduce_fn = reduce_fn or (lambda x: x)
        self.buffer: List[T] = []
        self.batch_counter = 0

    def add_element(self, element: T) -> Optional[R]:
        self.buffer.append(element)
        if len(self.buffer) >= self.target_count:
            return self.flush()
        return None

    def flush(self) -> Optional[R]:
        if not self.buffer:
            return None
        self.batch_counter += 1
        items = list(self.buffer)
        self.buffer.clear()
        return self.reduce_fn(items)
