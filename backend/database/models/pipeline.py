"""
DataFlowX Pipeline, DAG, Versioning & Scheduling Models
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON as JSONB, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.database.models.base import SoftDeleteMixin, TenantMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Pipeline(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    """Pipeline definition and DAG container."""
    __tablename__ = "pipelines"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_workspace_pipeline_slug"),)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)  # active, paused, archived, draft
    pipeline_type: Mapped[str] = mapped_column(String(30), default="batch", nullable=False)  # batch, streaming
    active_version_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    environment: Mapped[str] = mapped_column(String(20), default="development", nullable=False)  # development, staging, production
    tags: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True, default=list)
    concurrency_limit: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=3600, nullable=False)
    retry_count: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    retry_delay_seconds: Mapped[int] = mapped_column(Integer, default=30, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    versions: Mapped[List["PipelineVersion"]] = relationship("PipelineVersion", back_populates="pipeline", cascade="all, delete-orphan")
    schedules: Mapped[List["PipelineSchedule"]] = relationship("PipelineSchedule", back_populates="pipeline", cascade="all, delete-orphan")
    triggers: Mapped[List["PipelineTrigger"]] = relationship("PipelineTrigger", back_populates="pipeline", cascade="all, delete-orphan")
    parameters: Mapped[List["PipelineParameter"]] = relationship("PipelineParameter", back_populates="pipeline", cascade="all, delete-orphan")


class PipelineVersion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Immutable versioned snapshot of a pipeline's DAG graph."""
    __tablename__ = "pipeline_versions"
    __table_args__ = (UniqueConstraint("pipeline_id", "version_number", name="uq_pipeline_version_num"),)

    pipeline_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    dag_definition_json: Mapped[dict] = mapped_column(JSONB, nullable=False)  # nodes, edges, globals
    node_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    edge_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    commit_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    pipeline: Mapped["Pipeline"] = relationship("Pipeline", back_populates="versions")
    nodes: Mapped[List["PipelineNode"]] = relationship("PipelineNode", back_populates="pipeline_version", cascade="all, delete-orphan")
    edges: Mapped[List["PipelineEdge"]] = relationship("PipelineEdge", back_populates="pipeline_version", cascade="all, delete-orphan")


class PipelineNode(Base, UUIDPrimaryKeyMixin):
    """Individual task node in a pipeline DAG version."""
    __tablename__ = "pipeline_nodes"

    pipeline_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipeline_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    node_id: Mapped[str] = mapped_column(String(100), nullable=False)  # React Flow canvas node key
    node_type: Mapped[str] = mapped_column(String(50), nullable=False)  # extract, transform, filter, join, aggregate, quality, sql, python, warehouse_load, branch, notification
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    config_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    position_x: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    position_y: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    pipeline_version: Mapped["PipelineVersion"] = relationship("PipelineVersion", back_populates="nodes")


class PipelineEdge(Base, UUIDPrimaryKeyMixin):
    """Directed dependency link between two pipeline DAG nodes."""
    __tablename__ = "pipeline_edges"

    pipeline_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipeline_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    source_node_id: Mapped[str] = mapped_column(String(100), nullable=False)
    target_node_id: Mapped[str] = mapped_column(String(100), nullable=False)
    source_handle: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    target_handle: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    condition_expression: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    pipeline_version: Mapped["PipelineVersion"] = relationship("PipelineVersion", back_populates="edges")


class PipelineParameter(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Configurable runtime parameter for a pipeline."""
    __tablename__ = "pipeline_parameters"
    __table_args__ = (UniqueConstraint("pipeline_id", "param_key", name="uq_pipeline_param_key"),)

    pipeline_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    param_key: Mapped[str] = mapped_column(String(100), nullable=False)
    param_type: Mapped[str] = mapped_column(String(30), default="string", nullable=False)  # string, integer, float, boolean, json, date
    default_value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    pipeline: Mapped["Pipeline"] = relationship("Pipeline", back_populates="parameters")


class PipelineSchedule(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Cron or interval based execution schedule for a pipeline."""
    __tablename__ = "pipeline_schedules"

    pipeline_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    cron_expression: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g., '0 2 * * *'
    interval_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    next_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    pipeline: Mapped["Pipeline"] = relationship("Pipeline", back_populates="schedules")


class PipelineTrigger(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Event or webhook trigger for pipelines."""
    __tablename__ = "pipeline_triggers"

    pipeline_id: Mapped[str] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    trigger_type: Mapped[str] = mapped_column(String(50), nullable=False)  # webhook, kafka_event, s3_file_upload, api
    webhook_secret: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    event_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    filter_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    pipeline: Mapped["Pipeline"] = relationship("Pipeline", back_populates="triggers")
