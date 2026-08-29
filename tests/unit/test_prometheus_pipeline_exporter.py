import pytest
from data_engine.observability.prometheus_pipeline_exporter import PipelineMetricsCollector


def test_pipeline_metrics_exporter():
    collector = PipelineMetricsCollector()
    collector.record_ingestion("orders_stream", 5000)
    collector.record_ingestion("orders_stream", 3500)
    collector.record_checkpoint("orders_stream", 0.42)
    collector.set_backpressure_ratio("orders_stream", 0.15)

    assert collector.records_ingested_total["orders_stream"] == 8500
    assert collector.backpressure_ratio["orders_stream"] == 0.15

    prom = collector.export_prometheus()
    assert 'dataflowx_records_ingested_total{pipeline="orders_stream"} 8500' in prom
    assert 'dataflowx_backpressure_ratio{pipeline="orders_stream"} 0.15' in prom
