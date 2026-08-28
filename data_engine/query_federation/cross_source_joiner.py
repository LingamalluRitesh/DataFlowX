"""
DataFlowX Cross-Source Streaming Join Coordinator
Coordinates asynchronous chunk streaming and join execution across disparate database engines.
"""

from typing import Any, Dict, Generator, List, Optional
import pandas as pd


class CrossSourceJoinCoordinator:
    """Joins data chunks streamed from different database engines."""

    @classmethod
    def join_streams(
        cls,
        left_df: pd.DataFrame,
        right_df: pd.DataFrame,
        join_key: str,
        how: str = "inner"
    ) -> pd.DataFrame:
        if left_df.empty or right_df.empty:
            return pd.DataFrame()
        return pd.merge(left_df, right_df, on=join_key, how=how, suffixes=("_left", "_right"))
