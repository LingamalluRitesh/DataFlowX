"""
DataFlowX DAG Dependency Failure Tracer
Traverses DAG dependency graphs in reverse from failed leaf tasks to isolate the earliest upstream root failure node.
"""

from typing import Dict, List, Optional, Set
from pydantic import BaseModel


class RootCauseNode(BaseModel):
    task_id: str
    failure_type: str
    is_root_cause: bool
    downstream_impacted_count: int


class DAGDependencyTracer:
    """Isolates root failure nodes in complex DAGs."""

    @classmethod
    def trace_root_cause(cls, dependencies: Dict[str, List[str]], task_statuses: Dict[str, str]) -> Optional[RootCauseNode]:
        failed_tasks = [t for t, s in task_statuses.items() if s == "FAILED"]
        if not failed_tasks:
            return None

        # Find failed task with no failed upstreams
        for task in failed_tasks:
            upstreams = dependencies.get(task, [])
            failed_upstreams = [u for u in upstreams if task_statuses.get(u) == "FAILED"]
            if not failed_upstreams:
                downstream_cnt = sum(1 for deps in dependencies.values() if task in deps)
                return RootCauseNode(
                    task_id=task,
                    failure_type="PRIMARY_TASK_FAILURE",
                    is_root_cause=True,
                    downstream_impacted_count=downstream_cnt
                )

        return RootCauseNode(task_id=failed_tasks[0], failure_type="PRIMARY_TASK_FAILURE", is_root_cause=True, downstream_impacted_count=0)
