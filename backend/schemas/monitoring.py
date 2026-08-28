"""
DataFlowX Monitoring, Alerting & Audit Logging Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class AlertRuleBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: Optional[str] = None
    event_type: str = Field(description="PIPELINE_FAILED, TASK_FAILED, QUALITY_THRESHOLD_BREACH, SLA_MISSED, WORKER_OFFLINE, SCHEMA_CHANGED")
    severity: str = "ERROR"
    condition_json: Dict[str, Any] = Field(default_factory=dict)
    channels_json: List[str] = Field(default_factory=lambda: ["in_app"])
    cooldown_minutes: int = 15
    is_enabled: bool = True


class AlertRuleCreate(AlertRuleBase):
    pass


class AlertRuleOut(AlertRuleBase):
    id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertIncidentOut(BaseModel):
    id: str
    alert_rule_id: str
    execution_id: Optional[str] = None
    title: str
    description: str
    severity: str
    status: str
    details: Dict[str, Any] = {}
    triggered_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AuditLogOut(BaseModel):
    id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    actor_id: Optional[str] = None
    actor_email: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    ip_address: Optional[str] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class SystemOverviewMetrics(BaseModel):
    total_pipelines: int
    active_pipelines: int
    running_executions: int
    total_executions_24h: int
    success_rate_24h: float
    total_records_processed_24h: int
    avg_pipeline_duration_seconds: float
    average_data_quality_score: float
    active_workers_count: int
    active_alert_incidents_count: int
    total_sources: int
    total_datasets: int


class ExecutionTrendPoint(BaseModel):
    timestamp: str
    successful: int
    failed: int
    records_processed: int
