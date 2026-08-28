"""
DataFlowX Reference Lookup & Geographic Enrichment Pipeline Steps
Joins dimension lookup dictionaries, maps ISO country codes, and parses timestamps into temporal components (quarter, day_of_week, is_weekend).
"""

from typing import Any, Dict, Optional
import pandas as pd


class DataEnrichmentToolkit:
    """Enriches data streams with derived dimensions and lookups."""

    @staticmethod
    def map_dictionary_lookup(df: pd.DataFrame, source_col: str, lookup_dict: Dict[Any, Any], target_col: str, default_val: Optional[Any] = None) -> pd.DataFrame:
        if df.empty or source_col not in df.columns:
            return df
        df = df.copy()
        df[target_col] = df[source_col].map(lookup_dict).fillna(default_val)
        return df

    @staticmethod
    def add_temporal_features(df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
        if df.empty or timestamp_col not in df.columns:
            return df
        df = df.copy()
        ts = pd.to_datetime(df[timestamp_col], errors="coerce")
        df["year"] = ts.dt.year
        df["month"] = ts.dt.month
        df["quarter"] = ts.dt.quarter
        df["day_of_week"] = ts.dt.day_name()
        df["is_weekend"] = ts.dt.dayofweek >= 5
        return df
