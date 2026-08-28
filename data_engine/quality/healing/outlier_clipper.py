"""
DataFlowX Statistical Outlier Boundary Clipper & Winsorizer
Clamps statistical outliers to 3-sigma Z-score limits or Tukey 1.5x IQR whiskers to prevent skewed training sets and analytics.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


class OutlierClipper:
    """Clamps extreme values to statistical boundary percentiles."""

    @classmethod
    def clip_zscore(cls, df: pd.DataFrame, column_name: str, max_zscore: float = 3.0) -> pd.DataFrame:
        if df.empty or column_name not in df.columns:
            return df
        df = df.copy()
        series = pd.to_numeric(df[column_name], errors="coerce")
        mean = series.mean()
        std = series.std()

        if std == 0 or np.isnan(std):
            return df

        lower_bound = mean - max_zscore * std
        upper_bound = mean + max_zscore * std

        df[column_name] = series.clip(lower=lower_bound, upper=upper_bound)
        return df

    @classmethod
    def clip_iqr(cls, df: pd.DataFrame, column_name: str, multiplier: float = 1.5) -> pd.DataFrame:
        if df.empty or column_name not in df.columns:
            return df
        df = df.copy()
        series = pd.to_numeric(df[column_name], errors="coerce")
        q25 = series.quantile(0.25)
        q75 = series.quantile(0.75)
        iqr = q75 - q25

        lower_bound = q25 - multiplier * iqr
        upper_bound = q75 + multiplier * iqr

        df[column_name] = series.clip(lower=lower_bound, upper=upper_bound)
        return df
