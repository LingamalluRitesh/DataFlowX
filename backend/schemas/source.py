"""
DataFlowX Data Source & Connector Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class DataSourceBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    slug: Optional[str] = None
    connector_type: str = Field(description="postgres, mysql, mongodb, rest, csv, excel, kafka, s3, minio")
    description: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True


class DataSourceCreate(DataSourceBase):
    credentials: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Raw credentials to encrypt")
    auth_type: str = "password"


class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    credentials: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class DataSourceOut(DataSourceBase):
    id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    slug: str
    status: str
    health_status: str
    last_synced_at: Optional[datetime] = None
    last_health_check_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    has_credentials: bool = False

    model_config = ConfigDict(from_attributes=True)


class ConnectionTestRequest(BaseModel):
    connector_type: str
    config: Dict[str, Any]
    credentials: Optional[Dict[str, Any]] = None


class ConnectionTestResponse(BaseModel):
    success: bool
    status: str  # healthy, unhealthy
    latency_ms: float
    message: str
    details: Optional[Dict[str, Any]] = None


class DiscoveredColumn(BaseModel):
    name: str
    data_type: str
    is_nullable: bool = True
    is_primary_key: bool = False
    is_foreign_key: bool = False
    sample_values: List[Any] = []


class DiscoveredTable(BaseModel):
    name: str
    schema_name: Optional[str] = "public"
    columns: List[DiscoveredColumn] = []
    estimated_rows: Optional[int] = None


class SchemaDiscoveryResponse(BaseModel):
    source_id: str
    connector_type: str
    tables: List[DiscoveredTable] = []
    captured_at: datetime = Field(default_factory=datetime.utcnow)
