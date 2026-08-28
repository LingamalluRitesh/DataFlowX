"""
DataFlowX Probabilistic Split-Block Bloom Filter
Applies XXH64 / Murmur3 hash seeds across bit-arrays to enable zero-I/O row group skipping during Parquet and Delta Lake point lookups.
"""

import hashlib
import math
from typing import Any, List, Optional
import numpy as np


class SplitBlockBloomFilter:
    """Probabilistic Bloom filter for row group pruning."""

    def __init__(self, expected_entries: int = 10000, false_positive_rate: float = 0.01):
        self.expected_entries = expected_entries
        self.fpp = false_positive_rate
        # Calculate optimal number of bits and hash functions
        self.num_bits = int(- (expected_entries * math.log(false_positive_rate)) / (math.log(2) ** 2))
        self.num_hashes = int((self.num_bits / expected_entries) * math.log(2))
        self.bit_array = np.zeros(self.num_bits, dtype=bool)

    def _hashes(self, item: str) -> List[int]:
        h1 = int(hashlib.sha256(item.encode("utf-8")).hexdigest()[:16], 16)
        h2 = int(hashlib.md5(item.encode("utf-8")).hexdigest()[:16], 16)
        positions = []
        for i in range(self.num_hashes):
            pos = (h1 + i * h2) % self.num_bits
            positions.append(pos)
        return positions

    def add(self, item: Any) -> None:
        item_str = str(item)
        for pos in self._hashes(item_str):
            self.bit_array[pos] = True

    def contains(self, item: Any) -> bool:
        item_str = str(item)
        for pos in self._hashes(item_str):
            if not self.bit_array[pos]:
                return False  # Definitely not in set
        return True  # Probably in set
