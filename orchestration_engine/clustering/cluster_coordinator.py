"""
DataFlowX Worker Cluster Coordinator & Dynamic Rebalancer
Manages active worker discovery, queue capacity thresholds, heartbeat liveness, and graceful failover.
"""

from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class WorkerNodeStatus(BaseModel):
    worker_id: str
    hostname: str
    ip_address: str
    active_tasks: int = 0
    max_concurrency: int = 8
    cpu_percent: float = 0.0
    memory_used_mb: float = 0.0
    last_heartbeat_unix: float = Field(default_factory=time.time)
    is_alive: bool = True


class ClusterCoordinator:
    """Coordinates distributed worker node telemetry and task dispatch weighting."""

    def __init__(self, heartbeat_timeout_seconds: int = 45):
        self.heartbeat_timeout = heartbeat_timeout_seconds
        self._workers: Dict[str, WorkerNodeStatus] = {}

    def record_heartbeat(self, status: WorkerNodeStatus) -> None:
        status.last_heartbeat_unix = time.time()
        status.is_alive = True
        self._workers[status.worker_id] = status

    def get_healthy_workers(self) -> List[WorkerNodeStatus]:
        now = time.time()
        healthy = []
        for wid, w in self._workers.items():
            if now - w.last_heartbeat_unix <= self.heartbeat_timeout:
                w.is_alive = True
                healthy.append(w)
            else:
                w.is_alive = False
        return healthy

    def select_least_loaded_worker(self) -> Optional[WorkerNodeStatus]:
        """Select worker with maximum available execution slots."""
        healthy = self.get_healthy_workers()
        if not healthy:
            return None
        # Sort by available capacity descending
        return sorted(healthy, key=lambda w: (w.max_concurrency - w.active_tasks), reverse=True)[0]
