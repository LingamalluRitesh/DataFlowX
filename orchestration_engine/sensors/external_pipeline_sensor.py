"""
DataFlowX Cross-Pipeline Dependency Sensor
Waits for an upstream DAG pipeline execution to reach SUCCESS state before triggering downstream dependent workflows.
"""

import time
from typing import Any, Callable, Dict, Optional

from orchestration_engine.sensors.base_sensor import BaseSensor, SensorResult


class ExternalPipelineSensor(BaseSensor):
    """Monitors another pipeline's execution status."""

    def __init__(
        self,
        external_pipeline_id: str,
        status_checker: Callable[[str], Optional[str]],
        target_status: str = "SUCCESS",
        name: Optional[str] = None,
        timeout_seconds: int = 3600,
        poke_interval_seconds: int = 30
    ):
        super().__init__(name=name or f"external_pipe_sensor_{external_pipeline_id}", timeout_seconds=timeout_seconds, poke_interval_seconds=poke_interval_seconds)
        self.external_pipeline_id = external_pipeline_id
        self.status_checker = status_checker
        self.target_status = target_status

    def poke(self) -> SensorResult:
        try:
            curr_status = self.status_checker(self.external_pipeline_id)
            if curr_status == self.target_status:
                return SensorResult(
                    is_ready=True,
                    message=f"External pipeline '{self.external_pipeline_id}' achieved target status '{self.target_status}'",
                    metadata={"pipeline_id": self.external_pipeline_id, "status": curr_status},
                    poked_at=time.time()
                )
            elif curr_status in ("FAILED", "CANCELLED"):
                return SensorResult(
                    is_ready=False,
                    message=f"External pipeline '{self.external_pipeline_id}' in terminal failure state '{curr_status}'",
                    metadata={"pipeline_id": self.external_pipeline_id, "status": curr_status},
                    poked_at=time.time()
                )
        except Exception as exc:
            return SensorResult(is_ready=False, message=f"Status check error: {exc}", poked_at=time.time())

        return SensorResult(
            is_ready=False,
            message=f"External pipeline '{self.external_pipeline_id}' status is pending",
            poked_at=time.time()
        )
