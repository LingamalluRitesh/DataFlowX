"""
SQLAlchemy Models for Data Catalog, Data Contracts, Business Glossary, and Governance
"""

from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.core.database import Base, PortableJSON


class CatalogAssetModel(Base):
    __tablename__ = "catalog_assets"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    layer = Column(String(50), nullable=False, default="SILVER")
    domain = Column(String(100), nullable=False, default="Enterprise", index=True)
    owner = Column(String(255), nullable=False, default="data-team@dataflowx.io")
    description = Column(Text, nullable=True)
    storage_uri = Column(String(512), nullable=True)
    quality_score = Column(Float, nullable=True, default=100.0)
    columns_metadata = Column(PortableJSON, nullable=False, default=list)
    tags = Column(PortableJSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


class GlossaryTermModel(Base):
    __tablename__ = "glossary_terms"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    term = Column(String(150), nullable=False, index=True)
    definition = Column(Text, nullable=False)
    domain = Column(String(100), nullable=False, default="Enterprise", index=True)
    owner_email = Column(String(255), nullable=False)
    synonyms = Column(PortableJSON, nullable=False, default=list)
    tags = Column(PortableJSON, nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class DataContractModel(Base):
    __tablename__ = "enterprise_data_contracts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String(36), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False, index=True)
    dataset_name = Column(String(255), nullable=False, index=True)
    version = Column(String(50), nullable=False, default="v1.0.0")
    producer = Column(String(255), nullable=False)
    consumers = Column(PortableJSON, nullable=False, default=list)
    schema_spec = Column(PortableJSON, nullable=False, default=list)
    sla_max_freshness_minutes = Column(Integer, nullable=False, default=1440)
    sla_min_quality_score = Column(Float, nullable=False, default=95.0)
    status = Column(String(50), nullable=False, default="ACTIVE")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
