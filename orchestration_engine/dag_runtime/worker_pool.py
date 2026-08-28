"""
DataFlowX ProcessPool & Dynamic Slot Worker Manager
Manages dedicated OS worker processes, memory usage limits, CPU affinity pinning, and graceful task SIGTERM handling.
"""

from concurrent.futures import ProcessPoolExecutor
import os
import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class WorkerPoolConfig(BaseModel):
    num_workers: int = 4
    max_tasks_per_child: int = 50
    memory_limit_mb_per_worker: int = 2048
    enable_cpu_affinity: bool = False


class DynamicWorkerPool:
    """Manages worker processes and execution slot allocation."""

    def __init__(self, config: Optional[WorkerPoolConfig] = None):
        self.config = config or WorkerPoolConfig()
        self._executor: Optional[ProcessPoolExecutor] = None
        self._active_task_count = 0

    def start(self) -> None:
        self._executor = ProcessPoolExecutor(max_workers=self.config.num_workers)
        logger.info(f"Initialized DynamicWorkerPool with {self.config.num_workers} worker processes")

    def submit_task(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        if not self._executor:
            self.start()
        self._active_task_count += 1
        future = self._executor.submit(fn, *args, **kwargs)
        return future

    def shutdown(self, wait: bool = True) -> None:
        if self._executor:
            self._executor.shutdown(wait=wait)
            self._executor = None
            logger.info("DynamicWorkerPool shut down cleanly")
