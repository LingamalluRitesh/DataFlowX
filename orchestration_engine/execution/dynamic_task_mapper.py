"""
DataFlowX Dynamic Task Mapping & Parallel Fan-Out Engine
Dynamically spawns parallel task instances at runtime based on upstream list outputs (similar to Airflow 2.3+ `expand()` and Dagster DynamicOut).
"""

from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class MappedTaskInstance(BaseModel):
    mapped_index: int
    task_id: str
    input_item: Any
    status: str = "QUEUED"


class DynamicTaskMapper:
    """Expands upstream list outputs into parallel task instances."""

    @classmethod
    def expand_task(cls, base_task_id: str, upstream_items: List[Any]) -> List[MappedTaskInstance]:
        instances = []
        for idx, item in enumerate(upstream_items):
            inst = MappedTaskInstance(
                mapped_index=idx,
                task_id=f"{base_task_id}[{idx}]",
                input_item=item,
                status="QUEUED"
            )
            instances.append(inst)

        logger.info(f"Dynamically mapped task '{base_task_id}' into {len(instances)} parallel instances")
        return instances
