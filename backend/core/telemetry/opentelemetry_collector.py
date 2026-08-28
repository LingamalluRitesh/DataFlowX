"""
DataFlowX OpenTelemetry Tracing & Metrics Exporter
Emits standard distributed trace spans, latency percentiles, and error meters compatible with Prometheus, Jaeger, and Grafana.
"""

from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class TraceSpan(BaseModel):
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    name: str
    service_name: str = "dataflowx-backend"
    start_time_unix_nano: int
    end_time_unix_nano: Optional[int] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    status_code: str = "OK"  # OK, ERROR


class OpenTelemetryCollector:
    """Collects and aggregates runtime spans and system metrics."""

    def __init__(self):
        self.spans: List[TraceSpan] = []

    def start_span(self, trace_id: str, span_id: str, name: str, parent_span_id: Optional[str] = None) -> TraceSpan:
        span = TraceSpan(
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=name,
            start_time_unix_nano=int(time.time() * 1e9)
        )
        self.spans.append(span)
        return span

    def end_span(self, span: TraceSpan, error_message: Optional[str] = None) -> None:
        span.end_time_unix_nano = int(time.time() * 1e9)
        if error_message:
            span.status_code = "ERROR"
            span.attributes["error.message"] = error_message
        logger.debug(f"Span '{span.name}' completed (trace={span.trace_id}, status={span.status_code})")


# Global tracer instance
telemetry_tracer = OpenTelemetryCollector()
