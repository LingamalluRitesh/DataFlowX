"""
DataFlowX Data Quality Suite Evaluator
Runs composite quality checks, aggregates quality scores, and enforces failure actions.
"""

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from pydantic import BaseModel, Field
from backend.core.exceptions import QualityRuleFailedError
from backend.core.logging import get_logger
from data_engine.quality.quarantine import QuarantineManager
from data_engine.quality.rules import (
    BaseQualityRule,
    CustomSqlRule,
    EmailRule,
    NotNullRule,
    RangeRule,
    RegexRule,
    RuleEvaluationResult,
    UniqueRule,
)

logger = get_logger(__name__)


class SuiteEvaluationSummary(BaseModel):
    total_checks: int
    passed_checks: int
    failed_checks: int
    overall_quality_score: float
    is_suite_passed: bool
    total_records: int
    quarantined_records_count: int
    results: List[RuleEvaluationResult] = Field(default_factory=list)
    quarantine_storage_paths: List[str] = Field(default_factory=list)


class QualitySuiteEvaluator:
    """Evaluates test suites against pandas DataFrames."""

    def __init__(
        self,
        rules: Optional[List[BaseQualityRule]] = None,
        quarantine_manager: Optional[QuarantineManager] = None
    ):
        self.rules: List[BaseQualityRule] = rules or []
        self.quarantine_manager = quarantine_manager or QuarantineManager()

    def add_rule(self, rule: BaseQualityRule) -> "QualitySuiteEvaluator":
        self.rules.append(rule)
        return self

    @classmethod
    def from_check_configs(cls, check_configs: List[Dict[str, Any]]) -> "QualitySuiteEvaluator":
        evaluator = cls()
        for cfg in check_configs:
            rtype = cfg.get("rule_type", "").upper()
            col = cfg.get("target_column")
            name = cfg.get("rule_name") or f"{rtype}_{col}"
            threshold = float(cfg.get("threshold_percentage", 100.0))
            params = cfg.get("condition_params", {})

            if rtype == "NOT_NULL" and col:
                evaluator.add_rule(NotNullRule(target_column=col, name=name, threshold_percentage=threshold))
            elif rtype == "UNIQUE" and col:
                evaluator.add_rule(UniqueRule(target_column=col, name=name, threshold_percentage=threshold))
            elif rtype == "RANGE" and col:
                evaluator.add_rule(RangeRule(
                    target_column=col,
                    min_value=params.get("min"),
                    max_value=params.get("max"),
                    name=name,
                    threshold_percentage=threshold
                ))
            elif rtype == "REGEX" and col:
                evaluator.add_rule(RegexRule(
                    target_column=col,
                    pattern=params.get("pattern", ".*"),
                    name=name,
                    threshold_percentage=threshold
                ))
            elif rtype == "EMAIL" and col:
                evaluator.add_rule(EmailRule(target_column=col, name=name, threshold_percentage=threshold))
            elif rtype == "CUSTOM_SQL":
                evaluator.add_rule(CustomSqlRule(
                    sql_condition=params.get("condition", "1=1"),
                    name=name,
                    threshold_percentage=threshold
                ))
        return evaluator

    def evaluate(
        self,
        df: pd.DataFrame,
        dataset_id: str = "dataset_temp",
        execution_id: str = "exec_temp",
        failure_action: str = "FAIL_PIPELINE",  # FAIL_PIPELINE, WARN_AND_CONTINUE, QUARANTINE_RECORDS
    ) -> Tuple[SuiteEvaluationSummary, pd.DataFrame]:
        """
        Evaluate all configured rules against df.
        Returns evaluation summary and cleaned df (with quarantined rows removed if action is QUARANTINE_RECORDS).
        """
        results: List[RuleEvaluationResult] = []
        all_failed_indices = set()
        quarantine_paths: List[str] = []

        total_records = len(df)

        for rule in self.rules:
            res = rule.evaluate(df)
            results.append(res)
            if not res.passed:
                all_failed_indices.update(res.failed_indices)

        passed_checks = sum(1 for r in results if r.passed)
        failed_checks = len(results) - passed_checks
        avg_score = sum(r.score_percentage for r in results) / len(results) if results else 100.0
        is_suite_passed = (failed_checks == 0)

        cleaned_df = df.copy()

        # Handle failure actions
        if failed_checks > 0:
            if failure_action == "QUARANTINE_RECORDS" and all_failed_indices:
                bad_rows = df.iloc[list(all_failed_indices)].where(pd.notnull(df), None).to_dict(orient="records")
                q_path = self.quarantine_manager.quarantine_records(
                    records=bad_rows,
                    dataset_id=dataset_id,
                    execution_id=execution_id,
                    rule_name="suite_validation",
                    reason="Failed data quality suite checks"
                )
                quarantine_paths.append(q_path)
                # Drop quarantined rows
                cleaned_df = df.drop(index=list(all_failed_indices)).reset_index(drop=True)

            elif failure_action == "FAIL_PIPELINE":
                failed_res = [r for r in results if not r.passed][0]
                logger.error(f"Quality suite failed on rule '{failed_res.rule_name}' with score {failed_res.score_percentage:.2f}%")
                raise QualityRuleFailedError(
                    rule_name=failed_res.rule_name,
                    score=failed_res.score_percentage,
                    threshold=failed_res.threshold_percentage,
                    failed_records=failed_res.failed_records
                )

        summary = SuiteEvaluationSummary(
            total_checks=len(results),
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            overall_quality_score=round(avg_score, 2),
            is_suite_passed=is_suite_passed,
            total_records=total_records,
            quarantined_records_count=len(all_failed_indices) if failure_action == "QUARANTINE_RECORDS" else 0,
            results=results,
            quarantine_storage_paths=quarantine_paths
        )

        return summary, cleaned_df
