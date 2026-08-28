"""
DataFlowX Streaming Session Window Merger
Merges overlapping and gap-adjacent session windows when late-arriving events bridge the gap between two existing session windows.
"""

from typing import List
from pydantic import BaseModel


class TimeSessionWindow(BaseModel):
    window_id: str
    user_id: str
    start_ms: int
    end_ms: int
    event_count: int


class SessionWindowMerger:
    """Merges adjacent and overlapping session windows."""

    @classmethod
    def merge_windows(cls, windows: List[TimeSessionWindow], gap_threshold_ms: int = 1800000) -> List[TimeSessionWindow]:
        if not windows:
            return []

        sorted_wins = sorted(windows, key=lambda w: w.start_ms)
        merged: List[TimeSessionWindow] = [sorted_wins[0]]

        for current in sorted_wins[1:]:
            prev = merged[-1]
            # Check overlap or gap within threshold
            if current.start_ms <= (prev.end_ms + gap_threshold_ms):
                # Merge into previous
                merged[-1] = TimeSessionWindow(
                    window_id=f"{prev.window_id}+{current.window_id}",
                    user_id=prev.user_id,
                    start_ms=min(prev.start_ms, current.start_ms),
                    end_ms=max(prev.end_ms, current.end_ms),
                    event_count=prev.event_count + current.event_count
                )
            else:
                merged.append(current)

        return merged
