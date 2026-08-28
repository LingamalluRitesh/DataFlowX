"""
DataFlowX CEP Sliding Event Buffer Window
Maintains sorted event buffer queue, handles out-of-order event insertions, and evicts expired events past retention watermark.
"""

from bisect import bisect_left
from typing import Any, Dict, List


class CEPEventWindowBuffer:
    """Sorted sliding buffer for CEP evaluation."""

    def __init__(self, retention_seconds: float = 600.0):
        self.retention_seconds = retention_seconds
        self.events: List[Dict[str, Any]] = []

    def insert_event(self, event: Dict[str, Any]) -> None:
        ts = event.get("timestamp_unix", 0.0)
        # Insertion sort
        pos = 0
        while pos < len(self.events) and self.events[pos].get("timestamp_unix", 0.0) < ts:
            pos += 1
        self.events.insert(pos, event)

        # Evict old events
        cutoff = ts - self.retention_seconds
        while self.events and self.events[0].get("timestamp_unix", 0.0) < cutoff:
            self.events.pop(0)
