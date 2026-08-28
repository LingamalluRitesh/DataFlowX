"""
DataFlowX SQL Query State Sensor
Executes a boolean SQL query against an analytical database until it returns a truthy value (e.g. SELECT count(*) > 0).
"""

import time
from typing import Any, Callable, Dict, Optional

from orchestration_engine.sensors.base_sensor import BaseSensor, SensorResult


class SqlSensor(BaseSensor):
    """Polls a SQL database until a condition query returns non-zero / non-null records."""

    def __init__(
        self,
        query: str,
        query_executor: Callable[[str], Any],
        success_criteria: Optional[Callable[[Any], bool]] = None,
        name: Optional[str] = None,
        timeout_seconds: int = 3600,
        poke_interval_seconds: int = 60
    ):
        super().__init__(name=name or "sql_condition_sensor", timeout_seconds=timeout_seconds, poke_interval_seconds=poke_interval_seconds)
        self.query = query
        self.query_executor = query_executor
        self.success_criteria = success_criteria or (lambda res: bool(res and len(res) > 0 and (res[0] if isinstance(res, (list, tuple)) else True)))

    def poke(self) -> SensorResult:
        try:
            result = self.query_executor(self.query)
            if self.success_criteria(result):
                return SensorResult(
                    is_ready=True,
                    message=f"SQL condition met with result: {result}",
                    metadata={"query": self.query, "result": result},
                    poked_at=time.time()
                )
        except Exception as exc:
            return SensorResult(
                is_ready=False,
                message=f"SQL sensor execution failed: {exc}",
                poked_at=time.time()
            )

        return SensorResult(
            is_ready=False,
            message="SQL query returned false / zero records",
            poked_at=time.time()
        )
