"""
DataFlowX Historical Backfill Service
"""

import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.exceptions import NotFoundError
from backend.core.logging import get_logger
from backend.database.models.orchestration_extra import BackfillJobModel
from backend.schemas.orchestration_extra import BackfillCreate
from orchestration_engine.backfill.backfill_manager import BackfillManager

logger = get_logger(__name__)


class BackfillService:
    """Service for managing historical backfill jobs."""

    @staticmethod
    async def create_backfill(db: AsyncSession, workspace_id: str, data: BackfillCreate) -> BackfillJobModel:
        job_id = str(uuid.uuid4())
        job_spec = BackfillManager.create_backfill_job(
            job_id=job_id,
            pipeline_id=data.pipeline_id,
            start_date_str=data.start_date,
            end_date_str=data.end_date,
            chunk_interval=data.chunk_interval,
            max_parallel=data.max_parallel_partitions
        )

        job_model = BackfillJobModel(
            id=job_id,
            workspace_id=workspace_id,
            pipeline_id=data.pipeline_id,
            start_date=data.start_date,
            end_date=data.end_date,
            chunk_interval=data.chunk_interval,
            max_parallel_partitions=data.max_parallel_partitions,
            status="PENDING",
            partitions_data=[p.dict() for p in job_spec.partitions]
        )
        db.add(job_model)
        await db.commit()
        await db.refresh(job_model)
        logger.info(f"Created Backfill Job '{job_id}' for pipeline '{data.pipeline_id}'")
        return job_model

    @staticmethod
    async def list_backfills(db: AsyncSession, workspace_id: str) -> List[BackfillJobModel]:
        stmt = select(BackfillJobModel).where(BackfillJobModel.workspace_id == workspace_id).order_by(BackfillJobModel.created_at.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def get_backfill_by_id(db: AsyncSession, backfill_id: str, workspace_id: str) -> BackfillJobModel:
        stmt = select(BackfillJobModel).where(
            BackfillJobModel.id == backfill_id,
            BackfillJobModel.workspace_id == workspace_id
        )
        result = await db.execute(stmt)
        job = result.scalar_one_or_none()
        if not job:
            raise NotFoundError("BackfillJob", backfill_id)
        return job
