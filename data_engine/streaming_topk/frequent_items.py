"""
DataFlowX Misra-Gries Streaming Frequent Items Summary
Implements Misra-Gries streaming algorithm to identify elements appearing more than (1/k) fraction of total stream items.
"""

from typing import Any, Dict, List, Tuple


class MisraGriesFrequentItems:
    """Misra-Gries streaming frequency summary."""

    def __init__(self, k: int = 10):
        self.k = k
        self.counters: Dict[Any, int] = {}

    def process_item(self, item: Any) -> None:
        if item in self.counters:
            self.counters[item] += 1
        elif len(self.counters) < self.k - 1:
            self.counters[item] = 1
        else:
            # Decrement all counters
            to_delete = []
            for key in self.counters:
                self.counters[key] -= 1
                if self.counters[key] == 0:
                    to_delete.append(key)
            for key in to_delete:
                del self.counters[key]

    def get_frequent_items(self) -> Dict[Any, int]:
        return dict(self.counters)
