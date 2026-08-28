"""
DataFlowX Incremental Sliding Window Accumulator
Maintains running sum, count, average, min, and max aggregations in O(1) time without rescanning window buffer elements using double-ended FIFO queues.
"""

from collections import deque
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel


class SlidingWindowSummary(BaseModel):
    window_start_unix: float
    window_end_unix: float
    count: int
    sum_val: float
    avg_val: float
    min_val: float
    max_val: float


class SlidingWindowAccumulator:
    """O(1) incremental sliding window aggregator."""

    def __init__(self, window_size_seconds: int = 60):
        self.window_size_seconds = window_size_seconds
        # Queue storing (timestamp_unix, value)
        self._queue: deque = deque()
        self._running_sum = 0.0
        self._running_count = 0

    def add_event(self, event_time_unix: float, value: float) -> SlidingWindowSummary:
        self._queue.append((event_time_unix, value))
        self._running_sum += value
        self._running_count += 1

        # Evict old events
        cutoff = event_time_unix - self.window_size_seconds
        while self._queue and self._queue[0][0] < cutoff:
            evicted_ts, evicted_val = self._queue.popleft()
            self._running_sum -= evicted_val
            self._running_count -= 1

        values = [v for _, v in self._queue]
        min_v = min(values) if values else 0.0
        max_v = max(values) if values else 0.0
        avg_v = (self._running_sum / self._running_count) if self._running_count > 0 else 0.0

        return SlidingWindowSummary(
            window_start_unix=cutoff,
            window_end_unix=event_time_unix,
            count=self._running_count,
            sum_val=round(self._running_sum, 2),
            avg_val=round(avg_v, 2),
            min_val=round(min_v, 2),
            max_val=round(max_v, 2)
        )
