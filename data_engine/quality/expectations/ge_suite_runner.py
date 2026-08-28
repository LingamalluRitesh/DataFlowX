"""
DataFlowX Great Expectations Suite Runner
Executes complete JSON expectation suites against target DataFrames and generates standard ValidationResult reports.
"""

from typing import Any, Dict, List
import pandas as pd
from pydantic import BaseModel, Field

from data_engine.quality.expectations.column_expectations import ColumnExpectations, ExpectationResult
from data_engine.quality.expectations.table_expectations import TableExpectations


class ValidationSuiteSummary(BaseModel):
    suite_name: str
    success: bool
    total_evaluated: int
    successful_expectations: int
    unsuccessful_expectations: int
    results: List[ExpectationResult] = Field(default_factory=list)


class GreatExpectationsSuiteRunner:
    """Runs Great Expectations suites."""

    @classmethod
    def run_suite(cls, suite_name: str, df: pd.DataFrame, expectations_config: List[Dict[str, Any]]) -> ValidationSuiteSummary:
        results = []
        for exp in expectations_config:
            exp_type = exp.get("expectation_type")
            kwargs = exp.get("kwargs", {})

            if exp_type == "expect_column_values_to_not_be_null":
                r = ColumnExpectations.expect_column_values_to_not_be_null(df, kwargs["column"])
                results.append(r)
            elif exp_type == "expect_column_values_to_be_unique":
                r = ColumnExpectations.expect_column_values_to_be_unique(df, kwargs["column"])
                results.append(r)
            elif exp_type == "expect_table_row_count_to_be_between":
                r = TableExpectations.expect_table_row_count_to_be_between(df, kwargs.get("min_value", 1), kwargs.get("max_value"))
                results.append(r)

        success_cnt = sum(1 for r in results if r.success)
        return ValidationSuiteSummary(
            suite_name=suite_name,
            success=success_cnt == len(results),
            total_evaluated=len(results),
            successful_expectations=success_cnt,
            unsuccessful_expectations=len(results) - success_cnt,
            results=results
        )
