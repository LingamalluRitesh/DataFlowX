"""
DataFlowX Count-Based Sliding & Tumbling Window Operator
Maintains tumbling count (e.g. every 100 elements) and sliding count (e.g. window 100, slide 20) stream buffers.
"""

from collections import deque
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class CountWindowOperator(Generic[T, R]):
    """Manages count-based window evaluation."""

    def __init__(self, size: int, slide: Optional[int] = None, reduce_fn: Optional[Callable[[List[T]], R]] = None):
        self.size = size
        self.slide = slide or size  # If slide == size, tumbling window
        self.reduce_fn = reduce_fn or (lambda x: x)
        self.buffer: deque[T] = deque()
        self.count_since_last_slide = 0

    def add_element(self, element: T) -> List[R]:
        """Adds element and returns any triggered window reductions."""
        self.buffer.append(element)
        self.count_since_last_slide += 1
        results = []

        if len(self.buffer) >= self.size and self.count_since_last_slide >= self.slide:
            window_elements = list(self.buffer)[-self.size:]
            reduced = self.reduce_fn(window_elements)
            results.append(reduced)
            self.count_since_last_slide = 0

            # Evict elements if buffer exceeds capacity
            while len(self.buffer) > self.size * 2:
                self.buffer.popleft()

        return results
