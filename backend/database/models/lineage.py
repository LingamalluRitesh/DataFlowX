"""
DataFlowX Data Lineage & Governance Models
Tracks complete provenance and dependencies: Source -> Raw Dataset -> Clean Dataset -> Transformations -> Gold Dataset -> Warehouse -> Analytics.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON as JSONB, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.database.models.base import SoftDeleteMixin, TenantMixin, TimestampMixin, UUIDPrimaryKeyMixin


class LineageNode(Base, UUIDPrimaryKeyMixin, TimestampMixin, TenantMixin):
    """Entity node in the data lineage graph (Source, Dataset, Pipeline, Model, Dashboard)."""
    __tablename__ = "lineage_nodes"
    __table_args__ = (UniqueConstraint("workspace_id", "entity_type", "entity_id", name="uq_workspace_lineage_entity"),)

    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # source, dataset, pipeline, transform, warehouse_table, dashboard
    entity_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    layer: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # bronze, silver, gold, warehouse, source
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    outgoing_edges: Mapped[List["LineageEdge"]] = relationship("LineageEdge", foreign_keys="LineageEdge.source_node_id", back_populates="source_node", cascade="all, delete-orphan")
    incoming_edges: Mapped[List["LineageEdge"]] = relationship("LineageEdge", foreign_keys="LineageEdge.target_node_id", back_populates="target_node", cascade="all, delete-orphan")


class LineageEdge(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Directed dependency edge between two lineage nodes."""
    __tablename__ = "lineage_edges"

    source_node_id: Mapped[str] = mapped_column(String(36), ForeignKey("lineage_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    target_node_id: Mapped[str] = mapped_column(String(36), ForeignKey("lineage_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    transformation_type: Mapped[str] = mapped_column(String(50), default="PIPELINE_RUN", nullable=False)
    pipeline_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("pipelines.id", ondelete="SET NULL"), nullable=True)
    execution_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("executions.id", ondelete="SET NULL"), nullable=True)
    column_mappings_json: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)

    source_node: Mapped["LineageNode"] = relationship("LineageNode", foreign_keys=[source_node_id], back_populates="outgoing_edges")
    target_node: Mapped["LineageNode"] = relationship("LineageNode", foreign_keys=[target_node_id], back_populates="incoming_edges")


class LineageEvent(Base, UUIDPrimaryKeyMixin):
    """Discrete lineage lifecycle event emitted during pipeline executions."""
    __tablename__ = "lineage_events"

    execution_id: Mapped[str] = mapped_column(String(36), ForeignKey("executions.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)  # START, COMPLETE, FAIL, ABORT
    inputs_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    outputs_json: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    facets_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)  # schema, quality, metrics
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


class DataContract(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    """Formal SLA and schema compliance contract for datasets."""
    __tablename__ = "data_contracts"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    dataset_id: Mapped[str] = mapped_column(String(36), ForeignKey("datasets.id", ondelete="CASCADE"), nullable=False, index=True)
    schema_version_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("schema_versions.id", ondelete="SET NULL"), nullable=True)
    sla_freshness_hours: Mapped[int] = mapped_column(Integer, default=24, nullable=False)
    min_quality_score: Mapped[float] = mapped_column(Float, default=95.0, nullable=False)
    max_null_percentage: Mapped[float] = mapped_column(Float, default=5.0, nullable=False)
    owner_email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="ACTIVE", nullable=False)  # ACTIVE, VIOLATED, DRAFT


class TagDefinition(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Metadata tag taxonomy for classification and data governance."""
    __tablename__ = "tag_definitions"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(20), default="#3b82f6", nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="domain", nullable=False)  # compliance, domain, tier, sensitivity
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class EntityTag(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Junction mapping tags to datasets, pipelines, and data sources."""
    __tablename__ = "entity_tags"
    __table_args__ = (UniqueConstraint("tag_id", "entity_type", "entity_id", name="uq_entity_tag"),)

    tag_id: Mapped[str] = mapped_column(String(36), ForeignKey("tag_definitions.id", ondelete="CASCADE"), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)  # dataset, pipeline, source
    entity_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    applied_by_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    tag: Mapped["TagDefinition"] = relationship("TagDefinition")
