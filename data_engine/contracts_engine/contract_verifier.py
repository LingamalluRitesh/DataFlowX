"""
DataFlowX Data Contract Runtime Verifier
Executes runtime physical data validation checks against target Parquet/Delta tables to ensure contract conformance.
"""

from typing import Any, Dict, List, Optional
import pandas as pd
from pydantic import BaseModel, Field

from data_engine.contracts_engine.contract_spec import DataContractSpecification


class VerificationCheckResult(BaseModel):
    check_name: str
    column_name: Optional[str] = None
    passed: bool
    details: str


class ContractVerificationSummary(BaseModel):
    contract_id: str
    dataset_name: str
    is_conforming: bool
    total_checks: int
    passed_checks: int
    failed_checks: int
    check_results: List[VerificationCheckResult] = Field(default_factory=list)


class DataContractVerifier:
    """Verifies live DataFrames against published DataContractSpecification."""

    @classmethod
    def verify_dataframe(cls, df: pd.DataFrame, contract: DataContractSpecification) -> ContractVerificationSummary:
        results = []

        # Check required columns
        for col_spec in contract.columns:
            if col_spec.is_required:
                present = col_spec.name in df.columns
                results.append(VerificationCheckResult(
                    check_name="column_presence",
                    column_name=col_spec.name,
                    passed=present,
                    details=f"Required column '{col_spec.name}' present in dataset" if present else f"Missing required column '{col_spec.name}'"
                ))

                if present:
                    null_cnt = df[col_spec.name].isna().sum()
                    results.append(VerificationCheckResult(
                        check_name="not_null_check",
                        column_name=col_spec.name,
                        passed=null_cnt == 0,
                        details=f"Zero null values ({null_cnt} found)"
                    ))

        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed

        return ContractVerificationSummary(
            contract_id=contract.contract_id,
            dataset_name=contract.dataset_name,
            is_conforming=failed == 0,
            total_checks=len(results),
            passed_checks=passed,
            failed_checks=failed,
            check_results=results
        )
