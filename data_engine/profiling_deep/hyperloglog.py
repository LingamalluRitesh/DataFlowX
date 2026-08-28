"""
DataFlowX Pure-Python HyperLogLog (HLL) Cardinality Estimator
Estimates distinct count cardinalities over billions of items with 1.04 / sqrt(m) standard error using 16,384 register buckets and harmonic mean bias corrections.
"""

import hashlib
import math
from typing import Any, List
import numpy as np


class HyperLogLog:
    """HyperLogLog distinct element counter."""

    def __init__(self, p: int = 14):  # 2^14 = 16,384 registers
        self.p = p
        self.m = 1 << p
        self.registers = np.zeros(self.m, dtype=np.uint8)

    @staticmethod
    def _hash(value: Any) -> int:
        return int(hashlib.md5(str(value).encode("utf-8")).hexdigest()[:16], 16)

    def add(self, value: Any) -> None:
        x = self._hash(value)
        # Register index: first p bits
        idx = x >> (64 - self.p)
        # Remaining 64 - p bits
        w = x & ((1 << (64 - self.p)) - 1)
        # Count leading zeros + 1
        leading_zeros = (64 - self.p) - w.bit_length() + 1 if w > 0 else (64 - self.p + 1)
        self.registers[idx] = max(self.registers[idx], leading_zeros)

    def estimate_cardinality(self) -> int:
        alpha_m = 0.7213 / (1.0 + 1.079 / self.m)
        z = 1.0 / np.sum(2.0 ** -self.registers.astype(float))
        e = alpha_m * (self.m ** 2) * z

        # Small range correction
        if e <= 2.5 * self.m:
            v = np.sum(self.registers == 0)
            if v > 0:
                e = self.m * math.log(self.m / float(v))

        return int(round(e))
