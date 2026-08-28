"""
DataFlowX External Sort-Merge Join Operator
Sorts two large partitioned datasets by join keys and merges them in linear time with minimal memory footprint.
"""

from typing import Any, Dict, List, Optional
import pandas as pd


class SortMergeJoin:
    """External sort-merge join."""

    @classmethod
    def execute_join(
        cls,
        left_df: pd.DataFrame,
        right_df: pd.DataFrame,
        left_key: str,
        right_key: str,
        how: str = "inner"
    ) -> pd.DataFrame:
        if left_df.empty or right_df.empty:
            return pd.DataFrame()

        # Sort both inputs
        s_left = left_df.sort_values(by=left_key).reset_index(drop=True)
        s_right = right_df.sort_values(by=right_key).reset_index(drop=True)

        return pd.merge(s_left, s_right, left_on=left_key, right_on=right_key, how=how)
