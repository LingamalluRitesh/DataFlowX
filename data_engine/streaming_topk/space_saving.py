"""
DataFlowX Space-Saving Streaming Heavy-Hitters Algorithm
Maintains Top-K streaming frequency counters with bounded overestimation errors (Metwally et al. Space-Saving).
"""

from typing import Any, Dict, List, Tuple


class SpaceSavingTopK:
    """Space-Saving algorithm for Top-K items."""

    def __init__(self, k: int = 10):
        self.k = k
        self.counts: Dict[Any, int] = {}
        self.errors: Dict[Any, int] = {}

    def add(self, item: Any) -> None:
        if item in self.counts:
            self.counts[item] += 1
        elif len(self.counts) < self.k:
            self.counts[item] = 1
            self.errors[item] = 0
        else:
            # Evict minimum element
            min_item = min(self.counts, key=self.counts.get)
            min_count = self.counts.pop(min_item)
            self.errors.pop(min_item, None)

            self.counts[item] = min_count + 1
            self.errors[item] = min_count

    def get_top_k(self) -> List[Tuple[Any, int, int]]:
        """Returns list of (item, estimated_count, max_error)."""
        sorted_items = sorted(self.counts.items(), key=lambda x: x[1], reverse=True)
        return [(item, count, self.errors.get(item, 0)) for item, count in sorted_items]
