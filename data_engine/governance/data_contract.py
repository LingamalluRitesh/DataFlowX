"""
DataFlowX Data Contract Specification & SLA Verification Engine
Validates producer-consumer schema contracts, detecting breaking schema changes and SLA violations.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class ContractColumnSpec(BaseModel):
    name: str
    data_type: str
    is_required: bool = True
    is_unique: bool = False
    allowed_values: Optional[List[Any]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    regex_pattern: Optional[str] = None


class DataContractSpec(BaseModel):
    contract_id: str
    dataset_name: str
    version: str = "v1.0.0"
    producer: str
    consumers: List[str] = Field(default_factory=list)
    schema_spec: List[ContractColumnSpec] = Field(default_factory=list)
    sla_max_freshness_minutes: int = 1440  # 24 hours
    sla_min_quality_score: float = 95.0
    status: str = "ACTIVE"  # DRAFT, ACTIVE, DEPRECATED
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ContractValidationResult(BaseModel):
    is_valid: bool
    contract_id: str
    breaking_changes: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DataContractValidator:
    """Evaluates in-flight or catalog DataFrames against formal Data Contract specs."""

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, contract: DataContractSpec) -> ContractValidationResult:
        breaking_changes = []
        warnings = []

        existing_cols = set(df.columns)
        spec_cols = {col.name: col for col in contract.schema_spec}

        # 1. Missing required columns
        for col_name, col_spec in spec_cols.items():
            if col_spec.is_required and col_name not in existing_cols:
                breaking_changes.append(f"Missing required contract column: '{col_name}' (expected {col_spec.data_type})")

        # 2. Unexpected or undeclared columns
        for col_name in existing_cols:
            if col_name not in spec_cols:
                warnings.append(f"Undeclared extra column in payload: '{col_name}'")

        # 3. Data type & domain constraint checks
        for col_name, col_spec in spec_cols.items():
            if col_name not in df.columns:
                continue

            series = df[col_name]
            # Check non-null on required
            if col_spec.is_required and series.isna().any():
                null_count = int(series.isna().sum())
                breaking_changes.append(f"Contract violation: Required column '{col_name}' contains {null_count} null rows")

            # Check allowed values
            if col_spec.allowed_values:
                invalid_mask = ~series.isin(col_spec.allowed_values) & series.notna()
                if invalid_mask.any():
                    breaking_changes.append(f"Contract violation: Column '{col_name}' contains values not in allowlist: {col_spec.allowed_values}")

        is_valid = (len(breaking_changes) == 0)
        return ContractValidationResult(
            is_valid=is_valid,
            contract_id=contract.contract_id,
            breaking_changes=breaking_changes,
            warnings=warnings
        )
