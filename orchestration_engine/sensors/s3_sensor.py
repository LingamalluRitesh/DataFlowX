"""
DataFlowX Amazon S3 & MinIO Object Key Sensor
Pokes S3 buckets for the appearance of specific prefixes, objects, or file manifests.
"""

import time
from typing import Any, Dict, Optional

from orchestration_engine.sensors.base_sensor import BaseSensor, SensorResult
from storage import storage_engine


class S3KeySensor(BaseSensor):
    """Monitors S3 / MinIO object storage for key or prefix presence."""

    def __init__(
        self,
        bucket_name: str,
        object_key_prefix: str,
        name: Optional[str] = None,
        timeout_seconds: int = 3600,
        poke_interval_seconds: int = 60
    ):
        super().__init__(name=name or f"s3_sensor_{bucket_name}_{object_key_prefix}", timeout_seconds=timeout_seconds, poke_interval_seconds=poke_interval_seconds)
        self.bucket_name = bucket_name
        self.object_key_prefix = object_key_prefix

    def poke(self) -> SensorResult:
        try:
            if storage_engine.exists(self.object_key_prefix):
                return SensorResult(
                    is_ready=True,
                    message=f"Found target object in S3: {self.object_key_prefix}",
                    metadata={"bucket": self.bucket_name, "key": self.object_key_prefix},
                    poked_at=time.time()
                )
        except Exception:
            pass

        return SensorResult(
            is_ready=False,
            message=f"Object '{self.object_key_prefix}' not found in bucket '{self.bucket_name}'",
            poked_at=time.time()
        )
