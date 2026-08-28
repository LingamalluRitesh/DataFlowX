"""
DataFlowX Hierarchical Lexicographical Sort Compactor
Re-writes Lakehouse Parquet partitions sorted by leading query filter columns (e.g., customer_id, transaction_timestamp) to maximize Min/Max zone-map skipping.
"""

from typing import List
import pandas as pd


class SortOrderCompactor:
    """Sorts data partitions prior to Parquet serialization."""

    @classmethod
    def sort_partition(cls, df: pd.DataFrame, sort_columns: List[str], ascending: bool = True) -> pd.DataFrame:
        if df.empty or not sort_columns:
            return df
        valid_cols = [c for c in sort_columns if c in df.columns]
        if not valid_cols:
            return df
        return df.sort_values(by=valid_cols, ascending=ascending).reset_index(drop=True)
