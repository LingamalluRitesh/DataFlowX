"""
DataFlowX Vectorized One-Hot & Target Frequency Encoder
Transforms high-cardinality categorical columns into sparse binary vectors with handle_unknown='ignore' fallback support.
"""

from typing import Dict, List, Set
import pandas as pd


class VectorizedOneHotEncoder:
    """Encodes categorical series into binary columns."""

    def __init__(self, target_columns: List[str]):
        self.target_columns = target_columns
        self.categories_: Dict[str, List[str]] = {}

    def fit(self, df: pd.DataFrame) -> "VectorizedOneHotEncoder":
        for col in self.target_columns:
            if col in df.columns:
                unique_vals = sorted([str(v) for v in df[col].dropna().unique()])
                self.categories_[col] = unique_vals
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col, categories in self.categories_.items():
            if col in df.columns:
                for cat in categories:
                    df[f"{col}_{cat}"] = (df[col].astype(str) == cat).astype(int)
                df = df.drop(columns=[col])
        return df
