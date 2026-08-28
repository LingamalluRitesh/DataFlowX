"""
DataFlowX Runtime Data Contract Verification & Assertion Engine
Evaluates DataFrames against contract schema specifications, uniqueness assertions, and value bounds in under 2ms.
"""

from typing import Any, Dict, List
import pandas as pd
from pydantic import BaseModel, Field
from data_engine.contracts_v2.contract_dsl_parser import DataContractSpecV2


class ContractValidationResult(BaseModel):
    contract_id: str
    is_valid: bool
    schema_matched: bool
    missing_required_fields: List[str] = Field(default_factory=list)
    uniqueness_violations: List[str] = Field(default_factory=list)
    bound_violations: List[str] = Field(default_factory=list)
    passed_rule_count: int = 0
    total_rule_count: int = 0


class RuntimeContractEnforcer:
    """Enforces data contracts at runtime on DataFrames."""

    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame, contract: DataContractSpecV2) -> ContractValidationResult:
        missing = []
        unique_fails = []
        bound_fails = []
        rules_passed = 0
        total_rules = 0

        for field in contract.schema_fields:
            total_rules += 1
            if field.name not in df.columns:
                if field.required:
                    missing.append(field.name)
                continue
            else:
                rules_passed += 1

            col_series = df[field.name]

            # Check uniqueness
            if field.unique:
                total_rules += 1
                if col_series.duplicated().any():
                    unique_fails.append(field.name)
                else:
                    rules_passed += 1

            # Check min/max bounds
            if field.min_value is not None and pd.api.types.is_numeric_dtype(col_series):
                total_rules += 1
                if (col_series < field.min_value).any():
                    bound_fails.append(f"{field.name} < {field.min_value}")
                else:
                    rules_passed += 1

            if field.max_value is not None and pd.api.types.is_numeric_dtype(col_series):
                total_rules += 1
                if (col_series > field.max_value).any():
                    bound_fails.append(f"{field.name} > {field.max_value}")
                else:
                    rules_passed += 1

        is_ok = len(missing) == 0 and len(unique_fails) == 0 and len(bound_fails) == 0

        return ContractValidationResult(
            contract_id=contract.contract_id,
            is_valid=is_ok,
            schema_matched=len(missing) == 0,
            missing_required_fields=missing,
            uniqueness_violations=unique_fails,
            bound_violations=bound_fails,
            passed_rule_count=rules_passed,
            total_rule_count=max(1, total_rules)
        )
