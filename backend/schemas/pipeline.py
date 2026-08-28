"""
DataFlowX Pipeline, DAG, Node, Edge & Scheduling Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class PipelineNodeSchema(BaseModel):
    id: str  # Canvas node key
    type: str  # extract, transform, filter, join, aggregate, quality, sql, python, warehouse_load, branch, notification
    name: str
    config: Dict[str, Any] = Field(default_factory=dict)
    position: Dict[str, float] = Field(default_factory=lambda: {"x": 0.0, "y": 0.0})


class PipelineEdgeSchema(BaseModel):
    id: Optional[str] = None
    source: str
    target: str
    source_handle: Optional[str] = None
    target_handle: Optional[str] = None
    condition: Optional[str] = None


class PipelineDAGDefinition(BaseModel):
    nodes: List[PipelineNodeSchema]
    edges: List[PipelineEdgeSchema]
    globals: Dict[str, Any] = Field(default_factory=dict)


class PipelineScheduleCreate(BaseModel):
    cron_expression: Optional[str] = None
    interval_seconds: Optional[int] = None
    timezone: str = "UTC"
    is_enabled: bool = True


class PipelineScheduleOut(BaseModel):
    id: str
    pipeline_id: str
    cron_expression: Optional[str] = None
    interval_seconds: Optional[int] = None
    timezone: str
    is_enabled: bool
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PipelineTriggerCreate(BaseModel):
    trigger_type: str  # webhook, kafka_event, s3_file_upload, api
    webhook_secret: Optional[str] = None
    event_type: Optional[str] = None
    filter_json: Optional[Dict[str, Any]] = None
    is_enabled: bool = True


class PipelineTriggerOut(BaseModel):
    id: str
    pipeline_id: str
    trigger_type: str
    webhook_secret: Optional[str] = None
    event_type: Optional[str] = None
    filter_json: Optional[Dict[str, Any]] = None
    is_enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PipelineBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    slug: Optional[str] = None
    description: Optional[str] = None
    pipeline_type: str = "batch"  # batch, streaming
    environment: str = "development"  # development, staging, production
    tags: List[str] = []
    concurrency_limit: int = 5
    timeout_seconds: int = 3600
    retry_count: int = 3
    retry_delay_seconds: int = 30


class PipelineCreate(PipelineBase):
    dag: Optional[PipelineDAGDefinition] = None
    commit_message: Optional[str] = "Initial pipeline creation"


class PipelineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    environment: Optional[str] = None
    tags: Optional[List[str]] = None
    concurrency_limit: Optional[int] = None
    timeout_seconds: Optional[int] = None
    retry_count: Optional[int] = None
    retry_delay_seconds: Optional[int] = None
    dag: Optional[PipelineDAGDefinition] = None
    commit_message: Optional[str] = "Updated pipeline definition"


class PipelineVersionOut(BaseModel):
    id: str
    pipeline_id: str
    version_number: int
    dag_definition: PipelineDAGDefinition
    node_count: int
    edge_count: int
    checksum: str
    commit_message: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PipelineOut(PipelineBase):
    id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    slug: str
    status: str
    active_version_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    active_version: Optional[PipelineVersionOut] = None
    schedules: List[PipelineScheduleOut] = []

    model_config = ConfigDict(from_attributes=True)


class DAGValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    topological_order: List[str] = []
    cycle_nodes: List[str] = []
    isolated_nodes: List[str] = []
