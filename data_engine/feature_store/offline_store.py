"""
DataFlowX Point-in-Time Correct Offline Training Feature Generator
Performs point-in-time ASOF joins between entity observation timestamps and feature values to prevent data leakage in training datasets.
"""

from typing import Any, Dict, List, Optional
import pandas as pd
from pydantic import BaseModel


class OfflineFeatureStore:
    """Generates training datasets with point-in-time correctness."""

    @classmethod
    def get_historical_features(
        cls,
        entity_df: pd.DataFrame,
        feature_df: pd.DataFrame,
        entity_id_col: str,
        timestamp_col: str,
        feature_cols: List[str]
    ) -> pd.DataFrame:
        if entity_df.empty or feature_df.empty:
            return entity_df

        e_sorted = entity_df.sort_values(by=timestamp_col).copy()
        f_sorted = feature_df.sort_values(by=timestamp_col).copy()

        # Perform merge_asof
        merged = pd.merge_asof(
            e_sorted,
            f_sorted[[entity_id_col, timestamp_col] + feature_cols],
            by=entity_id_col,
            on=timestamp_col,
            direction="backward"
        )
        return merged
