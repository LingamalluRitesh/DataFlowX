"""
DataFlowX Reshaping, Pivoting & Wide-to-Long Unpivoting Operators
Transforms row-oriented records into wide cross-tabs (Pivot) and normalized narrow records (Melt/Unpivot).
"""

from typing import Any, Dict, List, Optional, Union
import pandas as pd

from backend.core.logging import get_logger
from data_engine.transformation.operators import BaseOperator

logger = get_logger(__name__)


class PivotTableOperator(BaseOperator):
    """Pivots DataFrame from narrow key-value format to wide summary matrix."""

    def __init__(
        self,
        index_columns: List[str],
        pivot_column: str,
        value_column: str,
        aggfunc: str = "sum",
        fill_value: Any = 0
    ):
        self.index_columns = index_columns
        self.pivot_column = pivot_column
        self.value_column = value_column
        self.aggfunc = aggfunc
        self.fill_value = fill_value

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.pivot_column not in df.columns or self.value_column not in df.columns:
            return df
        valid_idx = [c for c in self.index_columns if c in df.columns]
        if not valid_idx:
            return df

        pivoted = df.pivot_table(
            index=valid_idx,
            columns=self.pivot_column,
            values=self.value_column,
            aggfunc=self.aggfunc,
            fill_value=self.fill_value
        )
        # Flatten column names
        pivoted.columns = [f"{self.pivot_column}_{c}" for c in pivoted.columns]
        return pivoted.reset_index()


class UnpivotMeltOperator(BaseOperator):
    """Unpivots wide DataFrame into normalized long format (id_vars, variable, value)."""

    def __init__(
        self,
        id_vars: List[str],
        value_vars: List[str],
        var_name: str = "metric_name",
        value_name: str = "metric_value"
    ):
        self.id_vars = id_vars
        self.value_vars = value_vars
        self.var_name = var_name
        self.value_name = value_name

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        valid_ids = [c for c in self.id_vars if c in df.columns]
        valid_vals = [c for c in self.value_vars if c in df.columns]
        if not valid_vals:
            return df

        return pd.melt(
            df,
            id_vars=valid_ids,
            value_vars=valid_vals,
            var_name=self.var_name,
            value_name=self.value_name
        )
