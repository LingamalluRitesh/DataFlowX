"""
DataFlowX Inline Schema & Guardrail Validation Pipeline Steps
Enforces row count lower/upper bounds, column presence guards, non-null assertions, and type casting safeties.
"""

from typing import Any, List
import pandas as pd


class PipelineValidationGuard:
    """Runtime data assertions and guardrails."""

    @staticmethod
    def assert_row_count(df: pd.DataFrame, min_rows: int = 1, max_rows: Optional[int] = None) -> None:
        count = len(df)
        if count < min_rows:
            raise ValueError(f"Pipeline row count guard failed: {count} rows (minimum expected: {min_rows})")
        if max_rows is not None and count > max_rows:
            raise ValueError(f"Pipeline row count guard failed: {count} rows (maximum allowed: {max_rows})")

    @staticmethod
    def assert_columns_exist(df: pd.DataFrame, required_columns: List[str]) -> None:
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns in pipeline dataset: {missing}")
