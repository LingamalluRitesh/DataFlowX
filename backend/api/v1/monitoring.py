"""
DataFlowX Monitoring, Alerting & Telemetry Endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.deps import get_active_workspace_id, get_async_db, get_current_user
from backend.database.models import User
from backend.schemas.execution import WorkerHeartbeatOut
from backend.schemas.monitoring import (
    AlertIncidentOut,
    AlertRuleCreate,
    AlertRuleOut,
    SystemOverviewMetrics,
)
from backend.services.monitoring_service import MonitoringService
from orchestration_engine.workers import WorkerNodeManager

router = APIRouter(prefix="/monitoring", tags=["Monitoring & Alerts"])


@router.get("/overview", response_model=SystemOverviewMetrics)
async def get_system_overview(
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    """Retrieve executive KPI metrics: pipeline runs, records processed, success rate, quality scores."""
    return await MonitoringService.get_system_overview(session, workspace_id)


@router.get("/alerts/rules", response_model=List[AlertRuleOut])
async def list_alert_rules(
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    rules = await MonitoringService.list_alert_rules(session, workspace_id)
    return [
        AlertRuleOut(
            id=r.id,
            organization_id=r.organization_id,
            workspace_id=r.workspace_id,
            name=r.name,
            description=r.description,
            event_type=r.event_type,
            severity=r.severity,
            condition_json=r.condition_json,
            channels_json=r.channels_json,
            cooldown_minutes=r.cooldown_minutes,
            is_enabled=r.is_enabled,
            created_at=r.created_at,
            updated_at=r.updated_at
        )
        for r in rules
    ]


@router.post("/alerts/rules", response_model=AlertRuleOut, status_code=status.HTTP_201_CREATED)
async def create_alert_rule(
    payload: AlertRuleCreate,
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    rule = await MonitoringService.create_alert_rule(session, workspace_id, payload)
    return AlertRuleOut(
        id=rule.id,
        organization_id=rule.organization_id,
        workspace_id=rule.workspace_id,
        name=rule.name,
        description=rule.description,
        event_type=rule.event_type,
        severity=rule.severity,
        condition_json=rule.condition_json,
        channels_json=rule.channels_json,
        cooldown_minutes=rule.cooldown_minutes,
        is_enabled=rule.is_enabled,
        created_at=rule.created_at,
        updated_at=rule.updated_at
    )


@router.get("/alerts/incidents", response_model=List[AlertIncidentOut])
async def list_alert_incidents(
    session: AsyncSession = Depends(get_async_db),
    workspace_id: Optional[str] = Depends(get_active_workspace_id),
    _: User = Depends(get_current_user)
):
    incidents = await MonitoringService.list_alert_incidents(session, workspace_id)
    return [
        AlertIncidentOut(
            id=i.id,
            alert_rule_id=i.alert_rule_id,
            execution_id=i.execution_id,
            title=i.title,
            description=i.description,
            severity=i.severity,
            status=i.status,
            details=i.details_json or {},
            triggered_at=i.triggered_at,
            resolved_at=i.resolved_at
        )
        for i in incidents
    ]


@router.get("/workers", response_model=List[WorkerHeartbeatOut])
async def list_workers(_: User = Depends(get_current_user)):
    """Return live worker node registry and CPU/Memory utilization."""
    mgr = WorkerNodeManager()
    telemetry = mgr.get_telemetry()
    return [
        WorkerHeartbeatOut(
            id="worker_primary",
            worker_id=telemetry["worker_id"],
            hostname=telemetry["hostname"],
            ip_address=telemetry["ip_address"],
            queues=["high_priority", "default", "low_priority"],
            active_tasks_count=0,
            memory_used_mb=telemetry["memory_used_mb"],
            cpu_percent=telemetry["cpu_percent"],
            status=telemetry["status"],
            last_heartbeat_at=telemetry["timestamp"]
        )
    ]
