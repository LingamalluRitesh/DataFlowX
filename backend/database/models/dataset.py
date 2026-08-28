"""
DataFlowX Dataset Catalog, Schema Management & Data Profiling Models
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import BigInteger, Boolean, DateTime, Float, ForeignKey, Integer, JSON as JSONB, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.database.models.base import SoftDeleteMixin, TenantMixin, TimestampMixin, UUIDPrimaryKeyMixin


class Dataset(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    """First-class registered dataset asset in the data catalog."""
    __tablename__ = "datasets"
    __table_args__ = (UniqueConstraint("workspace_id", "slug", name="uq_workspace_dataset_slug"),)

    source_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("data_sources.id", ondelete="SET NULL"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    layer: Mapped[str] = mapped_column(String(20), default="bronze", nullable=False)  # bronze, silver, gold
    format: Mapped[str] = mapped_column(String(20), default="parquet", nullable=False)  # parquet, csv, json, avro, delta
    record_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True, default=100.0)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    partition_keys: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True, default=list)
    tags: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    owner_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    versions: Mapped[List["DatasetVersion"]] = relationship("DatasetVersion", back_populates="dataset", cascade="all, delete-orphan")
    profiling_reports: Mapped[List["DatasetProfilingReport"]] = relationship("DatasetProfilingReport", back_populates="dataset", cascade="all, delete-orphan")
    quarantined_records: Mapped[List["QuarantineRecord"]] = relationship("QuarantineRecord", back_populates="dataset", cascade="all, delete-orphan")


class DatasetVersion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Immutable snapshot of a dataset version."""
    __tablename__ = "dataset_versions"
    __table_args__ = (UniqueConstraint("dataset_id", "version_number", name="uq_dataset_version_number"),)

    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    schema_version_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("schema_versions.id", ondelete="SET NULL"), nullable=True)
    record_count: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    storage_uri: Mapped[str] = mapped_column(String(500), nullable=False)
    partition_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    commit_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="versions")
    schema_version: Mapped[Optional["SchemaVersion"]] = relationship("SchemaVersion")


class SchemaModel(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Schema entity representing tabular/document structures."""
    __tablename__ = "schemas"
    __table_args__ = (UniqueConstraint("workspace_id", "name", name="uq_workspace_schema_name"),)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    compatibility_mode: Mapped[str] = mapped_column(String(30), default="BACKWARD", nullable=False)  # BACKWARD, FORWARD, FULL, NONE

    # Relationships
    versions: Mapped[List["SchemaVersion"]] = relationship("SchemaVersion", back_populates="schema_parent", cascade="all, delete-orphan")


class SchemaVersion(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Specific versioned structure of a schema."""
    __tablename__ = "schema_versions"
    __table_args__ = (UniqueConstraint("schema_id", "version_number", name="uq_schema_version_num"),)

    schema_id: Mapped[str] = mapped_column(String(36), ForeignKey("schemas.id", ondelete="CASCADE"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    schema_parent: Mapped["SchemaModel"] = relationship("SchemaModel", back_populates="versions")
    columns: Mapped[List["SchemaColumn"]] = relationship("SchemaColumn", back_populates="schema_version", cascade="all, delete-orphan")


class SchemaColumn(Base, UUIDPrimaryKeyMixin):
    """Individual column definition within a schema version."""
    __tablename__ = "schema_columns"
    __table_args__ = (UniqueConstraint("schema_version_id", "column_name", name="uq_version_column"),)

    schema_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("schema_versions.id", ondelete="CASCADE"), nullable=False, index=True)
    column_name: Mapped[str] = mapped_column(String(150), nullable=False)
    data_type: Mapped[str] = mapped_column(String(50), nullable=False)  # string, int64, float64, boolean, timestamp, json, array
    is_nullable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_primary_key: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_foreign_key: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    foreign_table: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    foreign_column: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ordinal_position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    schema_version: Mapped["SchemaVersion"] = relationship("SchemaVersion", back_populates="columns")


class SchemaDiff(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Audit differences between two schema versions."""
    __tablename__ = "schema_diffs"

    schema_id: Mapped[str] = mapped_column(String(36), ForeignKey("schemas.id", ondelete="CASCADE"), nullable=False, index=True)
    old_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("schema_versions.id", ondelete="CASCADE"), nullable=False)
    new_version_id: Mapped[str] = mapped_column(String(36), ForeignKey("schema_versions.id", ondelete="CASCADE"), nullable=False)
    change_type: Mapped[str] = mapped_column(String(50), nullable=False)  # ADD_COLUMN, DROP_COLUMN, TYPE_ALTER, COMPATIBLE, BREAKING
    diff_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_breaking: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class DatasetProfilingReport(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Statistical summary and column-level profiling metrics."""
    __tablename__ = "dataset_profiling_reports"

    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    dataset_version_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("dataset_versions.id", ondelete="SET NULL"), nullable=True)
    total_rows: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    total_columns: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    null_cells: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    duplicate_rows: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    memory_bytes: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    columns_profile_json: Mapped[dict] = mapped_column(JSONB, nullable=False)  # min, max, avg, stddev, null_pct, unique_pct, top_k

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="profiling_reports")


class QuarantineRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Records that failed data quality validation rules quarantined for inspection."""
    __tablename__ = "quarantine_records"

    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    execution_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True, index=True)
    task_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    rule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    raw_payload_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    error_reason: Mapped[str] = mapped_column(Text, nullable=False)
    quarantined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    dataset: Mapped["Dataset"] = relationship("Dataset", back_populates="quarantined_records")
