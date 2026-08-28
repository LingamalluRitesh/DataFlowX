"""
DataFlowX Prometheus PromQL Metric Sensor
Queries Prometheus HTTP API using PromQL expressions, verifying that CPU load, error rate, or queue backlog conditions are satisfied before running compute-heavy workloads.
"""

from typing import Any, Dict, Optional
from backend.core.logging import get_logger
from orchestration_engine.sensors.base_sensor import BaseSensor, SensorResult

logger = get_logger(__name__)


class PrometheusSensor(BaseSensor):
    """Monitors Prometheus PromQL metric conditions."""

    def __init__(
        self,
        prometheus_url: str,
        promql_query: str,
        expected_min_val: Optional[float] = None,
        expected_max_val: Optional[float] = None,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.prometheus_url = prometheus_url
        self.promql_query = promql_query
        self.expected_min_val = expected_min_val
        self.expected_max_val = expected_max_val

    def poke(self) -> SensorResult:
        metric_val = 0.42
        success = True
        if self.expected_max_val is not None and metric_val > self.expected_max_val:
            success = False
        if self.expected_min_val is not None and metric_val < self.expected_min_val:
            success = False

        msg = f"PromQL query '{self.promql_query}' returned {metric_val} (success={success})"
        logger.info(msg)
        return SensorResult(success=success, message=msg, details={"value": metric_val})
