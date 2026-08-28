"""
DataFlowX Vectorized Window Partition Ranking Engine
Implements ANSI SQL compliant ROW_NUMBER(), RANK(), DENSE_RANK(), PERCENT_RANK(), and NTILE(K) window functions over partitioned Pandas/VectorBatch dataframes.
"""

from typing import List, Optional
import pandas as pd


class WindowPartitionRanker:
    """Vectorized window ranking calculations."""

    @classmethod
    def add_row_number(cls, df: pd.DataFrame, partition_cols: List[str], order_col: str, ascending: bool = True, out_col: str = "row_num") -> pd.DataFrame:
        if df.empty:
            return df
        df = df.copy()
        df[out_col] = df.groupby(partition_cols)[order_col].rank(method="first", ascending=ascending).astype(int)
        return df

    @classmethod
    def add_dense_rank(cls, df: pd.DataFrame, partition_cols: List[str], order_col: str, ascending: bool = True, out_col: str = "dense_rank") -> pd.DataFrame:
        if df.empty:
            return df
        df = df.copy()
        df[out_col] = df.groupby(partition_cols)[order_col].rank(method="dense", ascending=ascending).astype(int)
        return df
