"""
DataFlowX Pipelines & DAG Builder Endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_active_workspace_id, get_async_db, get_current_user
from backend.database.models import User
from backend.schemas.common import PaginatedResponse, PaginationParams
from backend.schemas.execution import ExecutionOut, ExecutionTriggerRequest
from backend.schemas.pipeline import (
    DAGValidationResult,
    PipelineCreate,
    PipelineDAGDefinition,
    PipelineOut,
    PipelineScheduleCreate,
    PipelineScheduleOut,
    PipelineUpdate,
)
from backend.services.execution_service import ExecutionService
from backend.services.pipeline_service import PipelineService

router = APIRouter(prefix="/pipelines", tags=["Pipelines & DAGs"])


@router.get("", response_model=PaginatedResponse[PipelineOut])
async def list_pipelines(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    pipes, total = await PipelineService.list_pipelines(session, workspace_id, params)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return PaginatedResponse(
        items=[
            PipelineOut(
                id=p.id,
                organization_id=p.organization_id,
                workspace_id=p.workspace_id,
                name=p.name,
                slug=p.slug,
                description=p.description,
                pipeline_type=p.pipeline_type,
                environment=p.environment,
                tags=p.tags or [],
                concurrency_limit=p.concurrency_limit,
                timeout_seconds=p.timeout_seconds,
                retry_count=p.retry_count,
                retry_delay_seconds=p.retry_delay_seconds,
                status=p.status,
                active_version_id=p.active_version_id,
                is_active=p.is_active,
                created_at=p.created_at,
                updated_at=p.updated_at,
                schedules=[]
            )
            for p in pipes
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=(page < total_pages),
        has_prev=(page > 1)
    )


@router.post("", response_model=PipelineOut, status_code=status.HTTP_201_CREATED)
async def create_pipeline(
    payload: PipelineCreate,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    p = await PipelineService.create_pipeline(session, workspace_id, payload)
    return PipelineOut(
        id=p.id,
        organization_id=p.organization_id,
        workspace_id=p.workspace_id,
        name=p.name,
        slug=p.slug,
        description=p.description,
        pipeline_type=p.pipeline_type,
        environment=p.environment,
        tags=p.tags or [],
        concurrency_limit=p.concurrency_limit,
        timeout_seconds=p.timeout_seconds,
        retry_count=p.retry_count,
        retry_delay_seconds=p.retry_delay_seconds,
        status=p.status,
        active_version_id=p.active_version_id,
        is_active=p.is_active,
        created_at=p.created_at,
        updated_at=p.updated_at,
        schedules=[]
    )


@router.get("/{pipeline_id}", response_model=PipelineOut)
async def get_pipeline(
    pipeline_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    p = await PipelineService.get_pipeline(session, pipeline_id)
    return PipelineOut(
        id=p.id,
        organization_id=p.organization_id,
        workspace_id=p.workspace_id,
        name=p.name,
        slug=p.slug,
        description=p.description,
        pipeline_type=p.pipeline_type,
        environment=p.environment,
        tags=p.tags or [],
        concurrency_limit=p.concurrency_limit,
        timeout_seconds=p.timeout_seconds,
        retry_count=p.retry_count,
        retry_delay_seconds=p.retry_delay_seconds,
        status=p.status,
        active_version_id=p.active_version_id,
        is_active=p.is_active,
        created_at=p.created_at,
        updated_at=p.updated_at,
        schedules=[]
    )


@router.post("/validate-dag", response_model=DAGValidationResult)
async def validate_dag(
    dag: PipelineDAGDefinition,
    _: User = Depends(get_current_user)
):
    """Validate a DAG structure (cycles, disconnected nodes, topological order)."""
    return PipelineService.validate_dag_definition(dag)


@router.post("/{pipeline_id}/schedules", response_model=PipelineScheduleOut, status_code=status.HTTP_201_CREATED)
async def add_pipeline_schedule(
    pipeline_id: str,
    payload: PipelineScheduleCreate,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    sched = await PipelineService.add_schedule(session, pipeline_id, payload)
    return PipelineScheduleOut(
        id=sched.id,
        pipeline_id=sched.pipeline_id,
        cron_expression=sched.cron_expression,
        interval_seconds=sched.interval_seconds,
        timezone=sched.timezone,
        is_enabled=sched.is_enabled,
        last_run_at=sched.last_run_at,
        next_run_at=sched.next_run_at,
        created_at=sched.created_at
    )


@router.post("/{pipeline_id}/trigger", response_model=ExecutionOut)
async def trigger_pipeline(
    pipeline_id: str,
    payload: ExecutionTriggerRequest = ExecutionTriggerRequest(),
    session: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Trigger immediate execution of a pipeline."""
    execution = await ExecutionService.trigger_execution(session, pipeline_id, current_user.id, payload)
    return ExecutionOut(
        id=execution.id,
        organization_id=execution.organization_id,
        workspace_id=execution.workspace_id,
        pipeline_id=execution.pipeline_id,
        pipeline_version_id=execution.pipeline_version_id,
        execution_type=execution.execution_type,
        trigger_source=execution.trigger_source,
        status=execution.status,
        start_time=execution.start_time,
        end_time=execution.end_time,
        duration_seconds=execution.duration_seconds,
        total_records_processed=execution.total_records_processed,
        total_bytes_processed=execution.total_bytes_processed,
        records_failed=execution.records_failed,
        quality_score=execution.quality_score,
        error_summary=execution.error_summary,
        parameters=execution.parameters_json or {},
        created_at=execution.created_at,
        tasks=[]
    )
