"""
DataFlowX Event-Time Watermark Tracker
Handles out-of-order records and defines progressive watermarks for bounded streaming execution.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class WatermarkState(BaseModel):
    current_watermark_unix: float = 0.0
    max_event_time_seen: float = 0.0
    allowed_lateness_seconds: float = 30.0
    late_records_dropped: int = 0


class WatermarkTracker:
    """Tracks highest seen event timestamps and computes moving watermarks."""

    def __init__(self, allowed_lateness_seconds: float = 30.0):
        self.state = WatermarkState(allowed_lateness_seconds=allowed_lateness_seconds)

    def process_event_timestamp(self, event_timestamp_unix: float) -> bool:
        """
        Evaluate if event is on-time or should be dropped.
        Returns True if accepted, False if dropped due to lateness.
        """
        if event_timestamp_unix > self.state.max_event_time_seen:
            self.state.max_event_time_seen = event_timestamp_unix
            self.state.current_watermark_unix = max(0.0, event_timestamp_unix - self.state.allowed_lateness_seconds)

        if event_timestamp_unix < self.state.current_watermark_unix:
            self.state.late_records_dropped += 1
            return False

        return True
