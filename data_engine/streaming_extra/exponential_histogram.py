"""
DataFlowX Exponential Histogram Bucket Accumulator
Implements OpenTelemetry exponential boundary histogram bucketing with scale factors for high-resolution streaming latency percentiles.
"""

import math
from typing import Dict, List
from pydantic import BaseModel, Field


class ExponentialHistogram(BaseModel):
    scale: int
    zero_count: int = 0
    positive_buckets: Dict[int, int] = Field(default_factory=dict)
    min_value: float = float("inf")
    max_value: float = float("-inf")
    total_count: int = 0
    sum_values: float = 0.0


class ExponentialHistogramAccumulator:
    """Accumulates values into exponential histogram buckets."""

    def __init__(self, scale: int = 3):  # 2^(2^-scale) base
        self.scale = scale
        self.base = 2.0 ** (2.0 ** -scale)
        self.hist = ExponentialHistogram(scale=scale)

    def record_value(self, value: float) -> None:
        if value < 0:
            return
        self.hist.total_count += 1
        self.hist.sum_values += value
        self.hist.min_value = min(self.hist.min_value, value)
        self.hist.max_value = max(self.hist.max_value, value)

        if value == 0:
            self.hist.zero_count += 1
            return

        bucket_idx = int(math.floor(math.log(value, self.base)))
        self.hist.positive_buckets[bucket_idx] = self.hist.positive_buckets.get(bucket_idx, 0) + 1

    def get_summary(self) -> ExponentialHistogram:
        return self.hist
