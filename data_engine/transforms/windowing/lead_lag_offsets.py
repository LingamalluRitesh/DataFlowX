"""
DataFlowX Vectorized Window LEAD and LAG Offset Functions
Computes LEAD(col, N, default) and LAG(col, N, default) operations over partitioned order sequences.
"""

from typing import Any, List, Optional
import pandas as pd


class WindowOffsetFunctions:
    """Calculates lead/lag offsets."""

    @classmethod
    def add_lag(cls, df: pd.DataFrame, partition_cols: List[str], target_col: str, offset: int = 1, default_val: Optional[Any] = None, out_col: Optional[str] = None) -> pd.DataFrame:
        if df.empty or target_col not in df.columns:
            return df
        df = df.copy()
        out = out_col or f"{target_col}_lag_{offset}"
        df[out] = df.groupby(partition_cols)[target_col].shift(offset).fillna(default_val)
        return df

    @classmethod
    def add_lead(cls, df: pd.DataFrame, partition_cols: List[str], target_col: str, offset: int = 1, default_val: Optional[Any] = None, out_col: Optional[str] = None) -> pd.DataFrame:
        if df.empty or target_col not in df.columns:
            return df
        df = df.copy()
        out = out_col or f"{target_col}_lead_{offset}"
        df[out] = df.groupby(partition_cols)[target_col].shift(-offset).fillna(default_val)
        return df
