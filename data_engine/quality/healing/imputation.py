"""
DataFlowX Automated Missing Value Imputation Engine
Applies statistical imputation strategies (Mean, Median, Mode, Forward Fill, Backward Fill, and Constant Value) to automatically repair null-polluted datasets.
"""

from typing import Any, Dict, List, Optional
import pandas as pd


class MissingValueImputer:
    """Repairs null fields in DataFrames using chosen imputation strategies."""

    @classmethod
    def impute_column(cls, df: pd.DataFrame, column_name: str, strategy: str = "MEDIAN", fill_constant: Optional[Any] = None) -> pd.DataFrame:
        if df.empty or column_name not in df.columns:
            return df
        df = df.copy()

        strat = strategy.upper()
        if strat == "MEAN":
            fill_val = df[column_name].mean()
        elif strat == "MEDIAN":
            fill_val = df[column_name].median()
        elif strat == "MODE":
            mode_series = df[column_name].mode()
            fill_val = mode_series[0] if not mode_series.empty else fill_constant
        elif strat == "FORWARD_FILL":
            df[column_name] = df[column_name].ffill()
            return df
        elif strat == "BACKWARD_FILL":
            df[column_name] = df[column_name].bfill()
            return df
        else:
            fill_val = fill_constant

        df[column_name] = df[column_name].fillna(fill_val)
        return df

    @classmethod
    def impute_dataframe(cls, df: pd.DataFrame, numeric_strategy: str = "MEAN", string_strategy: str = "CONSTANT", fill_constant: Any = "UNKNOWN") -> pd.DataFrame:
        if df.empty:
            return df
        res = df.copy()
        for col in res.columns:
            if pd.api.types.is_numeric_dtype(res[col]):
                res = cls.impute_column(res, col, strategy=numeric_strategy)
            else:
                res = cls.impute_column(res, col, strategy=string_strategy, fill_constant=fill_constant)
        return res
