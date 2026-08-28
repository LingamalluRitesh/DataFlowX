"""
DataFlowX Base Workflow Sensor Interface
Provides asynchronous polling, timeout evaluation, exponential poke intervals, and soft fail handling.
"""

from abc import ABC, abstractmethod
import time
from typing import Any, Dict, Optional
from pydantic import BaseModel

from backend.core.logging import get_logger

logger = get_logger(__name__)


class SensorResult(BaseModel):
    is_ready: bool
    message: str
    metadata: Dict[str, Any] = {}
    poked_at: float = 0.0


class BaseSensor(ABC):
    """Abstract base class for all external state sensors."""

    def __init__(
        self,
        name: str,
        timeout_seconds: int = 3600,
        poke_interval_seconds: int = 60,
        exponential_backoff: bool = False,
        soft_fail: bool = False
    ):
        self.name = name
        self.timeout_seconds = timeout_seconds
        self.poke_interval_seconds = poke_interval_seconds
        self.exponential_backoff = exponential_backoff
        self.soft_fail = soft_fail

    @abstractmethod
    def poke(self) -> SensorResult:
        """Evaluate whether external condition is satisfied."""
        pass

    def wait(self) -> bool:
        """Poll until ready or timeout reached."""
        start_time = time.time()
        current_interval = self.poke_interval_seconds

        while time.time() - start_time < self.timeout_seconds:
            result = self.poke()
            if result.is_ready:
                logger.info(f"Sensor '{self.name}' condition satisfied: {result.message}")
                return True

            logger.debug(f"Sensor '{self.name}' not ready: {result.message}. Waiting {current_interval}s...")
            time.sleep(min(current_interval, 5))  # Sleep up to interval

            if self.exponential_backoff:
                current_interval = min(current_interval * 2, 600)

        if self.soft_fail:
            logger.warning(f"Sensor '{self.name}' timed out (Soft Fail Enabled)")
            return False
        raise TimeoutError(f"Sensor '{self.name}' timed out after {self.timeout_seconds} seconds")
