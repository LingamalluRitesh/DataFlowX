"""
DataFlowX Execution, Task State, Distributed Worker & Lock Models
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, JSON as JSONB, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.database.models.base import TenantMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Execution(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """A single execution run of a pipeline."""
    __tablename__ = "executions"

    pipeline_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    pipeline_version_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("pipeline_versions.id", ondelete="SET NULL"), nullable=True)
    execution_type: Mapped[str] = mapped_column(String(30), default="manual", nullable=False)  # manual, scheduled, triggered, backfill
    trigger_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="CREATED", index=True, nullable=False)
    # Statuses: CREATED, QUEUED, RUNNING, SUCCESS, FAILED, RETRYING, CANCELLED, PAUSED, TIMEOUT

    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    total_records_processed: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    total_bytes_processed: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    records_failed: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    error_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parameters_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    run_context: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)  # XCom state dictionary
    triggered_by_user_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    tasks: Mapped[List["TaskExecution"]] = relationship("TaskExecution", back_populates="execution", cascade="all, delete-orphan")
    logs: Mapped[List["TaskLog"]] = relationship("TaskLog", back_populates="execution", cascade="all, delete-orphan")


class TaskExecution(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Execution state of an individual node/task within a pipeline run."""
    __tablename__ = "task_executions"

    execution_id: Mapped[str] = mapped_column(String(36), ForeignKey("executions.id", ondelete="CASCADE"), nullable=False, index=True)
    node_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # DAG node identifier
    task_type: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="PENDING", index=True, nullable=False)
    # Statuses: PENDING, QUEUED, RUNNING, SUCCESS, FAILED, RETRYING, SKIPPED, CANCELLED

    worker_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    attempt_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    retry_delay: Mapped[int] = mapped_column(Integer, default=10, nullable=False)

    records_in: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    records_out: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    bytes_processed: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    output_payload_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_traceback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    execution: Mapped["Execution"] = relationship("Execution", back_populates="tasks")
    logs: Mapped[List["TaskLog"]] = relationship("TaskLog", back_populates="task_execution", cascade="all, delete-orphan")


class TaskLog(Base, UUIDPrimaryKeyMixin):
    """Structured line-by-line task execution log entry."""
    __tablename__ = "task_logs"

    execution_id: Mapped[str] = mapped_column(String(36), ForeignKey("executions.id", ondelete="CASCADE"), nullable=False, index=True)
    task_execution_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("task_executions.id", ondelete="CASCADE"), nullable=True, index=True)
    log_level: Mapped[str] = mapped_column(String(20), default="INFO", index=True, nullable=False)  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    message: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)

    execution: Mapped["Execution"] = relationship("Execution", back_populates="logs")
    task_execution: Mapped[Optional["TaskExecution"]] = relationship("TaskExecution", back_populates="logs")


class ExecutionMetric(Base, UUIDPrimaryKeyMixin):
    """Detailed time-series telemetry recorded during pipeline execution."""
    __tablename__ = "execution_metrics"

    execution_id: Mapped[str] = mapped_column(String(36), ForeignKey("executions.id", ondelete="CASCADE"), nullable=False, index=True)
    task_execution_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("task_executions.id", ondelete="CASCADE"), nullable=True)
    metric_name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    metric_unit: Mapped[str] = mapped_column(String(30), default="count", nullable=False)
    tags_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


class WorkerHeartbeat(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Distributed worker node registration and health heartbeat."""
    __tablename__ = "worker_heartbeats"

    worker_id: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hostname: Mapped[str] = mapped_column(String(150), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    queues_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    active_tasks_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    memory_used_mb: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cpu_percent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)  # active, busy, offline, draining
    last_heartbeat_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


class DistributedLock(Base):
    """Distributed locking record for schedulers and exclusive operations."""
    __tablename__ = "distributed_locks"

    lock_key: Mapped[str] = mapped_column(String(200), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(100), nullable=False)
    acquired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
