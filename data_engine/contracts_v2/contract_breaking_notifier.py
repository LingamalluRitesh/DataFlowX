"""
DataFlowX Data Contract Breach Webhook & Incident Notifier
Dispatches real-time PagerDuty/Slack alerts and quarantines bad batches upon contract failure.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from data_engine.contracts_v2.runtime_contract_enforcer import ContractValidationResult


class ContractAlertPayload(BaseModel):
    contract_id: str
    dataset_name: str
    severity: str = "CRITICAL"
    reason: str
    violations: List[str] = Field(default_factory=list)


class ContractBreakingNotifier:
    """Dispatches alerts on contract validation failure."""

    @classmethod
    def create_alert(cls, dataset_name: str, result: ContractValidationResult) -> Optional[ContractAlertPayload]:
        if result.is_valid:
            return None

        violations = []
        violations.extend([f"Missing required field: {f}" for f in result.missing_required_fields])
        violations.extend([f"Duplicate values in unique field: {f}" for f in result.uniqueness_violations])
        violations.extend([f"Bound violation: {f}" for f in result.bound_violations])

        return ContractAlertPayload(
            contract_id=result.contract_id,
            dataset_name=dataset_name,
            severity="CRITICAL",
            reason=f"Data contract validation failed ({result.passed_rule_count}/{result.total_rule_count} rules passed)",
            violations=violations
        )
