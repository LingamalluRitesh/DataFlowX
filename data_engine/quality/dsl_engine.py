"""
DataFlowX Declarative Quality Assertion DSL Engine
Compiles human-readable assertion DSL expressions (e.g. 'expect column "order_total" > 0 with threshold 99.5%') into executable quality checks.
"""

import re
from typing import Any, Dict, List, Optional
import pandas as pd
from pydantic import BaseModel, Field

from data_engine.quality.rules import BaseQualityRule, RuleEvaluationResult


class DSLAssertion(BaseModel):
    raw_statement: str
    column_name: str
    operator: str
    target_value: Any
    threshold_percentage: float = 100.0


class QualityDSLCompiler:
    """Compiles declarative English-like quality assertions."""

    ASSERTION_PATTERN = re.compile(
        r'expect\s+column\s+["\']?([a-zA-Z0-9_]+)["\']?\s+([><!=]+|between|is not null|matches)\s*(.*?)(?:\s+with\s+threshold\s+(\d+(?:\.\d+)?)%)?$',
        re.IGNORECASE
    )

    @classmethod
    def parse_assertion(cls, statement: str) -> Optional[DSLAssertion]:
        m = cls.ASSERTION_PATTERN.match(statement.strip())
        if not m:
            return None
        col = m.group(1)
        op = m.group(2).lower()
        val = m.group(3).strip() if m.group(3) else None
        thresh = float(m.group(4)) if m.group(4) else 100.0

        return DSLAssertion(
            raw_statement=statement,
            column_name=col,
            operator=op,
            target_value=val,
            threshold_percentage=thresh
        )

    @classmethod
    def execute_dsl_rule(cls, assertion: DSLAssertion, df: pd.DataFrame) -> RuleEvaluationResult:
        col = assertion.column_name
        if col not in df.columns or df.empty:
            return RuleEvaluationResult(rule_name=assertion.raw_statement, target_column=col, passed=True, total_records=0, passed_records=0, failed_records=0, pass_rate=100.0, failed_sample_indices=[])

        total = len(df)
        if assertion.operator in (">", ">=", "<", "<=", "==", "!="):
            numeric_series = pd.to_numeric(df[col], errors="coerce")
            target_num = float(assertion.target_value)
            if assertion.operator == ">":
                pass_mask = numeric_series > target_num
            elif assertion.operator == ">=":
                pass_mask = numeric_series >= target_num
            elif assertion.operator == "<":
                pass_mask = numeric_series < target_num
            elif assertion.operator == "<=":
                pass_mask = numeric_series <= target_num
            elif assertion.operator in ("==", "="):
                pass_mask = numeric_series == target_num
            else:
                pass_mask = numeric_series != target_num

            failed_indices = df.index[~pass_mask].tolist()
        elif assertion.operator == "is not null":
            pass_mask = df[col].notna()
            failed_indices = df.index[~pass_mask].tolist()
        else:
            failed_indices = []

        failed = len(failed_indices)
        passed_cnt = total - failed
        pass_rate = round((passed_cnt / total) * 100, 2) if total > 0 else 100.0
        is_passed = pass_rate >= assertion.threshold_percentage

        return RuleEvaluationResult(
            rule_name=assertion.raw_statement,
            target_column=col,
            passed=is_passed,
            total_records=total,
            passed_records=passed_cnt,
            failed_records=failed,
            pass_rate=pass_rate,
            failed_sample_indices=failed_indices[:10]
        )
