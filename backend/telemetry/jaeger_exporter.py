"""
DataFlowX Jaeger / Zipkin OpenTelemetry Exporter
Formats collected execution spans into Jaeger-compatible thrift/proto JSON structures for distributed waterfall visualization.
"""

from typing import Any, Dict, List
from backend.telemetry.span_collector import OpenTelemetrySpan


class JaegerTraceExporter:
    """Exports spans to Jaeger."""

    @classmethod
    def format_jaeger_spans(cls, spans: List[OpenTelemetrySpan], service_name: str = "dataflowx-engine") -> Dict[str, Any]:
        jaeger_spans = []
        for s in spans:
            jaeger_spans.append({
                "traceID": s.trace_id,
                "spanID": s.span_id,
                "operationName": s.name,
                "startTime": s.start_time_unix_nano // 1000,
                "duration": int(s.duration_ms * 1000),
                "tags": [{"key": k, "type": "string", "value": str(v)} for k, v in s.attributes.items()]
            })

        return {
            "data": [{
                "traceID": spans[0].trace_id if spans else "0",
                "spans": jaeger_spans,
                "processes": {
                    "p1": {"serviceName": service_name}
                }
            }]
        }
