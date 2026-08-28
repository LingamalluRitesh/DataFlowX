"""
DataFlowX Historical Backfill Orchestration Engine
Splits wide historical date ranges into discrete parallel execution partitions, tracks idempotent ledger states, and manages checkpointed restarts.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class BackfillPartition(BaseModel):
    partition_id: str
    start_date: str
    end_date: str
    status: str = "PENDING"  # PENDING, RUNNING, SUCCESS, FAILED
    execution_id: Optional[str] = None
    records_processed: int = 0
    error_message: Optional[str] = None


class BackfillJobSpec(BaseModel):
    id: str
    pipeline_id: str
    start_date: str
    end_date: str
    chunk_interval: str = "1d"  # 1h, 6h, 1d, 7d
    max_parallel_partitions: int = 4
    status: str = "PENDING"  # PENDING, RUNNING, COMPLETED, FAILED
    partitions: List[BackfillPartition] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class BackfillManager:
    """Orchestrates historical time-range slicing and partition execution."""

    @staticmethod
    def create_backfill_job(
        job_id: str,
        pipeline_id: str,
        start_date_str: str,
        end_date_str: str,
        chunk_interval: str = "1d",
        max_parallel: int = 4
    ) -> BackfillJobSpec:
        """Partition date interval into sequential sub-ranges."""
        start_dt = datetime.fromisoformat(start_date_str.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))

        step = timedelta(days=1)
        if chunk_interval == "1h":
            step = timedelta(hours=1)
        elif chunk_interval == "6h":
            step = timedelta(hours=6)
        elif chunk_interval == "7d":
            step = timedelta(days=7)

        partitions = []
        curr = start_dt
        p_idx = 1
        while curr < end_dt:
            next_curr = min(curr + step, end_dt)
            partitions.append(BackfillPartition(
                partition_id=f"{job_id}_p{p_idx}",
                start_date=curr.isoformat(),
                end_date=next_curr.isoformat(),
                status="PENDING"
            ))
            curr = next_curr
            p_idx += 1

        job = BackfillJobSpec(
            id=job_id,
            pipeline_id=pipeline_id,
            start_date=start_date_str,
            end_date=end_date_str,
            chunk_interval=chunk_interval,
            max_parallel_partitions=max_parallel,
            partitions=partitions
        )
        logger.info(f"Created Backfill Job '{job_id}' for pipeline '{pipeline_id}' with {len(partitions)} partitions")
        return job
