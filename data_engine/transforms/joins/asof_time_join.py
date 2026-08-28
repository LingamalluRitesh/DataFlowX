"""
DataFlowX Temporal As-Of Join Operator
Joins time-series records matching the closest preceding or succeeding timestamp within an optional tolerance window.
"""

from typing import List, Optional
import pandas as pd


class AsOfTimeJoin:
    """Temporal As-Of Join."""

    @classmethod
    def execute_join(
        cls,
        trades_df: pd.DataFrame,
        quotes_df: pd.DataFrame,
        on_time_col: str,
        by_symbol_col: Optional[str] = None,
        direction: str = "backward",  # backward, forward, nearest
        tolerance: Optional[str] = None
    ) -> pd.DataFrame:
        if trades_df.empty or quotes_df.empty:
            return pd.DataFrame()

        t_df = trades_df.copy()
        q_df = quotes_df.copy()
        t_df[on_time_col] = pd.to_datetime(t_df[on_time_col])
        q_df[on_time_col] = pd.to_datetime(q_df[on_time_col])

        t_df = t_df.sort_values(by=on_time_col).reset_index(drop=True)
        q_df = q_df.sort_values(by=on_time_col).reset_index(drop=True)

        tol = pd.Timedelta(tolerance) if tolerance else None

        return pd.merge_asof(
            t_df,
            q_df,
            on=on_time_col,
            by=by_symbol_col,
            direction=direction,
            tolerance=tol,
            suffixes=("", "_quote")
        )
