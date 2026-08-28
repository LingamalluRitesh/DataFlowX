"""
DataFlowX Parallel Thread & Process Execution Pool Dispatcher
Manages concurrent worker slots, assigns priority tasks to free thread workers, and coordinates DAG wave completions.
"""

from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional
from backend.core.logging import get_logger

logger = get_logger(__name__)


class ExecutionPoolDispatcher:
    """Worker slot pool."""

    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers
        self._executor = ThreadPoolExecutor(max_workers=max_workers)

    def submit_task(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Future:
        return self._executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True) -> None:
        self._executor.shutdown(wait=wait)
