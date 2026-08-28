"""
DataFlowX Pipeline, DAG & Scheduling Service
"""

import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.exceptions import DAGValidationError, NotFoundError
from backend.database.models import Pipeline, PipelineEdge, PipelineNode, PipelineSchedule, PipelineVersion
from backend.schemas.common import PaginationParams
from backend.schemas.pipeline import (
    DAGValidationResult,
    PipelineCreate,
    PipelineDAGDefinition,
    PipelineScheduleCreate,
    PipelineUpdate,
)
from orchestration_engine.dag import DAGDefinition, DAGParser


class PipelineService:
    """Pipeline definition, versioning, DAG validation, and execution triggering."""

    @staticmethod
    async def list_pipelines(session: AsyncSession, workspace_id: Optional[str], params: PaginationParams) -> Tuple[List[Pipeline], int]:
        query = select(Pipeline).where(Pipeline.is_deleted == False)
        if workspace_id:
            query = query.where(Pipeline.workspace_id == workspace_id)
        if params.search:
            s = f"%{params.search}%"
            query = query.where((Pipeline.name.ilike(s)) | (Pipeline.environment.ilike(s)))

        total_stmt = select(func.count()).select_from(query.subquery())
        total = (await session.execute(total_stmt)).scalar() or 0

        query = query.order_by(Pipeline.created_at.desc()).offset((params.page - 1) * params.page_size).limit(params.page_size)
        items = (await session.execute(query)).scalars().all()
        return list(items), total

    @staticmethod
    async def get_pipeline(session: AsyncSession, pipeline_id: str) -> Pipeline:
        pipe = (await session.execute(select(Pipeline).where(Pipeline.id == pipeline_id, Pipeline.is_deleted == False))).scalar_one_or_none()
        if not pipe:
            raise NotFoundError("Pipeline", pipeline_id)
        return pipe

    @staticmethod
    def validate_dag_definition(dag: PipelineDAGDefinition) -> DAGValidationResult:
        dag_obj = DAGDefinition(
            nodes=[{"id": n.id, "type": n.type, "name": n.name, "config": n.config, "position": n.position} for n in dag.nodes],
            edges=[{"source": e.source, "target": e.target, "condition": e.condition} for e in dag.edges],
            globals=dag.globals
        )
        parser = DAGParser(dag_obj)
        is_valid, errors, warnings = parser.validate_dag()
        top_order = parser.get_topological_sort() if is_valid else []
        is_cyclic, cycle_nodes = parser.detect_cycles()

        return DAGValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            topological_order=top_order,
            cycle_nodes=cycle_nodes,
        )

    @staticmethod
    async def create_pipeline(session: AsyncSession, workspace_id: Optional[str], payload: PipelineCreate) -> Pipeline:
        slug = payload.slug or payload.name.lower().replace(" ", "-")
        pipe = Pipeline(
            workspace_id=workspace_id,
            name=payload.name,
            slug=slug,
            description=payload.description,
            pipeline_type=payload.pipeline_type,
            environment=payload.environment,
            tags=payload.tags,
            concurrency_limit=payload.concurrency_limit,
            timeout_seconds=payload.timeout_seconds,
            retry_count=payload.retry_count,
            retry_delay_seconds=payload.retry_delay_seconds,
            status="active",
            is_active=True
        )
        session.add(pipe)
        await session.flush()

        # If initial DAG provided, validate and create Version 1
        if payload.dag and payload.dag.nodes:
            val_res = PipelineService.validate_dag_definition(payload.dag)
            if not val_res.is_valid:
                raise DAGValidationError(f"Invalid DAG: {'; '.join(val_res.errors)}", val_res.errors)

            dag_json = payload.dag.model_dump(mode="json")
            checksum = hashlib.sha256(json.dumps(dag_json, sort_keys=True).encode()).hexdigest()

            v1 = PipelineVersion(
                pipeline_id=pipe.id,
                version_number=1,
                dag_definition_json=dag_json,
                node_count=len(payload.dag.nodes),
                edge_count=len(payload.dag.edges),
                checksum=checksum,
                commit_message=payload.commit_message or "Initial pipeline creation"
            )
            session.add(v1)
            await session.flush()
            pipe.active_version_id = v1.id

        await session.commit()
        await session.refresh(pipe)
        return pipe

    @staticmethod
    async def add_schedule(session: AsyncSession, pipeline_id: str, payload: PipelineScheduleCreate) -> PipelineSchedule:
        pipe = await PipelineService.get_pipeline(session, pipeline_id)
        sched = PipelineSchedule(
            pipeline_id=pipe.id,
            cron_expression=payload.cron_expression,
            interval_seconds=payload.interval_seconds,
            timezone=payload.timezone,
            is_enabled=payload.is_enabled
        )
        session.add(sched)
        await session.commit()
        await session.refresh(sched)
        return sched
