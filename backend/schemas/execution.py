"""
DataFlowX Execution, Task, Log & Worker Telemetry Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ExecutionTriggerRequest(BaseModel):
    """Payload to trigger a pipeline run."""
    version_id: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)


class TaskLogOut(BaseModel):
    id: str
    task_execution_id: Optional[str] = None
    log_level: str
    message: str
    metadata_json: Optional[Dict[str, Any]] = None
    logged_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskExecutionOut(BaseModel):
    id: str
    execution_id: str
    node_id: str
    task_type: str
    name: str
    status: str
    worker_id: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    attempt_number: int
    max_retries: int
    records_in: int
    records_out: int
    bytes_processed: int
    error_message: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExecutionMetricOut(BaseModel):
    metric_name: str
    metric_value: float
    metric_unit: str
    tags: Dict[str, Any] = {}
    recorded_at: datetime


class ExecutionOut(BaseModel):
    id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    pipeline_id: str
    pipeline_version_id: Optional[str] = None
    execution_type: str
    trigger_source: Optional[str] = None
    status: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    total_records_processed: int
    total_bytes_processed: int
    records_failed: int
    quality_score: Optional[float] = None
    error_summary: Optional[str] = None
    parameters: Dict[str, Any] = {}
    created_at: datetime
    tasks: List[TaskExecutionOut] = []

    model_config = ConfigDict(from_attributes=True)


class WorkerHeartbeatOut(BaseModel):
    id: str
    worker_id: str
    hostname: str
    ip_address: str
    queues: List[str] = []
    active_tasks_count: int
    memory_used_mb: float
    cpu_percent: float
    status: str
    last_heartbeat_at: datetime

    model_config = ConfigDict(from_attributes=True)
