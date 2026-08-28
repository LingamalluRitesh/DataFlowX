"""
DataFlowX Interval Range Overlap Join Operator
Joins records based on timestamp or numerical interval containment ([start, end] overlaps [target_start, target_end]).
"""

from typing import Any, Dict, List, Optional
import pandas as pd


class IntervalRangeJoin:
    """Interval overlap join."""

    @classmethod
    def execute_range_join(
        cls,
        events_df: pd.DataFrame,
        intervals_df: pd.DataFrame,
        event_time_col: str,
        interval_start_col: str,
        interval_end_col: str,
        key_col: Optional[str] = None
    ) -> pd.DataFrame:
        if events_df.empty or intervals_df.empty:
            return pd.DataFrame()

        results = []
        for _, ev in events_df.iterrows():
            e_time = ev[event_time_col]
            e_key = ev[key_col] if key_col else None

            # Filter matching intervals
            matches = intervals_df[
                (intervals_df[interval_start_col] <= e_time) & (intervals_df[interval_end_col] >= e_time)
            ]
            if key_col:
                matches = matches[matches[key_col] == e_key]

            for _, int_row in matches.iterrows():
                merged = dict(ev.to_dict())
                for k, v in int_row.to_dict().items():
                    if k != key_col:
                        merged[f"interval_{k}"] = v
                results.append(merged)

        return pd.DataFrame(results)
