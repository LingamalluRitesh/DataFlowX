"""
DataFlowX Dataset, Schema & Profiling Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class SchemaColumnSchema(BaseModel):
    id: Optional[str] = None
    column_name: str
    data_type: str
    is_nullable: bool = True
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_table: Optional[str] = None
    foreign_column: Optional[str] = None
    description: Optional[str] = None
    ordinal_position: int = 0

    model_config = ConfigDict(from_attributes=True)


class SchemaVersionOut(BaseModel):
    id: str
    schema_id: str
    version_number: int
    checksum: str
    is_active: bool
    created_at: datetime
    columns: List[SchemaColumnSchema] = []

    model_config = ConfigDict(from_attributes=True)


class SchemaModelOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    compatibility_mode: str
    created_at: datetime
    versions: List[SchemaVersionOut] = []

    model_config = ConfigDict(from_attributes=True)


class DatasetBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    slug: Optional[str] = None
    description: Optional[str] = None
    layer: str = "bronze"  # bronze, silver, gold
    format: str = "parquet"
    storage_path: str
    partition_keys: List[str] = []
    tags: List[str] = []
    owner_email: Optional[str] = None


class DatasetCreate(DatasetBase):
    source_id: Optional[str] = None


class DatasetUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    layer: Optional[str] = None
    partition_keys: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    owner_email: Optional[str] = None


class DatasetVersionOut(BaseModel):
    id: str
    dataset_id: str
    version_number: int
    record_count: int
    size_bytes: int
    storage_uri: str
    partition_metadata: Dict[str, Any] = {}
    commit_message: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DatasetOut(DatasetBase):
    id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    source_id: Optional[str] = None
    slug: str
    record_count: int
    size_bytes: int
    quality_score: Optional[float] = 100.0
    is_active: bool
    created_at: datetime
    updated_at: datetime
    versions: List[DatasetVersionOut] = []

    model_config = ConfigDict(from_attributes=True)


class ColumnProfileMetric(BaseModel):
    column_name: str
    data_type: str
    null_count: int
    null_percentage: float
    distinct_count: int
    unique_percentage: float
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    mean_value: Optional[float] = None
    median_value: Optional[float] = None
    std_dev: Optional[float] = None
    top_frequent_values: List[Dict[str, Any]] = []


class ProfilingReportOut(BaseModel):
    id: str
    dataset_id: str
    dataset_version_id: Optional[str] = None
    total_rows: int
    total_columns: int
    null_cells: int
    duplicate_rows: int
    memory_bytes: int
    columns_profile: List[ColumnProfileMetric] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuarantineRecordOut(BaseModel):
    id: str
    dataset_id: str
    execution_id: Optional[str] = None
    task_id: Optional[str] = None
    rule_name: str
    raw_payload: Dict[str, Any]
    error_reason: str
    quarantined_at: datetime
    is_resolved: bool

    model_config = ConfigDict(from_attributes=True)
