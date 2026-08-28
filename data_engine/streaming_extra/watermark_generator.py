"""
DataFlowX Bounded Out-of-Orderness Streaming Watermark Emitter
Emits monotonic event-time watermarks tracking max event timestamps minus configurable allowed lateness delays (e.g. 5000ms).
"""

from typing import Optional
from pydantic import BaseModel


class Watermark(BaseModel):
    timestamp_ms: int
    allowed_lateness_ms: int
    is_late_event_dropped: bool = False


class BoundedOutOfOrdernessWatermarkGenerator:
    """Emits streaming event-time watermarks."""

    def __init__(self, allowed_lateness_ms: int = 5000):
        self.allowed_lateness_ms = allowed_lateness_ms
        self.max_timestamp_observed_ms = 0

    def process_event_timestamp(self, event_timestamp_ms: int) -> Watermark:
        if event_timestamp_ms > self.max_timestamp_observed_ms:
            self.max_timestamp_observed_ms = event_timestamp_ms

        current_watermark_ms = max(0, self.max_timestamp_observed_ms - self.allowed_lateness_ms)
        is_late = event_timestamp_ms < current_watermark_ms

        return Watermark(
            timestamp_ms=current_watermark_ms,
            allowed_lateness_ms=self.allowed_lateness_ms,
            is_late_event_dropped=is_late
        )
