"""
DataFlowX Fluent Pipeline DAG Builder API
Enables clean, idiomatic Python pipeline authoring with context managers (`with Pipeline('name') as p:`) and bitshift dependency chaining (`t1 >> [t2, t3] >> t4`).
"""

from typing import Any, Callable, Dict, List, Optional, Set, Union
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class TaskNode:
    """Represents a single task in a pipeline DAG."""

    def __init__(
        self,
        task_id: str,
        operator_type: str,
        parameters: Optional[Dict[str, Any]] = None,
        retries: int = 3,
        retry_delay_seconds: int = 30,
        sla_seconds: Optional[int] = None
    ):
        self.task_id = task_id
        self.operator_type = operator_type
        self.parameters = parameters or {}
        self.retries = retries
        self.retry_delay_seconds = retry_delay_seconds
        self.sla_seconds = sla_seconds
        self.upstreams: Set["TaskNode"] = set()
        self.downstreams: Set["TaskNode"] = set()

    def __rshift__(self, other: Union["TaskNode", List["TaskNode"]]) -> Union["TaskNode", List["TaskNode"]]:
        """Operator >> defines downstream dependencies (self >> other)."""
        if isinstance(other, list):
            for t in other:
                self.downstreams.add(t)
                t.upstreams.add(self)
        else:
            self.downstreams.add(other)
            other.upstreams.add(self)
        return other

    def __lshift__(self, other: Union["TaskNode", List["TaskNode"]]) -> Union["TaskNode", List["TaskNode"]]:
        """Operator << defines upstream dependencies (self << other)."""
        if isinstance(other, list):
            for t in other:
                t.downstreams.add(self)
                self.upstreams.add(t)
        else:
            other.downstreams.add(self)
            self.upstreams.add(other)
        return other


class Pipeline:
    """Context manager and container for a complete DAG definition."""

    _CURRENT_PIPELINE: Optional["Pipeline"] = None

    def __init__(
        self,
        pipeline_id: str,
        schedule_cron: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        max_active_runs: int = 1
    ):
        self.pipeline_id = pipeline_id
        self.schedule_cron = schedule_cron
        self.description = description
        self.tags = tags or []
        self.max_active_runs = max_active_runs
        self.tasks: Dict[str, TaskNode] = {}

    def __enter__(self) -> "Pipeline":
        Pipeline._CURRENT_PIPELINE = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        Pipeline._CURRENT_PIPELINE = None

    def add_task(self, task: TaskNode) -> TaskNode:
        if task.task_id in self.tasks:
            raise ValueError(f"Duplicate task ID '{task.task_id}' in pipeline '{self.pipeline_id}'")
        self.tasks[task.task_id] = task
        return task

    def get_dependencies_map(self) -> Dict[str, List[str]]:
        return {
            task_id: [u.task_id for u in task.upstreams]
            for task_id, task in self.tasks.items()
        }
