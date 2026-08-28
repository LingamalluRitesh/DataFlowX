"""
DataFlowX Great Expectations Standard Column Assertions
Implements core Great Expectations column assertions: expect_column_values_to_not_be_null, expect_column_values_to_be_unique, expect_column_values_to_be_in_set, expect_column_values_to_be_between.
"""

from typing import Any, List, Optional, Set
import pandas as pd
from pydantic import BaseModel


class ExpectationResult(BaseModel):
    expectation_type: str
    column: Optional[str] = None
    success: bool
    unexpected_count: int = 0
    unexpected_percent: float = 0.0


class ColumnExpectations:
    """Executes column data quality assertions."""

    @classmethod
    def expect_column_values_to_not_be_null(cls, df: pd.DataFrame, column: str) -> ExpectationResult:
        if column not in df.columns:
            return ExpectationResult(expectation_type="expect_column_values_to_not_be_null", column=column, success=False, unexpected_count=len(df), unexpected_percent=100.0)
        null_cnt = int(df[column].isna().sum())
        total = len(df) or 1
        pct = round((null_cnt / total) * 100.0, 2)
        return ExpectationResult(
            expectation_type="expect_column_values_to_not_be_null",
            column=column,
            success=null_cnt == 0,
            unexpected_count=null_cnt,
            unexpected_percent=pct
        )

    @classmethod
    def expect_column_values_to_be_unique(cls, df: pd.DataFrame, column: str) -> ExpectationResult:
        if column not in df.columns:
            return ExpectationResult(expectation_type="expect_column_values_to_be_unique", column=column, success=False)
        dupes = int(df[column].duplicated().sum())
        total = len(df) or 1
        pct = round((dupes / total) * 100.0, 2)
        return ExpectationResult(
            expectation_type="expect_column_values_to_be_unique",
            column=column,
            success=dupes == 0,
            unexpected_count=dupes,
            unexpected_percent=pct
        )
