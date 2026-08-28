"""
DataFlowX Executions & Task Logs Endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_active_workspace_id, get_async_db, get_current_user
from backend.database.models import Execution, TaskExecution, TaskLog, User
from backend.schemas.common import PaginatedResponse, PaginationParams
from backend.schemas.execution import ExecutionOut, TaskExecutionOut, TaskLogOut
from backend.services.execution_service import ExecutionService

router = APIRouter(prefix="/executions", tags=["Executions & Monitoring"])


@router.get("", response_model=PaginatedResponse[ExecutionOut])
async def list_executions(
    page: int = 1,
    page_size: int = 20,
    search: Optional[str] = None,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    params = PaginationParams(page=page, page_size=page_size, search=search)
    execs, total = await ExecutionService.list_executions(session, workspace_id, params)
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return PaginatedResponse(
        items=[
            ExecutionOut(
                id=e.id,
                organization_id=e.organization_id,
                workspace_id=e.workspace_id,
                pipeline_id=e.pipeline_id,
                pipeline_version_id=e.pipeline_version_id,
                execution_type=e.execution_type,
                trigger_source=e.trigger_source,
                status=e.status,
                start_time=e.start_time,
                end_time=e.end_time,
                duration_seconds=e.duration_seconds,
                total_records_processed=e.total_records_processed,
                total_bytes_processed=e.total_bytes_processed,
                records_failed=e.records_failed,
                quality_score=e.quality_score,
                error_summary=e.error_summary,
                parameters=e.parameters_json or {},
                created_at=e.created_at,
                tasks=[]
            )
            for e in execs
        ],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=(page < total_pages),
        has_prev=(page > 1)
    )


@router.get("/{execution_id}", response_model=ExecutionOut)
async def get_execution(
    execution_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    e = await ExecutionService.get_execution(session, execution_id)
    # Fetch task executions
    tasks = (await session.execute(select(TaskExecution).where(TaskExecution.execution_id == execution_id).order_by(TaskExecution.created_at))).scalars().all()

    return ExecutionOut(
        id=e.id,
        organization_id=e.organization_id,
        workspace_id=e.workspace_id,
        pipeline_id=e.pipeline_id,
        pipeline_version_id=e.pipeline_version_id,
        execution_type=e.execution_type,
        trigger_source=e.trigger_source,
        status=e.status,
        start_time=e.start_time,
        end_time=e.end_time,
        duration_seconds=e.duration_seconds,
        total_records_processed=e.total_records_processed,
        total_bytes_processed=e.total_bytes_processed,
        records_failed=e.records_failed,
        quality_score=e.quality_score,
        error_summary=e.error_summary,
        parameters=e.parameters_json or {},
        created_at=e.created_at,
        tasks=[
            TaskExecutionOut(
                id=t.id,
                execution_id=t.execution_id,
                node_id=t.node_id,
                task_type=t.task_type,
                name=t.name,
                status=t.status,
                worker_id=t.worker_id,
                start_time=t.start_time,
                end_time=t.end_time,
                duration_seconds=t.duration_seconds,
                attempt_number=t.attempt_number,
                max_retries=t.max_retries,
                records_in=t.records_in,
                records_out=t.records_out,
                bytes_processed=t.bytes_processed,
                error_message=t.error_message,
                created_at=t.created_at
            )
            for t in tasks
        ]
    )


@router.get("/{execution_id}/logs", response_model=List[TaskLogOut])
async def get_execution_logs(
    execution_id: str,
    session: AsyncSession = Depends(get_async_db),
    _: User = Depends(get_current_user)
):
    stmt = select(TaskLog).where(TaskLog.execution_id == execution_id).order_by(TaskLog.logged_at.asc())
    logs = (await session.execute(stmt)).scalars().all()
    return [
        TaskLogOut(
            id=l.id,
            task_execution_id=l.task_execution_id,
            log_level=l.log_level,
            message=l.message,
            metadata_json=l.metadata_json or {},
            logged_at=l.logged_at
        )
        for l in logs
    ]
