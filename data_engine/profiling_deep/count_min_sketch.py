"""
DataFlowX Count-Min Sketch Heavy-Hitter Frequency Estimator
Probabilistic 2D array matrix with multiple independent hash functions for estimating top frequent items in streaming pipelines with bounded error.
"""

import hashlib
from typing import Any, List
import numpy as np


class CountMinSketch:
    """Probabilistic frequency estimation data structure."""

    def __init__(self, depth: int = 5, width: int = 2000):
        self.depth = depth
        self.width = width
        self.table = np.zeros((depth, width), dtype=np.uint32)

    def _hash(self, item: str, seed: int) -> int:
        raw = f"{seed}:{item}".encode("utf-8")
        return int(hashlib.md5(raw).hexdigest()[:8], 16) % self.width

    def add(self, item: Any, count: int = 1) -> None:
        item_str = str(item)
        for d in range(self.depth):
            col = self._hash(item_str, d)
            self.table[d, col] += count

    def estimate_frequency(self, item: Any) -> int:
        item_str = str(item)
        min_val = float("inf")
        for d in range(self.depth):
            col = self._hash(item_str, d)
            min_val = min(min_val, self.table[d, col])
        return int(min_val)
