"""
DataFlowX Multi-Dimensional Aggregation & Cube Rollup Pipeline Steps
Computes hierarchical Group-By rollups, multidimensional OLAP cubes, pivot matrices, and weighted average metrics.
"""

from typing import Dict, List, Optional
import pandas as pd


class AggregationToolkit:
    """OLAP aggregations and rollups."""

    @staticmethod
    def group_by_summary(
        df: pd.DataFrame,
        group_cols: List[str],
        agg_map: Dict[str, List[str]]
    ) -> pd.DataFrame:
        """Executes multi-column group-by aggregations."""
        if df.empty:
            return df
        return df.groupby(group_cols, as_index=False).agg(agg_map)

    @staticmethod
    def weighted_average(df: pd.DataFrame, value_col: str, weight_col: str, group_cols: List[str]) -> pd.DataFrame:
        if df.empty:
            return df

        def calc_w_avg(group):
            w = group[weight_col]
            v = group[value_col]
            sum_w = w.sum()
            return (v * w).sum() / sum_w if sum_w > 0 else 0.0

        res = df.groupby(group_cols).apply(calc_w_avg).reset_index(name=f"weighted_avg_{value_col}")
        return res
