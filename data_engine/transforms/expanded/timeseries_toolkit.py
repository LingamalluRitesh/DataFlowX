"""
DataFlowX Time-Series Analytics & Signal Processing Toolkit
Computes Exponential Moving Averages (EMA), Simple Moving Averages (SMA), Bollinger Bands, rolling volatility, and lag differences.
"""

from typing import List, Optional
import pandas as pd


class TimeSeriesToolkit:
    """Vectorized time series transformations."""

    @staticmethod
    def apply_exponential_moving_avg(df: pd.DataFrame, value_col: str, span: int = 14, out_col: Optional[str] = None) -> pd.DataFrame:
        if df.empty or value_col not in df.columns:
            return df
        df = df.copy()
        out = out_col or f"{value_col}_ema_{span}"
        df[out] = df[value_col].ewm(span=span, adjust=False).mean()
        return df

    @staticmethod
    def apply_bollinger_bands(df: pd.DataFrame, value_col: str, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
        if df.empty or value_col not in df.columns:
            return df
        df = df.copy()
        rolling_mean = df[value_col].rolling(window=window).mean()
        rolling_std = df[value_col].rolling(window=window).std()

        df[f"{value_col}_bb_upper"] = rolling_mean + (rolling_std * num_std)
        df[f"{value_col}_bb_lower"] = rolling_mean - (rolling_std * num_std)
        return df
