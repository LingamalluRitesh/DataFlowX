"""
DataFlowX Git CI/CD Pull Request Contract Webhook Handler
Intercepts GitHub / GitLab pull request webhook payloads, runs BreakingChangeAnalyzer on modified contract YAML files, and posts status checks.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger
from data_engine.contracts_engine.breaking_change_analyzer import BreakingChangeAnalyzer, ContractCompatibilityReport
from data_engine.contracts_engine.contract_spec import DataContractSpecification

logger = get_logger(__name__)


class GitPRCheckResult(BaseModel):
    pr_number: int
    repository: str
    status: str  # SUCCESS, FAILURE, NEUTRAL
    conclusion_summary: str
    compatibility: ContractCompatibilityReport


class GitWebhookPRHandler:
    """Handles GitHub pull_request webhook events."""

    @classmethod
    def evaluate_pr_contracts(
        cls,
        pr_number: int,
        repository: str,
        base_contract: DataContractSpecification,
        head_contract: DataContractSpecification
    ) -> GitPRCheckResult:
        report = BreakingChangeAnalyzer.analyze_diff(base_contract, head_contract)
        status = "SUCCESS" if report.is_backward_compatible else "FAILURE"

        summary = (
            f"Data Contract check passed: 100% backward compatible (Bump: {report.suggested_version_bump})"
            if report.is_backward_compatible
            else f"Data Contract check failed: {len(report.violations)} breaking changes detected without major version bump!"
        )

        logger.info(f"PR #{pr_number} contract check: {status} ({summary})")
        return GitPRCheckResult(
            pr_number=pr_number,
            repository=repository,
            status=status,
            conclusion_summary=summary,
            compatibility=report
        )
