"""
DataFlowX Sliding Multi-Window Bloom Filter for Streaming Deduplication
Rotates active, warming, and cooling Bloom filter bitsets over sliding time windows to achieve constant-memory duplicate suppression across unbounded streams.
"""

from typing import Any, List
from data_engine.indexing.bloom_filter import LakehouseBloomFilter


class SlidingBloomFilter:
    """Sliding time-window Bloom filter."""

    def __init__(self, window_capacity: int = 100000, num_windows: int = 3):
        self.window_capacity = window_capacity
        self.num_windows = num_windows
        self.filters: List[LakehouseBloomFilter] = [LakehouseBloomFilter(size_bits=window_capacity * 10) for _ in range(num_windows)]

    def contains(self, item: Any) -> bool:
        # Check if item exists in any active window
        for bf in self.filters:
            if bf.contains(item):
                return True
        return False

    def add(self, item: Any) -> None:
        # Add to head filter
        self.filters[0].add(item)

    def rotate_window(self) -> None:
        """Rotates filters: drops oldest, prepends fresh new filter."""
        self.filters.pop()
        self.filters.insert(0, LakehouseBloomFilter(size_bits=self.window_capacity * 10))
