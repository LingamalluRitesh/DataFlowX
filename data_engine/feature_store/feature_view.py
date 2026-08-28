"""
DataFlowX ML Feature View & Entity Model
Defines point-in-time correct ML feature definitions, entity primary keys, update cadences, and feature value types.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class FeatureDefinition(BaseModel):
    name: str
    data_type: str  # FLOAT, INT, STRING, VECTOR
    description: str


class FeatureView(BaseModel):
    name: str
    entity_id_column: str
    timestamp_column: str
    features: List[FeatureDefinition] = Field(default_factory=list)
    source_dataset: str
    ttl_days: int = 365
