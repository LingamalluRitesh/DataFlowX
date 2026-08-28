"""
Pydantic Schemas for Backfills, Workflow Sensors & SLAs
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class BackfillCreate(BaseModel):
    pipeline_id: str
    start_date: str
    end_date: str
    chunk_interval: str = "1d"
    max_parallel_partitions: int = 4


class BackfillOut(BackfillCreate):
    id: str
    workspace_id: str
    status: str
    partitions_data: List[Dict[str, Any]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WorkflowSensorCreate(BaseModel):
    name: str
    sensor_type: str
    config: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = 3600
    poke_interval_seconds: int = 60
    is_active: bool = True


class WorkflowSensorOut(WorkflowSensorCreate):
    id: str
    workspace_id: str
    created_at: datetime

    class Config:
        from_attributes = True
