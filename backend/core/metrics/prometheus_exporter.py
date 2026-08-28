"""
DataFlowX Prometheus Metrics Exposition Engine
Emits standard Prometheus text format metrics: Counters (events ingested), Gauges (active workers, queue depth), Histograms (latency seconds), and Summaries.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PrometheusMetric(BaseModel):
    name: str
    metric_type: str  # counter, gauge, histogram
    help_text: str
    value: float
    labels: Dict[str, str] = Field(default_factory=dict)


class PrometheusExporter:
    """Manages internal metric registries and renders text format."""

    def __init__(self):
        self._metrics: List[PrometheusMetric] = []

    def set_gauge(self, name: str, value: float, help_text: str, labels: Optional[Dict[str, str]] = None) -> None:
        self._metrics.append(PrometheusMetric(name=name, metric_type="gauge", help_text=help_text, value=value, labels=labels or {}))

    def inc_counter(self, name: str, value: float, help_text: str, labels: Optional[Dict[str, str]] = None) -> None:
        self._metrics.append(PrometheusMetric(name=name, metric_type="counter", help_text=help_text, value=value, labels=labels or {}))

    def render_prometheus_text(self) -> str:
        lines = []
        for m in self._metrics:
            lines.append(f"# HELP {m.name} {m.help_text}")
            lines.append(f"# TYPE {m.name} {m.metric_type}")
            label_str = ""
            if m.labels:
                pairs = [f'{k}="{v}"' for k, v in m.labels.items()]
                label_str = "{" + ",".join(pairs) + "}"
            lines.append(f"{m.name}{label_str} {m.value}")
        return "\n".join(lines) + "\n"
