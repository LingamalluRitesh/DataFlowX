"""
DataFlowX Service Level Agreement (SLA) Evaluator
Evaluates execution duration, task deadlines, and freshness thresholds to identify and alert on SLA misses.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class SLAMissIncident(BaseModel):
    id: str
    pipeline_id: str
    execution_id: str
    sla_type: str  # MAX_DURATION, COMPLETION_DEADLINE, FRESHNESS
    threshold_value: float
    actual_value: float
    status: str = "OPEN"  # OPEN, ACKNOWLEDGED, RESOLVED
    triggered_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SLAEvaluator:
    """Evaluates whether pipeline runs or individual tasks breached defined SLAs."""

    @staticmethod
    def evaluate_duration(
        pipeline_id: str,
        execution_id: str,
        duration_seconds: float,
        max_duration_seconds: float
    ) -> Optional[SLAMissIncident]:
        if duration_seconds > max_duration_seconds:
            incident = SLAMissIncident(
                id=f"sla_miss_{execution_id}",
                pipeline_id=pipeline_id,
                execution_id=execution_id,
                sla_type="MAX_DURATION",
                threshold_value=max_duration_seconds,
                actual_value=duration_seconds
            )
            logger.warning(f"SLA Breach detected for pipeline '{pipeline_id}' (duration={duration_seconds}s > max={max_duration_seconds}s)")
            return incident
        return None
