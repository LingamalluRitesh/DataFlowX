"""
DataFlowX Feature Scaling Suite: StandardScaler, MinMaxScaler & RobustScaler
Normalizes numerical feature columns using mean/variance, min/max intervals [0, 1], and median/IQR whisker bounds.
"""

from typing import Dict, List
import pandas as pd


class VectorizedStandardScaler:
    """Z-score normalization."""

    def __init__(self, target_columns: List[str]):
        self.target_columns = target_columns
        self.means_: Dict[str, float] = {}
        self.stds_: Dict[str, float] = {}

    def fit(self, df: pd.DataFrame) -> "VectorizedStandardScaler":
        for col in self.target_columns:
            if col in df.columns:
                series = pd.to_numeric(df[col], errors="coerce").dropna()
                self.means_[col] = float(series.mean())
                self.stds_[col] = float(series.std()) if series.std() != 0 else 1.0
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col in self.target_columns:
            if col in df.columns and col in self.means_:
                mean = self.means_[col]
                std = self.stds_[col]
                df[col] = (pd.to_numeric(df[col], errors="coerce") - mean) / std
        return df
