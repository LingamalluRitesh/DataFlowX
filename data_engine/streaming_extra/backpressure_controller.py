"""
DataFlowX Streaming Adaptive Backpressure Feedback Controller
Monitors worker queue depth and dynamically modulates upstream consumer pull rates to eliminate out-of-memory crashes.
"""

from typing import Dict
from backend.core.logging import get_logger

logger = get_logger(__name__)


class BackpressureController:
    """Modulates ingestion concurrency based on buffer saturation."""

    def __init__(self, high_watermark: float = 0.85, low_watermark: float = 0.40):
        self.high_watermark = high_watermark
        self.low_watermark = low_watermark
        self.is_throttled = False

    def evaluate_saturation(self, queue_size: int, queue_capacity: int) -> bool:
        ratio = queue_size / max(1, queue_capacity)
        if ratio >= self.high_watermark and not self.is_throttled:
            self.is_throttled = True
            logger.warning(f"Backpressure engaged! Queue saturation {ratio*100:.1f}%. Throttling consumer pull rate.")
        elif ratio <= self.low_watermark and self.is_throttled:
            self.is_throttled = False
            logger.info(f"Backpressure released. Queue saturation dropped to {ratio*100:.1f}%.")

        return self.is_throttled
