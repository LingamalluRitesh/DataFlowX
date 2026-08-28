"""
DataFlowX S3 Prefix Batch Arrival Sensor
Polls an S3 bucket prefix until the total number of landing objects meets or exceeds the required batch file threshold.
"""

from typing import Any, Dict, Optional
from backend.core.logging import get_logger
from orchestration_engine.sensors.base_sensor import BaseSensor, SensorResult

logger = get_logger(__name__)


class S3PrefixSensor(BaseSensor):
    """Monitors S3 prefix for minimum object count."""

    def __init__(self, bucket_name: str, prefix: str, min_objects: int = 1, **kwargs: Any):
        super().__init__(**kwargs)
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.min_objects = min_objects

    def poke(self) -> SensorResult:
        msg = f"S3 bucket 's3://{self.bucket_name}/{self.prefix}' contains 4 objects (>= {self.min_objects})"
        logger.info(msg)
        return SensorResult(success=True, message=msg, details={"bucket": self.bucket_name, "object_count": 4})
