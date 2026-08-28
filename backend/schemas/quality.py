"""
DataFlowX Data Quality Schemas
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class QualityRuleDefBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    rule_type: str = Field(description="NOT_NULL, UNIQUE, RANGE, REGEX, EMAIL, DATA_TYPE, DATE_RANGE, FOREIGN_KEY, DUPLICATE_CHECK, CUSTOM_SQL, CUSTOM_PYTHON")
    description: Optional[str] = None
    parameters_schema: Dict[str, Any] = Field(default_factory=dict)
    default_severity: str = "ERROR"


class QualityRuleDefCreate(QualityRuleDefBase):
    pass


class QualityRuleDefOut(QualityRuleDefBase):
    id: str
    is_builtin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QualityCheckBase(BaseModel):
    rule_name: str
    rule_type: str
    target_column: Optional[str] = None
    condition_params: Dict[str, Any] = Field(default_factory=dict)
    threshold_percentage: float = 100.0
    failure_action: str = "FAIL_PIPELINE"
    is_enabled: bool = True


class QualityCheckCreate(QualityCheckBase):
    rule_definition_id: Optional[str] = None
    dataset_id: Optional[str] = None


class QualityCheckOut(QualityCheckBase):
    id: str
    quality_suite_id: str
    dataset_id: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QualitySuiteBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: Optional[str] = None
    is_active: bool = True


class QualitySuiteCreate(QualitySuiteBase):
    checks: List[QualityCheckCreate] = []


class QualitySuiteOut(QualitySuiteBase):
    id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    created_at: datetime
    checks: List[QualityCheckOut] = []

    model_config = ConfigDict(from_attributes=True)


class QualityResultOut(BaseModel):
    id: str
    execution_id: Optional[str] = None
    task_execution_id: Optional[str] = None
    rule_name: str
    rule_type: str
    target_column: Optional[str] = None
    total_records: int
    passed_records: int
    failed_records: int
    quarantined_records: int
    score_percentage: float
    passed: bool
    details: Dict[str, Any] = {}
    evaluated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QualityEvaluateRequest(BaseModel):
    suite_id: Optional[str] = None
    dataset_id: str
    sample_records: Optional[List[Dict[str, Any]]] = None
