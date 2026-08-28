"""
DataFlowX Webhook & External Callback Sensor
Awaits an incoming HTTP webhook callback or external trigger token before unlocking downstream tasks.
"""

import time
from typing import Any, Dict, Optional

from orchestration_engine.sensors.base_sensor import BaseSensor, SensorResult


class WebhookSensor(BaseSensor):
    """Awaits external system callback token."""

    _received_webhooks: Dict[str, Dict[str, Any]] = {}

    def __init__(
        self,
        token: str,
        name: Optional[str] = None,
        timeout_seconds: int = 7200,
        poke_interval_seconds: int = 10
    ):
        super().__init__(name=name or f"webhook_sensor_{token}", timeout_seconds=timeout_seconds, poke_interval_seconds=poke_interval_seconds)
        self.token = token

    @classmethod
    def register_callback(cls, token: str, payload: Dict[str, Any]) -> None:
        cls._received_webhooks[token] = payload

    def poke(self) -> SensorResult:
        if self.token in self._received_webhooks:
            payload = self._received_webhooks.pop(self.token)
            return SensorResult(
                is_ready=True,
                message=f"Received webhook callback for token '{self.token}'",
                metadata={"token": self.token, "payload": payload},
                poked_at=time.time()
            )

        return SensorResult(
            is_ready=False,
            message=f"Waiting for webhook callback on token '{self.token}'",
            poked_at=time.time()
        )
