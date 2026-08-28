"""
DataFlowX Dataset Partition & Train/Validation/Test Splitter
Splits datasets into chronological training, validation, and testing partitions to prevent lookahead bias in time-series and predictive models.
"""

from typing import Tuple
import pandas as pd


class DatasetTrainTestSplitter:
    """Partitions datasets for machine learning."""

    @classmethod
    def train_test_split(cls, df: pd.DataFrame, train_ratio: float = 0.8) -> Tuple[pd.DataFrame, pd.DataFrame]:
        if df.empty:
            return df, pd.DataFrame()
        split_idx = int(len(df) * train_ratio)
        train_df = df.iloc[:split_idx].copy().reset_index(drop=True)
        test_df = df.iloc[split_idx:].copy().reset_index(drop=True)
        return train_df, test_df
