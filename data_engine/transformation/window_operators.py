"""
DataFlowX Advanced Window Functions & Analytical Partition Operators
Provides vectorized window calculations: row_number, rank, dense_rank, lead/lag, rolling averages, moving sums, exponential moving averages, and sessionization.
"""

from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd

from backend.core.logging import get_logger
from data_engine.transformation.operators import BaseOperator

logger = get_logger(__name__)


class RowNumberOperator(BaseOperator):
    """Assigns sequential integer rank per partition ordered by specific columns."""

    def __init__(self, partition_by: List[str], order_by: List[str], output_col: str = "row_num", ascending: bool = True):
        self.partition_by = partition_by
        self.order_by = order_by
        self.output_col = output_col
        self.ascending = ascending

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        df = df.copy()
        valid_part = [c for c in self.partition_by if c in df.columns]
        valid_order = [c for c in self.order_by if c in df.columns]

        if valid_order:
            df = df.sort_values(by=valid_part + valid_order, ascending=self.ascending)

        if valid_part:
            df[self.output_col] = df.groupby(valid_part).cumcount() + 1
        else:
            df[self.output_col] = np.arange(1, len(df) + 1)
        return df


class DenseRankOperator(BaseOperator):
    """Computes dense rank per partition without gaps in ranking values."""

    def __init__(self, partition_by: List[str], order_by_col: str, output_col: str = "dense_rank", ascending: bool = True):
        self.partition_by = partition_by
        self.order_by_col = order_by_col
        self.output_col = output_col
        self.ascending = ascending

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.order_by_col not in df.columns:
            return df
        df = df.copy()
        valid_part = [c for c in self.partition_by if c in df.columns]

        if valid_part:
            df[self.output_col] = df.groupby(valid_part)[self.order_by_col].rank(method="dense", ascending=self.ascending).astype(int)
        else:
            df[self.output_col] = df[self.order_by_col].rank(method="dense", ascending=self.ascending).astype(int)
        return df


class LeadLagOperator(BaseOperator):
    """Shifts values within partition by offset (Lead = positive offset, Lag = negative offset)."""

    def __init__(
        self,
        target_column: str,
        offset: int = 1,
        partition_by: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
        default_value: Any = None,
        output_col: Optional[str] = None
    ):
        self.target_column = target_column
        self.offset = offset
        self.partition_by = partition_by or []
        self.order_by = order_by or []
        self.default_value = default_value
        op_name = "lead" if offset > 0 else "lag"
        self.output_col = output_col or f"{self.target_column}_{op_name}_{abs(offset)}"

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.target_column not in df.columns:
            return df
        df = df.copy()
        valid_part = [c for c in self.partition_by if c in df.columns]
        valid_order = [c for c in self.order_by if c in df.columns]

        if valid_order:
            df = df.sort_values(by=valid_part + valid_order)

        if valid_part:
            df[self.output_col] = df.groupby(valid_part)[self.target_column].shift(-self.offset)
        else:
            df[self.output_col] = df[self.target_column].shift(-self.offset)

        if self.default_value is not None:
            df[self.output_col] = df[self.output_col].fillna(self.default_value)
        return df


class RollingWindowAggregateOperator(BaseOperator):
    """Calculates moving window aggregations (mean, sum, min, max, std) over fixed N rows or time intervals."""

    def __init__(
        self,
        target_column: str,
        window_size: int,
        aggregation: str = "mean",  # mean, sum, min, max, std
        partition_by: Optional[List[str]] = None,
        order_by_col: Optional[str] = None,
        output_col: Optional[str] = None
    ):
        self.target_column = target_column
        self.window_size = window_size
        self.aggregation = aggregation.lower()
        self.partition_by = partition_by or []
        self.order_by_col = order_by_col
        self.output_col = output_col or f"{self.target_column}_rolling_{self.aggregation}_{self.window_size}"

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.target_column not in df.columns:
            return df
        df = df.copy()
        valid_part = [c for c in self.partition_by if c in df.columns]

        if self.order_by_col and self.order_by_col in df.columns:
            df = df.sort_values(by=valid_part + [self.order_by_col])

        def apply_rolling(series: pd.Series) -> pd.Series:
            roller = series.rolling(window=self.window_size, min_periods=1)
            if self.aggregation == "sum":
                return roller.sum()
            elif self.aggregation == "min":
                return roller.min()
            elif self.aggregation == "max":
                return roller.max()
            elif self.aggregation == "std":
                return roller.std().fillna(0.0)
            return roller.mean()

        if valid_part:
            df[self.output_col] = df.groupby(valid_part)[self.target_column].transform(apply_rolling)
        else:
            df[self.output_col] = apply_rolling(df[self.target_column])
        return df


class ExponentialMovingAverageOperator(BaseOperator):
    """Computes Exponential Moving Average (EMA) with decay span alpha."""

    def __init__(
        self,
        target_column: str,
        span: int = 14,
        partition_by: Optional[List[str]] = None,
        output_col: Optional[str] = None
    ):
        self.target_column = target_column
        self.span = span
        self.partition_by = partition_by or []
        self.output_col = output_col or f"{self.target_column}_ema_{self.span}"

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.target_column not in df.columns:
            return df
        df = df.copy()
        valid_part = [c for c in self.partition_by if c in df.columns]

        if valid_part:
            df[self.output_col] = df.groupby(valid_part)[self.target_column].transform(
                lambda s: s.ewm(span=self.span, adjust=False).mean()
            )
        else:
            df[self.output_col] = df[self.target_column].ewm(span=self.span, adjust=False).mean()
        return df


class SessionizationOperator(BaseOperator):
    """Partitions continuous time-series events into user sessions based on inactivity threshold."""

    def __init__(
        self,
        user_col: str,
        timestamp_col: str,
        max_inactivity_minutes: int = 30,
        session_id_col: str = "session_id"
    ):
        self.user_col = user_col
        self.timestamp_col = timestamp_col
        self.max_inactivity_seconds = max_inactivity_minutes * 60
        self.session_id_col = session_id_col

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.user_col not in df.columns or self.timestamp_col not in df.columns:
            return df
        df = df.copy()
        df[self.timestamp_col] = pd.to_datetime(df[self.timestamp_col])
        df = df.sort_values(by=[self.user_col, self.timestamp_col])

        # Compute time difference between subsequent events per user
        df["_time_diff"] = df.groupby(self.user_col)[self.timestamp_col].diff().dt.total_seconds()
        # New session starts if diff is null (first event) or exceeds inactivity threshold
        df["_is_new_session"] = (df["_time_diff"].isna()) | (df["_time_diff"] > self.max_inactivity_seconds)
        df["_session_num"] = df.groupby(self.user_col)["_is_new_session"].cumsum()
        df[self.session_id_col] = df[self.user_col].astype(str) + "_s" + df["_session_num"].astype(str)

        return df.drop(columns=["_time_diff", "_is_new_session", "_session_num"])
