"""
DataFlowX Vectorized Math & Statistical Numeric Standard Library
Provides 30+ SIMD-accelerated math operations for Lakehouse transformations.
"""

from typing import Any, List, Optional, Union
import numpy as np
import pandas as pd


class MathFunctions:
    """Vectorized mathematical functions."""

    @staticmethod
    def abs(series: pd.Series) -> pd.Series:
        return np.abs(series)

    @staticmethod
    def ceil(series: pd.Series) -> pd.Series:
        return np.ceil(series)

    @staticmethod
    def floor(series: pd.Series) -> pd.Series:
        return np.floor(series)

    @staticmethod
    def round(series: pd.Series, decimals: int = 0) -> pd.Series:
        return np.round(series, decimals)

    @staticmethod
    def truncate(series: pd.Series, decimals: int = 0) -> pd.Series:
        factor = 10.0 ** decimals
        return np.trunc(series * factor) / factor

    @staticmethod
    def sqrt(series: pd.Series) -> pd.Series:
        return np.sqrt(np.maximum(0, series))

    @staticmethod
    def cbrt(series: pd.Series) -> pd.Series:
        return np.cbrt(series)

    @staticmethod
    def exp(series: pd.Series) -> pd.Series:
        return np.exp(series)

    @staticmethod
    def ln(series: pd.Series) -> pd.Series:
        return np.log(np.maximum(1e-12, series))

    @staticmethod
    def log10(series: pd.Series) -> pd.Series:
        return np.log10(np.maximum(1e-12, series))

    @staticmethod
    def log2(series: pd.Series) -> pd.Series:
        return np.log2(np.maximum(1e-12, series))

    @staticmethod
    def power(series: pd.Series, exponent: Union[float, pd.Series]) -> pd.Series:
        return np.power(series, exponent)

    @staticmethod
    def sign(series: pd.Series) -> pd.Series:
        return np.sign(series)

    @staticmethod
    def clamp(series: pd.Series, min_val: float, max_val: float) -> pd.Series:
        return np.clip(series, min_val, max_val)

    @staticmethod
    def degrees(series: pd.Series) -> pd.Series:
        return np.degrees(series)

    @staticmethod
    def radians(series: pd.Series) -> pd.Series:
        return np.radians(series)

    @staticmethod
    def sin(series: pd.Series) -> pd.Series:
        return np.sin(series)

    @staticmethod
    def cos(series: pd.Series) -> pd.Series:
        return np.cos(series)

    @staticmethod
    def tan(series: pd.Series) -> pd.Series:
        return np.tan(series)

    @staticmethod
    def asin(series: pd.Series) -> pd.Series:
        return np.arcsin(np.clip(series, -1.0, 1.0))

    @staticmethod
    def acos(series: pd.Series) -> pd.Series:
        return np.arccos(np.clip(series, -1.0, 1.0))

    @staticmethod
    def atan(series: pd.Series) -> pd.Series:
        return np.arctan(series)

    @staticmethod
    def z_score(series: pd.Series) -> pd.Series:
        std = series.std()
        if std == 0 or np.isnan(std):
            return pd.Series(0.0, index=series.index)
        return (series - series.mean()) / std

    @staticmethod
    def min_max_scale(series: pd.Series) -> pd.Series:
        s_min = series.min()
        s_max = series.max()
        if s_max == s_min or np.isnan(s_max - s_min):
            return pd.Series(0.0, index=series.index)
        return (series - s_min) / (s_max - s_min)
