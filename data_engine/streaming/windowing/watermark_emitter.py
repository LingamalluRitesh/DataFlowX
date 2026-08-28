"""
DataFlowX Bounded Out-of-Orderness Watermark Emitter
Tracks maximum observed event timestamps, applies latency bounds, and emits monotonic watermark progressions to trigger late-window computations.
"""

from typing import List, Optional
from pydantic import BaseModel


class WatermarkProgress(BaseModel):
    current_watermark_unix: float
    max_observed_timestamp_unix: float
    allowed_lateness_seconds: float


class BoundedWatermarkEmitter:
    """Emits monotonic watermarks based on max observed event time minus bounded lateness."""

    def __init__(self, allowed_lateness_seconds: float = 5.0):
        self.allowed_lateness_seconds = allowed_lateness_seconds
        self.max_observed_ts: float = 0.0
        self.current_watermark: float = 0.0

    def on_event_time(self, event_time_unix: float) -> WatermarkProgress:
        self.max_observed_ts = max(self.max_observed_ts, event_time_unix)
        calculated_wm = self.max_observed_ts - self.allowed_lateness_seconds
        self.current_watermark = max(self.current_watermark, calculated_wm)

        return WatermarkProgress(
            current_watermark_unix=self.current_watermark,
            max_observed_timestamp_unix=self.max_observed_ts,
            allowed_lateness_seconds=self.allowed_lateness_seconds
        )
