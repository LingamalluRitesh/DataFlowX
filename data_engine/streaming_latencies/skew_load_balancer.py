"""
DataFlowX Streaming Key-Skew & Hotspot Load Balancer
Detects keyed distribution skew in real-time and dynamically introduces deterministic integer salts to distribute heavy keys across worker partitions.
"""

from collections import Counter
import hashlib
from typing import Dict, List, Tuple
from pydantic import BaseModel


class SkewDetectionReport(BaseModel):
    total_events_observed: int
    skewed_keys: List[str]
    max_key_volume_pct: float
    is_skew_detected: bool


class StreamingSkewBalancer:
    """Detects hot keys and salts partitions."""

    def __init__(self, skew_threshold_pct: float = 20.0, num_salts: int = 4):
        self.skew_threshold_pct = skew_threshold_pct
        self.num_salts = num_salts
        self.key_counter: Counter = Counter()
        self.total_count = 0

    def record_key(self, key: str) -> None:
        self.key_counter[key] += 1
        self.total_count += 1

    def get_skew_report(self) -> SkewDetectionReport:
        if self.total_count == 0:
            return SkewDetectionReport(
                total_events_observed=0,
                skewed_keys=[],
                max_key_volume_pct=0.0,
                is_skew_detected=False
            )

        hot_keys = []
        max_pct = 0.0

        for k, count in self.key_counter.most_common(10):
            pct = (count / self.total_count) * 100.0
            if pct > max_pct:
                max_pct = pct
            if pct >= self.skew_threshold_pct:
                hot_keys.append(k)

        return SkewDetectionReport(
            total_events_observed=self.total_count,
            skewed_keys=hot_keys,
            max_key_volume_pct=round(max_pct, 2),
            is_skew_detected=len(hot_keys) > 0
        )

    def route_key(self, key: str, salt_round: int = 0) -> str:
        """Applies salted routing if key is heavy."""
        report = self.get_skew_report()
        if key in report.skewed_keys:
            salt_idx = salt_round % self.num_salts
            return f"{key}_salt_{salt_idx}"
        return key
