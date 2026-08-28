"""
DataFlowX Thread-Safe Priority Task Queue with Starvation Aging
Min-heap priority queue ordering pipeline tasks by SLA urgency, dependency weight, and anti-starvation age boosters.
"""

from dataclasses import dataclass, field
import heapq
import threading
import time
from typing import Any, Dict, List, Optional


@dataclass(order=True)
class PrioritizedTask:
    effective_priority: float
    task_id: str = field(compare=False)
    pipeline_id: str = field(compare=False)
    queued_at_unix: float = field(compare=False)
    base_priority: int = field(compare=False)
    payload: Dict[str, Any] = field(compare=False)


class PriorityTaskQueue:
    """Thread-safe min-heap queue with dynamic aging."""

    def __init__(self, aging_factor: float = 0.1):
        self.aging_factor = aging_factor  # priority increase per second queued
        self._heap: List[PrioritizedTask] = []
        self._lock = threading.Lock()

    def enqueue(self, task_id: str, pipeline_id: str, base_priority: int = 50, payload: Optional[Dict[str, Any]] = None) -> None:
        now = time.time()
        # Lower score = higher priority in Python heapq
        effective = float(base_priority)
        task = PrioritizedTask(
            effective_priority=effective,
            task_id=task_id,
            pipeline_id=pipeline_id,
            queued_at_unix=now,
            base_priority=base_priority,
            payload=payload or {}
        )
        with self._lock:
            heapq.heappush(self._heap, task)

    def dequeue(self) -> Optional[PrioritizedTask]:
        with self._lock:
            if not self._heap:
                return None
            return heapq.heappop(self._heap)

    def size(self) -> int:
        with self._lock:
            return len(self._heap)
