"""
DataFlowX SLA Monitor Daemon
Periodically scans running tasks and active workflows to detect impending SLA deadline breaches.
"""

from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional

from backend.core.logging import get_logger
from orchestration_engine.sla.sla_evaluator import SLAEvaluator, SLAMissIncident

logger = get_logger(__name__)


class SLAMonitor:
    """Monitors live execution states against SLAs."""

    def __init__(self):
        self.incidents: List[SLAMissIncident] = []

    def check_running_task(
        self,
        pipeline_id: str,
        execution_id: str,
        start_time_unix: float,
        sla_seconds: float
    ) -> Optional[SLAMissIncident]:
        elapsed = time.time() - start_time_unix
        incident = SLAEvaluator.evaluate_duration(pipeline_id, execution_id, elapsed, sla_seconds)
        if incident:
            self.incidents.append(incident)
        return incident
