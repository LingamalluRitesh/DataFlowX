"""
DataFlowX Data Contract Breaking Change Analyzer
Computes semantic contract compatibility between version N and version N+1 to prevent downstream data outages and schema breakage.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from data_engine.contracts_engine.contract_spec import DataContractSpecification


class ContractDiffViolation(BaseModel):
    violation_type: str  # COLUMN_DELETED, TYPE_INCOMPATIBLE, CONSTRAINT_ADDED, SLA_DEGRADED
    column_name: Optional[str] = None
    description: str
    severity: str  # BREAKING, WARNING, COMPATIBLE


class ContractCompatibilityReport(BaseModel):
    is_backward_compatible: bool
    violations: List[ContractDiffViolation] = Field(default_factory=list)
    suggested_version_bump: str = "PATCH"  # MAJOR, MINOR, PATCH


class BreakingChangeAnalyzer:
    """Analyzes schema diffs between contract versions."""

    @classmethod
    def analyze_diff(cls, old_contract: DataContractSpecification, new_contract: DataContractSpecification) -> ContractCompatibilityReport:
        old_cols = {c.name.lower(): c for c in old_contract.columns}
        new_cols = {c.name.lower(): c for c in new_contract.columns}

        violations = []
        is_breaking = False

        # 1. Dropped columns
        for name, col in old_cols.items():
            if name not in new_cols:
                violations.append(ContractDiffViolation(
                    violation_type="COLUMN_DELETED",
                    column_name=col.name,
                    description=f"Required column '{col.name}' was removed from the contract",
                    severity="BREAKING"
                ))
                is_breaking = True

        # 2. Altered column types
        for name, col in old_cols.items():
            if name in new_cols:
                new_c = new_cols[name]
                if col.data_type.upper() != new_c.data_type.upper():
                    violations.append(ContractDiffViolation(
                        violation_type="TYPE_INCOMPATIBLE",
                        column_name=col.name,
                        description=f"Column '{col.name}' data type changed from '{col.data_type}' to '{new_c.data_type}'",
                        severity="BREAKING"
                    ))
                    is_breaking = True

        # 3. New required columns
        for name, col in new_cols.items():
            if name not in old_cols and col.is_required:
                violations.append(ContractDiffViolation(
                    violation_type="CONSTRAINT_ADDED",
                    column_name=col.name,
                    description=f"New non-nullable column '{col.name}' was introduced",
                    severity="WARNING"
                ))

        suggested = "MAJOR" if is_breaking else "MINOR" if len(new_cols) > len(old_cols) else "PATCH"

        return ContractCompatibilityReport(
            is_backward_compatible=not is_breaking,
            violations=violations,
            suggested_version_bump=suggested
        )
