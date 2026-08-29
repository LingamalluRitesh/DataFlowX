"""
Event-Time Streaming Watermark & Late Arrival Engine.
Handles out-of-order event streams, bounded latency buffers, and window emission triggers.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class StreamEvent:
    event_id: str
    event_timestamp: float  # Unix timestamp in seconds
    payload: Dict[str, Any]


@dataclass
class WindowResult:
    window_start: float
    window_end: float
    events_count: int
    aggregated_metrics: Dict[str, float]
    is_late_trigger: bool = False


class StreamingWatermarkEngine:
    """Manages event-time progress, monotonic watermarks, and window materializations."""

    def __init__(self, window_size_sec: float = 60.0, allowed_lateness_sec: float = 15.0, max_out_of_orderness_sec: float = 5.0):
        self.window_size = window_size_sec
        self.allowed_lateness = allowed_lateness_sec
        self.max_delay = max_out_of_orderness_sec
        self.current_watermark = 0.0
        self.max_timestamp_observed = 0.0
        self.window_buffers: Dict[Tuple[float, float], List[StreamEvent]] = {}
        self.emitted_windows: List[WindowResult] = []
        self.side_output_dropped_events: List[StreamEvent] = []

    def process_event(self, event: StreamEvent) -> Optional[List[WindowResult]]:
        # Update watermark
        if event.event_timestamp > self.max_timestamp_observed:
            self.max_timestamp_observed = event.event_timestamp
            self.current_watermark = self.max_timestamp_observed - self.max_delay

        # Calculate window boundary
        win_start = (event.event_timestamp // self.window_size) * self.window_size
        win_end = win_start + self.window_size
        win_key = (win_start, win_end)

        # Check if event is too late (dropped to dead letter / side output)
        if event.event_timestamp < (self.current_watermark - self.allowed_lateness):
            self.side_output_dropped_events.append(event)
            return None

        if win_key not in self.window_buffers:
            self.window_buffers[win_key] = []
        self.window_buffers[win_key].append(event)

        # Check for windows ready to emit (window_end <= current_watermark)
        emitted = []
        closed_keys = []
        for (w_s, w_e), events in list(self.window_buffers.items()):
            if w_e <= self.current_watermark:
                total_val = sum(e.payload.get("value", 1.0) for e in events)
                result = WindowResult(
                    window_start=w_s,
                    window_end=w_e,
                    events_count=len(events),
                    aggregated_metrics={"sum_value": total_val, "avg_value": total_val / len(events)},
                    is_late_trigger=False,
                )
                self.emitted_windows.append(result)
                emitted.append(result)
                closed_keys.append((w_s, w_e))

        for k in closed_keys:
            del self.window_buffers[k]

        return emitted if emitted else None
