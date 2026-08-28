"""
DataFlowX Time Series Resampling & Gap Filling Engine
Provides time-series downsampling, upsampling, linear/polynomial interpolations, forward/backward fills, and date part extraction.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

from backend.core.logging import get_logger
from data_engine.transformation.operators import BaseOperator

logger = get_logger(__name__)


class TimeSeriesResampleOperator(BaseOperator):
    """Resamples regular or irregular time series data into fixed interval buckets (1min, 5min, 1h, 1d)."""

    def __init__(
        self,
        time_column: str,
        freq: str = "1h",  # '1min', '5min', '1h', '1d', '1W', '1M'
        aggregations: Dict[str, str] = {"value": "mean"},
        partition_by: Optional[List[str]] = None,
        fill_method: Optional[str] = "ffill"  # ffill, bfill, zero, none
    ):
        self.time_column = time_column
        self.freq = freq
        self.aggregations = aggregations
        self.partition_by = partition_by or []
        self.fill_method = fill_method

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.time_column not in df.columns:
            return df
        df = df.copy()
        df[self.time_column] = pd.to_datetime(df[self.time_column])

        valid_part = [c for c in self.partition_by if c in df.columns]

        if valid_part:
            resampled_list = []
            for name, group in df.groupby(valid_part):
                g = group.set_index(self.time_column).resample(self.freq).agg(self.aggregations)
                if self.fill_method == "ffill":
                    g = g.ffill()
                elif self.fill_method == "bfill":
                    g = g.bfill()
                elif self.fill_method == "zero":
                    g = g.fillna(0)

                g = g.reset_index()
                if isinstance(name, tuple):
                    for idx, pcol in enumerate(valid_part):
                        g[pcol] = name[idx]
                else:
                    g[valid_part[0]] = name
                resampled_list.append(g)
            return pd.concat(resampled_list, ignore_index=True)
        else:
            res = df.set_index(self.time_column).resample(self.freq).agg(self.aggregations)
            if self.fill_method == "ffill":
                res = res.ffill()
            elif self.fill_method == "bfill":
                res = res.bfill()
            elif self.fill_method == "zero":
                res = res.fillna(0)
            return res.reset_index()


class DatePartExtractionOperator(BaseOperator):
    """Extracts calendar and temporal components: year, month, day, hour, day_of_week, quarter, is_weekend."""

    def __init__(self, time_column: str, prefix: Optional[str] = None):
        self.time_column = time_column
        self.prefix = prefix or time_column

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.time_column not in df.columns:
            return df
        df = df.copy()
        dt_series = pd.to_datetime(df[self.time_column])

        df[f"{self.prefix}_year"] = dt_series.dt.year
        df[f"{self.prefix}_month"] = dt_series.dt.month
        df[f"{self.prefix}_day"] = dt_series.dt.day
        df[f"{self.prefix}_hour"] = dt_series.dt.hour
        df[f"{self.prefix}_dayofweek"] = dt_series.dt.dayofweek
        df[f"{self.prefix}_quarter"] = dt_series.dt.quarter
        df[f"{self.prefix}_is_weekend"] = dt_series.dt.dayofweek.isin([5, 6]).astype(int)

        return df
