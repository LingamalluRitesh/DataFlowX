"""
DataFlowX Great Expectations Table-Level Assertions
Implements expect_table_row_count_to_be_between, expect_table_columns_to_match_ordered_set, and expect_table_column_count_to_equal.
"""

from typing import List, Optional
import pandas as pd
from data_engine.quality.expectations.column_expectations import ExpectationResult


class TableExpectations:
    """Executes table-level assertions."""

    @classmethod
    def expect_table_row_count_to_be_between(cls, df: pd.DataFrame, min_value: int = 1, max_value: Optional[int] = None) -> ExpectationResult:
        count = len(df)
        success = count >= min_value
        if max_value is not None and count > max_value:
            success = False

        return ExpectationResult(
            expectation_type="expect_table_row_count_to_be_between",
            success=success,
            unexpected_count=0 if success else 1
        )

    @classmethod
    def expect_table_columns_to_match_ordered_set(cls, df: pd.DataFrame, expected_columns: List[str]) -> ExpectationResult:
        actual_cols = list(df.columns)
        success = actual_cols == expected_columns
        return ExpectationResult(
            expectation_type="expect_table_columns_to_match_ordered_set",
            success=success
        )
