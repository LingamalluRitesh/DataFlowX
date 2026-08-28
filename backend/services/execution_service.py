"""
DataFlowX Pipeline Execution & Telemetry Service
"""

from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.exceptions import NotFoundError
from backend.core.logging import get_logger
from backend.database.models import Execution, Pipeline, PipelineVersion, TaskExecution, TaskLog
from backend.schemas.common import PaginationParams
from backend.schemas.execution import ExecutionTriggerRequest
from orchestration_engine.dag import DAGDefinition
from orchestration_engine.executor.dag_executor import DAGExecutor

logger = get_logger(__name__)


class ExecutionService:
    """Manages execution runs, task telemetry, and historical logs."""

    @staticmethod
    async def list_executions(session: AsyncSession, workspace_id: Optional[str], params: PaginationParams) -> Tuple[List[Execution], int]:
        query = select(Execution)
        if workspace_id:
            query = query.where(Execution.workspace_id == workspace_id)
        if params.search:
            s = f"%{params.search}%"
            query = query.where((Execution.status.ilike(s)) | (Execution.trigger_source.ilike(s)))

        total_stmt = select(func.count()).select_from(query.subquery())
        total = (await session.execute(total_stmt)).scalar() or 0

        query = query.order_by(Execution.created_at.desc()).offset((params.page - 1) * params.page_size).limit(params.page_size)
        items = (await session.execute(query)).scalars().all()
        return list(items), total

    @staticmethod
    async def get_execution(session: AsyncSession, execution_id: str) -> Execution:
        exec_obj = (await session.execute(select(Execution).where(Execution.id == execution_id))).scalar_one_or_none()
        if not exec_obj:
            raise NotFoundError("Execution", execution_id)
        return exec_obj

    @staticmethod
    async def trigger_execution(
        session: AsyncSession,
        pipeline_id: str,
        user_id: Optional[str],
        payload: ExecutionTriggerRequest
    ) -> Execution:
        pipe = (await session.execute(select(Pipeline).where(Pipeline.id == pipeline_id))).scalar_one_or_none()
        if not pipe:
            raise NotFoundError("Pipeline", pipeline_id)

        version_id = payload.version_id or pipe.active_version_id
        if not version_id:
            raise NotFoundError("PipelineVersion", "No active version assigned to pipeline")

        p_ver = (await session.execute(select(PipelineVersion).where(PipelineVersion.id == version_id))).scalar_one_or_none()
        if not p_ver:
            raise NotFoundError("PipelineVersion", version_id)

        # Create execution record
        now = datetime.now(timezone.utc)
        execution = Execution(
            workspace_id=pipe.workspace_id,
            pipeline_id=pipe.id,
            pipeline_version_id=p_ver.id,
            execution_type="manual",
            trigger_source="web_ui" if user_id else "api",
            status="RUNNING",
            start_time=now,
            triggered_by_user_id=user_id,
            parameters_json=payload.parameters
        )
        session.add(execution)
        await session.commit()
        await session.refresh(execution)

        # Execute DAG synchronously or async task
        dag_def = DAGDefinition(**p_ver.dag_definition_json)
        executor = DAGExecutor(
            dag_definition=dag_def,
            pipeline_id=pipe.id,
            execution_id=execution.id,
            max_workers=pipe.concurrency_limit
        )

        exec_summary = executor.run(runtime_parameters=payload.parameters)

        # Update execution state & persist tasks and logs
        execution.status = exec_summary.status
        execution.end_time = exec_summary.end_time
        execution.duration_seconds = exec_summary.duration_seconds
        execution.total_records_processed = exec_summary.total_records_processed
        execution.total_bytes_processed = exec_summary.total_bytes_processed
        execution.records_failed = exec_summary.records_failed
        execution.quality_score = exec_summary.quality_score
        execution.error_summary = exec_summary.error_summary

        for nid, tres in exec_summary.task_results.items():
            task_exec = TaskExecution(
                execution_id=execution.id,
                node_id=nid,
                task_type="TRANSFORM",
                name=tres.name,
                status=tres.status,
                start_time=tres.start_time,
                end_time=tres.end_time,
                duration_seconds=tres.duration_seconds,
                records_in=tres.records_in,
                records_out=tres.records_out,
                bytes_processed=tres.bytes_processed,
                error_message=tres.error_message,
                error_traceback=tres.error_traceback
            )
            session.add(task_exec)
            await session.flush()

            # Add task logs
            for log_entry in tres.logs:
                t_log = TaskLog(
                    execution_id=execution.id,
                    task_execution_id=task_exec.id,
                    log_level=log_entry.get("level", "INFO"),
                    message=log_entry.get("message", ""),
                    metadata_json=log_entry.get("metadata", {}),
                    logged_at=datetime.fromisoformat(log_entry["timestamp"]) if "timestamp" in log_entry else now
                )
                session.add(t_log)

        await session.commit()
        await session.refresh(execution)
        return execution
