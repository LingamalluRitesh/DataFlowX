"""
Pydantic Schemas for Data Catalog, Data Contracts, Business Glossary & Privacy
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CatalogColumnSchema(BaseModel):
    name: str
    data_type: str
    description: Optional[str] = None
    is_primary_key: bool = False
    is_foreign_key: bool = False
    is_pii: bool = False
    pii_category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class CatalogAssetCreate(BaseModel):
    name: str
    layer: str = "SILVER"
    domain: str = "Enterprise"
    owner: str = "data-team@dataflowx.io"
    description: Optional[str] = None
    storage_uri: Optional[str] = None
    columns_metadata: List[CatalogColumnSchema] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class CatalogAssetOut(CatalogAssetCreate):
    id: str
    workspace_id: str
    quality_score: Optional[float] = 100.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GlossaryTermCreate(BaseModel):
    term: str
    definition: str
    domain: str = "Enterprise"
    owner_email: str
    synonyms: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class GlossaryTermOut(GlossaryTermCreate):
    id: str
    workspace_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ContractColumnSpecSchema(BaseModel):
    name: str
    data_type: str
    is_required: bool = True
    is_unique: bool = False
    allowed_values: Optional[List[Any]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None


class DataContractCreate(BaseModel):
    dataset_name: str
    version: str = "v1.0.0"
    producer: str
    consumers: List[str] = Field(default_factory=list)
    schema_spec: List[ContractColumnSpecSchema] = Field(default_factory=list)
    sla_max_freshness_minutes: int = 1440
    sla_min_quality_score: float = 95.0


class DataContractOut(DataContractCreate):
    id: str
    workspace_id: str
    status: str = "ACTIVE"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
