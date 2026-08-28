"""
DataFlowX Vectorized Conditional & Logical Functions
Provides vectorized COALESCE, NULLIF, IF_ELSE, CASE WHEN, and GREATEST/LEAST evaluation.
"""

from typing import Any, Callable, List, Optional, Tuple, Union
import numpy as np
import pandas as pd


class ConditionalFunctions:
    """Vectorized conditional logic functions."""

    @staticmethod
    def coalesce(*series_list: pd.Series) -> pd.Series:
        if not series_list:
            return pd.Series([])
        res = series_list[0].copy()
        for s in series_list[1:]:
            res = res.combine_first(s)
        return res

    @staticmethod
    def nullif(series_a: pd.Series, series_b: Union[Any, pd.Series]) -> pd.Series:
        res = series_a.copy()
        if isinstance(series_b, pd.Series):
            mask = series_a == series_b
        else:
            mask = series_a == series_b
        res[mask] = np.nan
        return res

    @staticmethod
    def if_else(condition: pd.Series, true_series: Union[Any, pd.Series], false_series: Union[Any, pd.Series]) -> pd.Series:
        return pd.Series(np.where(condition, true_series, false_series), index=condition.index)

    @staticmethod
    def nvl(series: pd.Series, fallback: Any) -> pd.Series:
        return series.fillna(fallback)

    @staticmethod
    def nvl2(series: pd.Series, not_null_val: Any, null_val: Any) -> pd.Series:
        return pd.Series(np.where(series.notna(), not_null_val, null_val), index=series.index)

    @staticmethod
    def greatest(*series_list: pd.Series) -> pd.Series:
        if not series_list:
            return pd.Series([])
        df = pd.concat(series_list, axis=1)
        return df.max(axis=1)

    @staticmethod
    def least(*series_list: pd.Series) -> pd.Series:
        if not series_list:
            return pd.Series([])
        df = pd.concat(series_list, axis=1)
        return df.min(axis=1)

    @classmethod
    def case_when(cls, df: pd.DataFrame, when_then_pairs: List[Tuple[pd.Series, Any]], default_val: Any = None) -> pd.Series:
        res = pd.Series(default_val, index=df.index)
        # Apply in reverse so earlier pairs take precedence
        for cond, val in reversed(when_then_pairs):
            if isinstance(val, pd.Series):
                res = np.where(cond, val, res)
            else:
                res = np.where(cond, val, res)
        return pd.Series(res, index=df.index)
