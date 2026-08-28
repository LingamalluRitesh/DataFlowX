"""
DataFlowX Watermark Ingestion Lag Tracker & Monotonicity Verifier
Monitors real-time difference between wall-clock time and streaming watermark progress, alerting on stalled streams.
"""

import time
from typing import Dict, Optional
from pydantic import BaseModel


class WatermarkLagStatus(BaseModel):
    stream_id: str
    current_watermark_epoch_ms: int
    wallclock_epoch_ms: int
    lag_ms: int
    is_lag_excessive: bool
    is_monotonic: bool


class WatermarkLagTracker:
    """Tracks streaming lag against wallclock time."""

    def __init__(self, max_allowed_lag_ms: int = 5000):
        self.max_allowed_lag_ms = max_allowed_lag_ms
        self.stream_watermarks: Dict[str, int] = {}

    def update_watermark(self, stream_id: str, watermark_ms: int) -> WatermarkLagStatus:
        now_ms = int(time.time() * 1000)
        prev_wm = self.stream_watermarks.get(stream_id, 0)
        is_mono = watermark_ms >= prev_wm

        if is_mono:
            self.stream_watermarks[stream_id] = watermark_ms

        lag = max(0, now_ms - watermark_ms)

        return WatermarkLagStatus(
            stream_id=stream_id,
            current_watermark_epoch_ms=watermark_ms,
            wallclock_epoch_ms=now_ms,
            lag_ms=lag,
            is_lag_excessive=lag > self.max_allowed_lag_ms,
            is_monotonic=is_mono
        )
