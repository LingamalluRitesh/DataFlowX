"""
DataFlowX Composable Machine Learning Feature Engineering Pipeline
Sequentially executes feature scalers, encoders, and mathematical transformers with fit() and transform() semantics.
"""

from typing import Any, List, Tuple
import pandas as pd


class MLFeaturePipeline:
    """Sequential feature transformer."""

    def __init__(self, steps: List[Tuple[str, Any]]):
        self.steps = steps

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        working_df = df.copy()
        for name, transformer in self.steps:
            working_df = transformer.fit(working_df).transform(working_df)
        return working_df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        working_df = df.copy()
        for name, transformer in self.steps:
            working_df = transformer.transform(working_df)
        return working_df
