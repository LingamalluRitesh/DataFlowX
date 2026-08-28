"""
DataFlowX Monitoring, Alerting, Notifications & Audit Logging Models
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON as JSONB, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.database.models.base import SoftDeleteMixin, TenantMixin, TimestampMixin, UUIDPrimaryKeyMixin


class AlertRule(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    """Configurable conditions that trigger operational alerts."""
    __tablename__ = "alert_rules"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Event Types: PIPELINE_FAILED, TASK_FAILED, QUALITY_THRESHOLD_BREACH, SLA_MISSED, WORKER_OFFLINE, SCHEMA_CHANGED, LONG_RUNNING_PIPELINE
    severity: Mapped[str] = mapped_column(String(20), default="ERROR", nullable=False)  # INFO, WARNING, ERROR, CRITICAL
    condition_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    channels_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)  # email, slack, webhook, in_app
    cooldown_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    incidents: Mapped[List["AlertIncident"]] = relationship("AlertIncident", back_populates="rule", cascade="all, delete-orphan")


class AlertIncident(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """An active or resolved alert incident triggered by an AlertRule."""
    __tablename__ = "alert_incidents"

    alert_rule_id: Mapped[str] = mapped_column(String(36), ForeignKey("alert_rules.id", ondelete="CASCADE"), nullable=False, index=True)
    execution_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("executions.id", ondelete="SET NULL"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="ERROR", nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="TRIGGERED", nullable=False)  # TRIGGERED, ACKNOWLEDGED, RESOLVED, SUPPRESSED
    details_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    triggered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    rule: Mapped["AlertRule"] = relationship("AlertRule", back_populates="incidents")
    notifications: Mapped[List["AlertNotification"]] = relationship("AlertNotification", back_populates="incident", cascade="all, delete-orphan")


class AlertNotification(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Dispatched notification message for an incident across email, slack, or webhook."""
    __tablename__ = "alert_notifications"

    alert_incident_id: Mapped[str] = mapped_column(String(36), ForeignKey("alert_incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    channel_type: Mapped[str] = mapped_column(String(30), nullable=False)  # email, slack, webhook, in_app
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="PENDING", nullable=False)  # PENDING, SENT, FAILED, DELIVERED
    payload_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    incident: Mapped["AlertIncident"] = relationship("AlertIncident", back_populates="notifications")


class NotificationTemplate(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Template for formatting email, slack, or in-app notification content."""
    __tablename__ = "notification_templates"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    channel_type: Mapped[str] = mapped_column(String(30), nullable=False)
    subject_template: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    body_template: Mapped[str] = mapped_column(Text, nullable=False)


class AuditLog(Base, UUIDPrimaryKeyMixin):
    """Immutable audit trail recording every security, pipeline, and data mutation."""
    __tablename__ = "audit_logs"

    organization_id: Mapped[Optional[str]] = mapped_column(String(36), index=True, nullable=True)
    workspace_id: Mapped[Optional[str]] = mapped_column(String(36), index=True, nullable=True)
    actor_id: Mapped[Optional[str]] = mapped_column(String(36), index=True, nullable=True)
    actor_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    action: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    # e.g., USER_LOGIN, PIPELINE_CREATE, PIPELINE_EXECUTE, SOURCE_CREATE, CREDENTIAL_UPDATE, DATASET_DELETE
    resource_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    old_values_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    new_values_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)


class SystemMetric(Base, UUIDPrimaryKeyMixin):
    """Aggregated operational metrics for platform observability dashboards."""
    __tablename__ = "system_metrics"

    metric_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(30), default="count", nullable=False)
    labels_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)
