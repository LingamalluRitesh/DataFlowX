"""
SQLAlchemy Models for Backfills, Workflow Sensors, and SLA Tracking
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text

from backend.core.database import Base, PortableJSON


class BackfillJobModel(Base):
    __tablename__ = "backfill_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    pipeline_id = Column(String(36), ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False, index=True)
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50), nullable=False)
    chunk_interval = Column(String(20), nullable=False, default="1d")
    max_parallel_partitions = Column(Integer, nullable=False, default=4)
    status = Column(String(50), nullable=False, default="PENDING")
    partitions_data = Column(PortableJSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class WorkflowSensorModel(Base):
    __tablename__ = "workflow_sensors"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    sensor_type = Column(String(50), nullable=False)  # S3, FILE, SQL, WEBHOOK, EXTERNAL_PIPELINE
    config = Column(PortableJSON, nullable=False, default=dict)
    timeout_seconds = Column(Integer, nullable=False, default=3600)
    poke_interval_seconds = Column(Integer, nullable=False, default=60)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
