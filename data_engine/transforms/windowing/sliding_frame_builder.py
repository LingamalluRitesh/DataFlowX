"""
DataFlowX SQL Sliding Window Frame Builder
Calculates sliding aggregate frames (ROWS BETWEEN N PRECEDING AND CURRENT ROW) for custom moving averages and bounded sum windows.
"""

from typing import List, Optional
import pandas as pd


class SlidingWindowFrameBuilder:
    """Computes bounded moving frame aggregations."""

    @classmethod
    def apply_moving_average_frame(
        cls,
        df: pd.DataFrame,
        partition_cols: List[str],
        target_col: str,
        preceding_rows: int = 3,
        out_col: Optional[str] = None
    ) -> pd.DataFrame:
        if df.empty or target_col not in df.columns:
            return df
        df = df.copy()
        out = out_col or f"{target_col}_mavg_{preceding_rows}"
        df[out] = df.groupby(partition_cols)[target_col].rolling(window=preceding_rows + 1, min_periods=1).mean().reset_index(level=0, drop=True)
        return df
