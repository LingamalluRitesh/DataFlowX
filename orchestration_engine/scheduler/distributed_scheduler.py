"""
DataFlowX Distributed Enterprise Scheduler Engine
Master scheduling loop: polls cron jobs, dynamic backfills, sensor timeouts, priority queues, and coordinates worker slot dispatch.
"""

from datetime import datetime, timezone
import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger
from orchestration_engine.scheduler.cron_parser_advanced import AdvancedCronParser
from orchestration_engine.scheduler.priority_queue import PriorityTaskQueue

logger = get_logger(__name__)


class ScheduledJobDefinition(BaseModel):
    job_id: str
    pipeline_id: str
    cron_expression: str
    priority: int = 50
    is_paused: bool = False
    last_run_utc: Optional[str] = None
    next_run_utc: Optional[str] = None


class DistributedSchedulerEngine:
    """Master scheduler engine."""

    def __init__(self):
        self.jobs: Dict[str, ScheduledJobDefinition] = {}
        self.queue = PriorityTaskQueue()
        self._is_running = False

    def register_job(self, job_id: str, pipeline_id: str, cron_expr: str, priority: int = 50) -> ScheduledJobDefinition:
        next_dt = AdvancedCronParser.get_next_schedule(cron_expr)
        job = ScheduledJobDefinition(
            job_id=job_id,
            pipeline_id=pipeline_id,
            cron_expression=cron_expr,
            priority=priority,
            next_run_utc=next_dt.isoformat()
        )
        self.jobs[job_id] = job
        logger.info(f"Registered scheduled job '{job_id}' (next run: {job.next_run_utc})")
        return job

    def poll_due_jobs(self, current_time: Optional[datetime] = None) -> List[str]:
        now = current_time or datetime.now(timezone.utc)
        dispatched_jobs = []

        for job_id, job in self.jobs.items():
            if job.is_paused or not job.next_run_utc:
                continue

            next_dt = datetime.fromisoformat(job.next_run_utc)
            if now >= next_dt:
                # Dispatch job
                self.queue.enqueue(
                    task_id=f"run_{job_id}_{int(now.timestamp())}",
                    pipeline_id=job.pipeline_id,
                    base_priority=job.priority
                )
                job.last_run_utc = now.isoformat()
                job.next_run_utc = AdvancedCronParser.get_next_schedule(job.cron_expression, now).isoformat()
                dispatched_jobs.append(job_id)
                logger.info(f"Dispatched job '{job_id}' to priority queue. Next run: {job.next_run_utc}")

        return dispatched_jobs
