"""
DataFlowX Distributed Scheduler Daemon
Polls pipeline schedules, evaluates triggers, acquires distributed locks, and dispatches pipeline executions.
"""

from datetime import datetime, timezone
import os
import signal
import sys
import time
from typing import List, Optional
from sqlalchemy import select
from backend.core.database import sync_session_factory
from backend.core.logging import get_logger, setup_logging
from backend.database.models import Pipeline, PipelineSchedule, PipelineVersion
from orchestration_engine.dag.models import DAGDefinition
from orchestration_engine.executor.dag_executor import DAGExecutor
from orchestration_engine.scheduler.cron_evaluator import ScheduleEvaluator
from orchestration_engine.scheduler.distributed_lock import DistributedLockManager

logger = get_logger(__name__)


class SchedulerDaemon:
    """Master scheduler process for DataFlowX."""

    def __init__(self, poll_interval_seconds: int = 10):
        self.poll_interval = poll_interval_seconds
        self.lock_manager = DistributedLockManager()
        self.running = True

    def start(self) -> None:
        logger.info("DataFlowX Scheduler Daemon starting up...")
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

        while self.running:
            try:
                self.check_and_trigger_due_schedules()
            except Exception as exc:
                logger.error(f"Scheduler tick error: {exc}")

            time.sleep(self.poll_interval)

        logger.info("DataFlowX Scheduler Daemon stopped gracefully.")

    def _handle_signal(self, signum, frame):
        logger.info(f"Received shutdown signal {signum}. Stopping scheduler daemon...")
        self.running = False

    def check_and_trigger_due_schedules(self) -> None:
        """Poll database for enabled schedules that have reached next_run_at."""
        now = datetime.now(timezone.utc)
        session = sync_session_factory()

        try:
            # Query enabled schedules
            stmt = select(PipelineSchedule).where(PipelineSchedule.is_enabled == True)
            schedules: List[PipelineSchedule] = session.scalars(stmt).all()

            for sched in schedules:
                if not ScheduleEvaluator.is_due(sched.next_run_at, now):
                    continue

                lock_key = f"pipeline_sched_{sched.pipeline_id}"
                token = self.lock_manager.acquire_lock(lock_key, timeout_seconds=120)
                if not token:
                    logger.debug(f"Schedule for pipeline '{sched.pipeline_id}' locked by another worker.")
                    continue

                try:
                    self._trigger_pipeline_execution(session, sched, now)
                finally:
                    self.lock_manager.release_lock(lock_key, token)

        finally:
            session.close()

    def _trigger_pipeline_execution(self, session, schedule: PipelineSchedule, trigger_time: datetime) -> None:
        pipeline = session.get(Pipeline, schedule.pipeline_id)
        if not pipeline or not pipeline.is_active or pipeline.status != "active":
            return

        logger.info(f"Triggering scheduled execution for pipeline '{pipeline.name}' (ID: {pipeline.id})")

        # Update schedule next run
        next_run = ScheduleEvaluator.get_next_run(
            cron_expression=schedule.cron_expression,
            interval_seconds=schedule.interval_seconds,
            base_time=trigger_time
        )
        schedule.last_run_at = trigger_time
        schedule.next_run_at = next_run
        session.commit()

        # Load active pipeline version DAG
        if pipeline.active_version_id:
            p_ver = session.get(PipelineVersion, pipeline.active_version_id)
            if p_ver:
                dag_def = DAGDefinition(**p_ver.dag_definition_json)
                execution_id = f"exec_sched_{int(time.time())}"
                executor = DAGExecutor(dag_def, pipeline.id, execution_id)
                # Run execution
                executor.run()


if __name__ == "__main__":
    setup_logging()
    daemon = SchedulerDaemon()
    daemon.start()
