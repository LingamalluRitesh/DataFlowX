"""
DataFlowX Vectorized Array Set Algebra & Collection Operations
High-performance array operations: distinct, union, intersect, except, compact, and element frequency counting.
"""

from collections import Counter
from typing import Any, List, Optional
import pandas as pd


class ArraySetAlgebra:
    """Vectorized array operations."""

    @staticmethod
    def array_distinct(series: pd.Series) -> pd.Series:
        return series.apply(lambda arr: list(dict.fromkeys(arr)) if isinstance(arr, list) else arr)

    @staticmethod
    def array_union(series_a: pd.Series, series_b: pd.Series) -> pd.Series:
        return pd.Series([
            list(dict.fromkeys((a if isinstance(a, list) else []) + (b if isinstance(b, list) else [])))
            for a, b in zip(series_a, series_b)
        ])

    @staticmethod
    def array_intersect(series_a: pd.Series, series_b: pd.Series) -> pd.Series:
        return pd.Series([
            [x for x in (a if isinstance(a, list) else []) if x in set(b if isinstance(b, list) else [])]
            for a, b in zip(series_a, series_b)
        ])

    @staticmethod
    def array_except(series_a: pd.Series, series_b: pd.Series) -> pd.Series:
        return pd.Series([
            [x for x in (a if isinstance(a, list) else []) if x not in set(b if isinstance(b, list) else [])]
            for a, b in zip(series_a, series_b)
        ])

    @staticmethod
    def array_compact(series: pd.Series) -> pd.Series:
        """Removes None / NaN elements from arrays."""
        return series.apply(lambda arr: [x for x in arr if x is not None and pd.notna(x)] if isinstance(arr, list) else arr)
