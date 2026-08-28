"""
DataFlowX Monitoring, Alerting & Observability Service
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.exceptions import NotFoundError
from backend.database.models import (
    AlertIncident,
    AlertNotification,
    AlertRule,
    DataSource,
    Dataset,
    Execution,
    Pipeline,
    WorkerHeartbeat,
)
from backend.schemas.common import PaginationParams
from backend.schemas.monitoring import AlertRuleCreate, SystemOverviewMetrics


class MonitoringService:
    """Monitoring, KPIs, metrics aggregation, and alert operations."""

    @staticmethod
    async def get_system_overview(session: AsyncSession, workspace_id: Optional[str]) -> SystemOverviewMetrics:
        # Count pipelines
        p_stmt = select(func.count()).select_from(Pipeline).where(Pipeline.is_deleted == False)
        if workspace_id:
            p_stmt = p_stmt.where(Pipeline.workspace_id == workspace_id)
        total_pipelines = (await session.execute(p_stmt)).scalar() or 0

        active_p_stmt = select(func.count()).select_from(Pipeline).where(Pipeline.is_deleted == False, Pipeline.is_active == True)
        if workspace_id:
            active_p_stmt = active_p_stmt.where(Pipeline.workspace_id == workspace_id)
        active_pipelines = (await session.execute(active_p_stmt)).scalar() or 0

        # Count sources & datasets
        s_stmt = select(func.count()).select_from(DataSource).where(DataSource.is_deleted == False)
        d_stmt = select(func.count()).select_from(Dataset).where(Dataset.is_deleted == False)
        if workspace_id:
            s_stmt = s_stmt.where(DataSource.workspace_id == workspace_id)
            d_stmt = d_stmt.where(Dataset.workspace_id == workspace_id)
        total_sources = (await session.execute(s_stmt)).scalar() or 0
        total_datasets = (await session.execute(d_stmt)).scalar() or 0

        # Executions in last 24h
        now = datetime.now(timezone.utc)
        since_24h = now - timedelta(hours=24)

        exec_24h_stmt = select(Execution).where(Execution.created_at >= since_24h)
        if workspace_id:
            exec_24h_stmt = exec_24h_stmt.where(Execution.workspace_id == workspace_id)
        execs_24h = (await session.execute(exec_24h_stmt)).scalars().all()

        total_execs_24h = len(execs_24h)
        successful_24h = sum(1 for e in execs_24h if e.status == "SUCCESS")
        success_rate = (successful_24h / total_execs_24h * 100.0) if total_execs_24h > 0 else 100.0
        total_records_24h = sum(e.total_records_processed for e in execs_24h)

        durations = [e.duration_seconds for e in execs_24h if e.duration_seconds is not None]
        avg_duration = (sum(durations) / len(durations)) if durations else 0.0

        qualities = [e.quality_score for e in execs_24h if e.quality_score is not None]
        avg_quality = (sum(qualities) / len(qualities)) if qualities else 100.0

        running_stmt = select(func.count()).select_from(Execution).where(Execution.status == "RUNNING")
        if workspace_id:
            running_stmt = running_stmt.where(Execution.workspace_id == workspace_id)
        running_execs = (await session.execute(running_stmt)).scalar() or 0

        # Active workers
        w_stmt = select(func.count()).select_from(WorkerHeartbeat).where(WorkerHeartbeat.status == "active")
        active_workers = (await session.execute(w_stmt)).scalar() or 0

        # Open alert incidents
        inc_stmt = select(func.count()).select_from(AlertIncident).where(AlertIncident.status == "TRIGGERED")
        if workspace_id:
            inc_stmt = inc_stmt.where(AlertIncident.workspace_id == workspace_id)
        active_incidents = (await session.execute(inc_stmt)).scalar() or 0

        return SystemOverviewMetrics(
            total_pipelines=total_pipelines,
            active_pipelines=active_pipelines,
            running_executions=running_execs,
            total_executions_24h=total_execs_24h,
            success_rate_24h=round(success_rate, 2),
            total_records_processed_24h=total_records_24h,
            avg_pipeline_duration_seconds=round(avg_duration, 2),
            average_data_quality_score=round(avg_quality, 2),
            active_workers_count=max(active_workers, 1),
            active_alert_incidents_count=active_incidents,
            total_sources=total_sources,
            total_datasets=total_datasets
        )

    @staticmethod
    async def list_alert_rules(session: AsyncSession, workspace_id: Optional[str]) -> List[AlertRule]:
        stmt = select(AlertRule).where(AlertRule.is_deleted == False)
        if workspace_id:
            stmt = stmt.where(AlertRule.workspace_id == workspace_id)
        rules = (await session.execute(stmt.order_by(AlertRule.created_at.desc()))).scalars().all()
        return list(rules)

    @staticmethod
    async def create_alert_rule(session: AsyncSession, workspace_id: Optional[str], payload: AlertRuleCreate) -> AlertRule:
        rule = AlertRule(
            workspace_id=workspace_id,
            name=payload.name,
            description=payload.description,
            event_type=payload.event_type,
            severity=payload.severity,
            condition_json=payload.condition_json,
            channels_json=payload.channels_json,
            cooldown_minutes=payload.cooldown_minutes,
            is_enabled=payload.is_enabled
        )
        session.add(rule)
        await session.commit()
        await session.refresh(rule)
        return rule

    @staticmethod
    async def list_alert_incidents(session: AsyncSession, workspace_id: Optional[str]) -> List[AlertIncident]:
        stmt = select(AlertIncident)
        if workspace_id:
            stmt = stmt.where(AlertIncident.workspace_id == workspace_id)
        incidents = (await session.execute(stmt.order_by(AlertIncident.triggered_at.desc()).limit(100))).scalars().all()
        return list(incidents)
