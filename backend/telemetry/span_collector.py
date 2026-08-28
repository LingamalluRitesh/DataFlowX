"""
DataFlowX Microsecond Span Collector & Trace Aggregator
Collects high-resolution microsecond spans for each DAG node execution, tracking IO wait, SIMD evaluation, and network serialization times.
"""

import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class OpenTelemetrySpan(BaseModel):
    span_id: str
    trace_id: str
    parent_span_id: Optional[str] = None
    name: str
    start_time_unix_nano: int
    end_time_unix_nano: int
    duration_ms: float
    attributes: Dict[str, Any] = Field(default_factory=dict)


class SpanCollector:
    """Collects tracing spans."""

    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.spans: List[OpenTelemetrySpan] = []

    def record_span(self, name: str, duration_ms: float, attributes: Optional[Dict[str, Any]] = None) -> OpenTelemetrySpan:
        import secrets
        now_ns = int(time.time() * 1e9)
        dur_ns = int(duration_ms * 1e6)
        span = OpenTelemetrySpan(
            span_id=secrets.token_hex(8),
            trace_id=self.trace_id,
            name=name,
            start_time_unix_nano=now_ns - dur_ns,
            end_time_unix_nano=now_ns,
            duration_ms=duration_ms,
            attributes=attributes or {}
        )
        self.spans.append(span)
        return span
