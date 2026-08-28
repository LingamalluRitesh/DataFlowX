"""
DataFlowX OpenDataContract Standard Specification v2.2.0 Parser
Defines schemas for Data Contracts: Schema specifications, column constraints, SLA commitments (freshness, availability), and team ownership.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ColumnConstraint(BaseModel):
    constraint_type: str  # UNIQUE, NOT_NULL, MIN, MAX, REGEX, ENUM
    parameters: Dict[str, Any] = Field(default_factory=dict)


class ContractColumnSpec(BaseModel):
    name: str
    data_type: str
    is_required: bool = True
    is_pii: bool = False
    business_term: Optional[str] = None
    description: Optional[str] = None
    constraints: List[ColumnConstraint] = Field(default_factory=list)


class SLAContractSpec(BaseModel):
    max_latency_seconds: int = 3600
    freshness_cron: Optional[str] = None
    availability_uptime_pct: float = 99.9
    quality_threshold_pct: float = 99.0


class DataContractSpecification(BaseModel):
    contract_id: str
    version: str = "1.0.0"
    dataset_name: str
    domain: str
    owner_team: str
    owner_email: str
    sla: SLAContractSpec = Field(default_factory=SLAContractSpec)
    columns: List[ContractColumnSpec] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
