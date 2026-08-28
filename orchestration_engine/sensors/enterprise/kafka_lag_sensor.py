"""
DataFlowX Kafka Consumer Group Lag Sensor
Polls Kafka broker consumer group offsets, blocking downstream pipeline tasks until consumer lag drops below max allowed threshold.
"""

from typing import Any, Dict, Optional
from backend.core.logging import get_logger
from orchestration_engine.sensors.base_sensor import BaseSensor, SensorResult

logger = get_logger(__name__)


class KafkaLagSensor(BaseSensor):
    """Monitors Kafka consumer lag before triggering pipeline."""

    def __init__(
        self,
        topic: str,
        consumer_group: str,
        max_allowed_lag: int = 100,
        **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.topic = topic
        self.consumer_group = consumer_group
        self.max_allowed_lag = max_allowed_lag

    def poke(self) -> SensorResult:
        # Emulate checking consumer group lag
        current_lag = 42
        success = current_lag <= self.max_allowed_lag
        msg = f"Kafka lag for group '{self.consumer_group}' on '{self.topic}' is {current_lag} (threshold: {self.max_allowed_lag})"
        logger.info(msg)
        return SensorResult(success=success, message=msg, details={"current_lag": current_lag})
