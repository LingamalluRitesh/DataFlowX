"""
DataFlowX Data Lineage, Governance & Tagging Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class LineageNodeOut(BaseModel):
    id: str
    entity_type: str  # source, dataset, pipeline, transform, warehouse_table, dashboard
    entity_id: str
    name: str
    layer: Optional[str] = None
    metadata: Dict[str, Any] = {}

    model_config = ConfigDict(from_attributes=True)


class LineageEdgeOut(BaseModel):
    id: str
    source_node_id: str
    target_node_id: str
    transformation_type: str
    pipeline_id: Optional[str] = None
    execution_id: Optional[str] = None
    column_mappings: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class LineageGraphOut(BaseModel):
    nodes: List[LineageNodeOut] = []
    edges: List[LineageEdgeOut] = []


class DataContractBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    dataset_id: str
    sla_freshness_hours: int = 24
    min_quality_score: float = 95.0
    max_null_percentage: float = 5.0
    owner_email: str


class DataContractCreate(DataContractBase):
    schema_version_id: Optional[str] = None


class DataContractOut(DataContractBase):
    id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    schema_version_id: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagBase(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    color: str = "#3b82f6"
    category: str = "domain"
    description: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    id: str
    organization_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
