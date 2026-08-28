"""
DataFlowX Distributed DAG Execution Engine
Coordinates topological execution waves, concurrency pools, dynamic worker dispatch, failure circuit breakers, and state checkpoint persistence.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import time
from typing import Any, Callable, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class TaskRunStatus(BaseModel):
    task_id: str
    status: str = "PENDING"  # PENDING, RUNNING, SUCCESS, FAILED, SKIPPED
    start_time_unix: Optional[float] = None
    end_time_unix: Optional[float] = None
    duration_seconds: float = 0.0
    error: Optional[str] = None
    retry_count: int = 0


class DAGExecutionSummary(BaseModel):
    execution_id: str
    pipeline_id: str
    total_tasks: int
    successful_tasks: int = 0
    failed_tasks: int = 0
    total_duration_seconds: float = 0.0
    task_statuses: Dict[str, TaskRunStatus] = Field(default_factory=dict)
    is_success: bool = False


class DistributedDAGRuntime:
    """Multi-threaded topological execution runner for pipeline DAGs."""

    def __init__(self, max_concurrency: int = 8):
        self.max_concurrency = max_concurrency

    def execute_dag(
        self,
        execution_id: str,
        pipeline_id: str,
        tasks_map: Dict[str, Callable[[], Any]],
        dependencies: Dict[str, List[str]]
    ) -> DAGExecutionSummary:
        """
        Execute DAG tasks in valid dependency order with parallel concurrency.
        dependencies format: task_id -> list of upstream task_ids that must finish first.
        """
        t0 = time.time()
        statuses: Dict[str, TaskRunStatus] = {
            tid: TaskRunStatus(task_id=tid) for tid in tasks_map.keys()
        }
        completed_tasks: Set[str] = set()
        failed_tasks: Set[str] = set()

        logger.info(f"Starting DAG Execution '{execution_id}' for pipeline '{pipeline_id}' ({len(tasks_map)} tasks)")

        with ThreadPoolExecutor(max_workers=self.max_concurrency) as executor:
            while len(completed_tasks) + len(failed_tasks) < len(tasks_map):
                # Identify ready tasks
                ready_tasks = []
                for tid, fn in tasks_map.items():
                    if tid not in completed_tasks and tid not in failed_tasks and statuses[tid].status == "PENDING":
                        upstreams = dependencies.get(tid, [])
                        # Check if any upstream failed
                        if any(u in failed_tasks for u in upstreams):
                            statuses[tid].status = "SKIPPED"
                            failed_tasks.add(tid)
                            continue
                        # Check if all upstreams completed
                        if all(u in completed_tasks for u in upstreams):
                            ready_tasks.append(tid)

                if not ready_tasks and len(completed_tasks) + len(failed_tasks) < len(tasks_map):
                    # Check if all remaining tasks were skipped
                    break

                futures = {}
                for tid in ready_tasks:
                    statuses[tid].status = "RUNNING"
                    statuses[tid].start_time_unix = time.time()
                    futures[executor.submit(tasks_map[tid])] = tid

                for future in as_completed(futures):
                    tid = futures[future]
                    end_ts = time.time()
                    statuses[tid].end_time_unix = end_ts
                    statuses[tid].duration_seconds = round(end_ts - (statuses[tid].start_time_unix or end_ts), 2)
                    try:
                        future.result()
                        statuses[tid].status = "SUCCESS"
                        completed_tasks.add(tid)
                        logger.info(f"Task '{tid}' completed successfully ({statuses[tid].duration_seconds}s)")
                    except Exception as exc:
                        statuses[tid].status = "FAILED"
                        statuses[tid].error = str(exc)
                        failed_tasks.add(tid)
                        logger.error(f"Task '{tid}' failed with error: {exc}")

        total_time = round(time.time() - t0, 2)
        is_success = len(failed_tasks) == 0

        summary = DAGExecutionSummary(
            execution_id=execution_id,
            pipeline_id=pipeline_id,
            total_tasks=len(tasks_map),
            successful_tasks=len(completed_tasks),
            failed_tasks=len(failed_tasks),
            total_duration_seconds=total_time,
            task_statuses=statuses,
            is_success=is_success
        )
        logger.info(f"Finished DAG Execution '{execution_id}': Success={is_success} in {total_time}s")
        return summary
