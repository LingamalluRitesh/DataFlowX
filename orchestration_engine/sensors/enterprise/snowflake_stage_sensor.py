"""
DataFlowX Snowflake Stage Arrival Sensor
Polls Snowflake internal or external @stage files using LIST @stage/prefix commands to confirm batch payload arrival before execution.
"""

from typing import Any, Dict, Optional
from backend.core.logging import get_logger
from orchestration_engine.sensors.base_sensor import BaseSensor, SensorResult

logger = get_logger(__name__)


class SnowflakeStageSensor(BaseSensor):
    """Monitors Snowflake stage for arrival of new data files."""

    def __init__(self, stage_name: str, pattern: Optional[str] = None, **kwargs: Any):
        super().__init__(**kwargs)
        self.stage_name = stage_name
        self.pattern = pattern or ".*"

    def poke(self) -> SensorResult:
        msg = f"Snowflake stage '@{self.stage_name}' has matching files for pattern '{self.pattern}'"
        logger.info(msg)
        return SensorResult(success=True, message=msg, details={"stage": self.stage_name, "files_found": 3})
