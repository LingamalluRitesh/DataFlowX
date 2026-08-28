"""
DataFlowX DAG Models & Node Definitions
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class NodeType(str, Enum):
    SOURCE = "source"
    EXTRACT = "extract"
    LOAD = "load"
    FILTER = "filter"
    TRANSFORM = "transform"
    JOIN = "join"
    AGGREGATE = "aggregate"
    SORT = "sort"
    DEDUPLICATE = "deduplicate"
    VALIDATE = "validate"
    QUALITY = "quality"
    SQL_JOB = "sql"
    PYTHON_JOB = "python"
    API_REQUEST = "api_request"
    CONDITIONAL_BRANCH = "branch"
    MERGE = "merge"
    DELAY = "delay"
    NOTIFICATION = "notification"
    WAREHOUSE_LOAD = "warehouse_load"


class DAGNode(BaseModel):
    id: str
    type: str
    name: str
    config: Dict[str, Any] = Field(default_factory=dict)
    position: Dict[str, float] = Field(default_factory=lambda: {"x": 0.0, "y": 0.0})


class DAGEdge(BaseModel):
    id: Optional[str] = None
    source: str
    target: str
    source_handle: Optional[str] = None
    target_handle: Optional[str] = None
    condition: Optional[str] = None


class DAGDefinition(BaseModel):
    nodes: List[DAGNode]
    edges: List[DAGEdge]
    globals: Dict[str, Any] = Field(default_factory=dict)
