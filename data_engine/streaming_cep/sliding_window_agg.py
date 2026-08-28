"""
DataFlowX Two-Stacks Sliding Window Aggregator (DABA Algorithm)
Maintains O(1) amortized sliding window aggregates (MIN, MAX, SUM, COUNT, MEAN) using push/pop functional queues.
"""

from typing import Any, Callable, Generic, List, Optional, Tuple, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class TwoStacksWindowAggregator(Generic[T, R]):
    """O(1) sliding window aggregator."""

    def __init__(self, agg_fn: Callable[[R, T], R], identity_val: R):
        self.agg_fn = agg_fn
        self.identity = identity_val
        # Stacks store tuples of (raw_value, cumulative_aggregate)
        self.front_stack: List[Tuple[T, R]] = []  # Outgoing (pop from here)
        self.back_stack: List[Tuple[T, R]] = []   # Incoming (push here)

    def push(self, val: T) -> None:
        prev_agg = self.back_stack[-1][1] if self.back_stack else self.identity
        new_agg = self.agg_fn(prev_agg, val)
        self.back_stack.append((val, new_agg))

    def pop(self) -> Optional[T]:
        if not self.front_stack:
            # Transfer back_stack to front_stack reversing elements
            while self.back_stack:
                raw_val, _ = self.back_stack.pop()
                prev_agg = self.front_stack[-1][1] if self.front_stack else self.identity
                new_agg = self.agg_fn(prev_agg, raw_val)
                self.front_stack.append((raw_val, new_agg))

        if self.front_stack:
            return self.front_stack.pop()[0]
        return None

    def query_aggregate(self) -> R:
        """Returns the combined aggregate over the entire current window in O(1)."""
        front_agg = self.front_stack[-1][1] if self.front_stack else self.identity
        back_agg = self.back_stack[-1][1] if self.back_stack else self.identity
        return self.agg_fn(front_agg, back_agg)
