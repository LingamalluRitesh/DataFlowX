"""
Prometheus Streaming Pipeline & Lakehouse Metrics Exporter.
Gathers pipeline ingestion rates, checkpoint duration histograms, and backpressure telemetry.
"""

from typing import Dict, List, Any
import time


class PipelineMetricsCollector:
    """Collects real-time streaming metrics and serializes to Prometheus exposition text."""

    def __init__(self):
        self.records_ingested_total: Dict[str, int] = {}
        self.checkpoint_duration_seconds: Dict[str, List[float]] = {}
        self.backpressure_ratio: Dict[str, float] = {}

    def record_ingestion(self, pipeline_id: str, count: int) -> None:
        self.records_ingested_total[pipeline_id] = self.records_ingested_total.get(pipeline_id, 0) + count

    def record_checkpoint(self, pipeline_id: str, duration_sec: float) -> None:
        if pipeline_id not in self.checkpoint_duration_seconds:
            self.checkpoint_duration_seconds[pipeline_id] = []
        self.checkpoint_duration_seconds[pipeline_id].append(duration_sec)

    def set_backpressure_ratio(self, pipeline_id: str, ratio: float) -> None:
        self.backpressure_ratio[pipeline_id] = max(0.0, min(1.0, ratio))

    def export_prometheus(self) -> str:
        lines = [
            "# HELP dataflowx_records_ingested_total Total records processed by streaming pipeline",
            "# TYPE dataflowx_records_ingested_total counter",
        ]
        for pid, total in self.records_ingested_total.items():
            lines.append(f'dataflowx_records_ingested_total{{pipeline="{pid}"}} {total}')

        lines.extend([
            "# HELP dataflowx_backpressure_ratio Stream buffer backpressure ratio (0.0 to 1.0)",
            "# TYPE dataflowx_backpressure_ratio gauge",
        ])
        for pid, ratio in self.backpressure_ratio.items():
            lines.append(f'dataflowx_backpressure_ratio{{pipeline="{pid}"}} {ratio}')

        return "\n".join(lines) + "\n"
