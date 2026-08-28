"""
DataFlowX Vectorized Cumulative Aggregation Window Functions
Calculates running cumulative sums (CUMSUM), running minimums (CUMMIN), running maximums (CUMMAX), and running products (CUMPROD).
"""

from typing import List, Optional
import pandas as pd


class CumulativeAggregates:
    """Calculates running cumulative statistics."""

    @classmethod
    def add_cumulative_sum(cls, df: pd.DataFrame, partition_cols: List[str], target_col: str, out_col: Optional[str] = None) -> pd.DataFrame:
        if df.empty or target_col not in df.columns:
            return df
        df = df.copy()
        out = out_col or f"{target_col}_cumsum"
        df[out] = df.groupby(partition_cols)[target_col].cumsum()
        return df

    @classmethod
    def add_cumulative_max(cls, df: pd.DataFrame, partition_cols: List[str], target_col: str, out_col: Optional[str] = None) -> pd.DataFrame:
        if df.empty or target_col not in df.columns:
            return df
        df = df.copy()
        out = out_col or f"{target_col}_cummax"
        df[out] = df.groupby(partition_cols)[target_col].cummax()
        return df
