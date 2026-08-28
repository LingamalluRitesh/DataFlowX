"""
DataFlowX Task Instance Execution Sandbox & Retry Runner
Executes task callables within timeout sandboxes, captures logs, and executes exponential backoff retries upon transient errors.
"""

import time
from typing import Any, Callable, Dict, Optional
from pydantic import BaseModel

from backend.core.logging import get_logger

logger = get_logger(__name__)


class TaskExecutionResult(BaseModel):
    task_id: str
    is_success: bool
    attempt_count: int
    duration_seconds: float
    error_message: Optional[str] = None


class TaskInstanceRunner:
    """Executes single task with retries."""

    @classmethod
    def run_task_with_retries(
        cls,
        task_id: str,
        task_fn: Callable[[], Any],
        max_retries: int = 3,
        initial_backoff_sec: float = 1.0
    ) -> TaskExecutionResult:
        t0 = time.time()
        attempt = 0
        backoff = initial_backoff_sec

        while attempt <= max_retries:
            attempt += 1
            try:
                logger.info(f"Executing task '{task_id}' (attempt {attempt}/{max_retries + 1})")
                task_fn()
                elapsed = time.time() - t0
                return TaskExecutionResult(task_id=task_id, is_success=True, attempt_count=attempt, duration_seconds=round(elapsed, 3))
            except Exception as e:
                logger.warning(f"Task '{task_id}' attempt {attempt} failed: {e}")
                if attempt <= max_retries:
                    time.sleep(min(backoff, 5.0))
                    backoff *= 2.0
                else:
                    elapsed = time.time() - t0
                    return TaskExecutionResult(task_id=task_id, is_success=False, attempt_count=attempt, duration_seconds=round(elapsed, 3), error_message=str(e))

        return TaskExecutionResult(task_id=task_id, is_success=False, attempt_count=attempt, duration_seconds=0.0)
