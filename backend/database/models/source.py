"""
DataFlowX Data Source & Connector Models
Manages connections to PostgreSQL, MySQL, MongoDB, REST APIs, CSV, Excel, Kafka, S3, MinIO.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON as JSONB, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.database.models.base import SoftDeleteMixin, TenantMixin, TimestampMixin, UUIDPrimaryKeyMixin


class DataSource(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    """External or internal data source connection definition."""
    __tablename__ = "data_sources"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_workspace_source_slug"),)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    connector_type: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # postgres, mysql, mongodb, rest, csv, excel, kafka, s3, minio
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)  # active, degraded, error, testing
    config: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_health_check_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    health_status: Mapped[str] = mapped_column(String(30), default="healthy", nullable=False)  # healthy, unhealthy, unknown

    # Relationships
    credentials: Mapped[Optional["SourceCredential"]] = relationship(
        "SourceCredential",
        back_populates="source",
        uselist=False,
        cascade="all, delete-orphan"
    )
    health_logs: Mapped[List["ConnectionHealthLog"]] = relationship(
        "ConnectionHealthLog",
        back_populates="source",
        cascade="all, delete-orphan"
    )
    schema_snapshots: Mapped[List["SourceSchemaSnapshot"]] = relationship(
        "SourceSchemaSnapshot",
        back_populates="source",
        cascade="all, delete-orphan"
    )


class SourceCredential(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """AES-256-GCM encrypted credentials for data source authentication."""
    __tablename__ = "source_credentials"

    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("data_sources.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    auth_type: Mapped[str] = mapped_column(String(50), default="password", nullable=False)  # password, api_key, oauth2, aws_iam, ssh_key, none
    encrypted_payload: Mapped[str] = mapped_column(Text, nullable=False)
    key_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    source: Mapped["DataSource"] = relationship("DataSource", back_populates="credentials")


class ConnectionHealthLog(Base, UUIDPrimaryKeyMixin):
    """Historical telemetry and ping health logs for data sources."""
    __tablename__ = "connection_health_logs"

    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)  # healthy, unhealthy, timeout
    latency_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True)

    source: Mapped["DataSource"] = relationship("DataSource", back_populates="health_logs")


class SourceSchemaSnapshot(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Introspected metadata snapshot of remote tables/collections/schemas."""
    __tablename__ = "source_schema_snapshots"

    source_id: Mapped[str] = mapped_column(String(36), ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    raw_schema_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    table_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    column_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    source: Mapped["DataSource"] = relationship("DataSource", back_populates="schema_snapshots")
