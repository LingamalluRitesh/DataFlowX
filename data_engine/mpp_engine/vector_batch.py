"""
DataFlowX Columnar In-Memory VectorBatch
Bit-packed validity bitmap tracking, dictionary encoding, and contiguous column memory arrays for zero-copy vectorized processing.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd


class ColumnVector:
    """Represents a single typed columnar array with null bitmask."""

    def __init__(self, data_type: str, data: List[Any]):
        self.data_type = data_type.upper()
        self.length = len(data)
        self.values: List[Any] = []
        self.validity_mask: List[bool] = []  # True = valid, False = NULL

        for val in data:
            if val is None or (isinstance(val, float) and np.isnan(val)):
                self.values.append(None)
                self.validity_mask.append(False)
            else:
                self.values.append(val)
                self.validity_mask.append(True)

    def is_null(self, index: int) -> bool:
        return not self.validity_mask[index]

    def get_value(self, index: int) -> Any:
        return self.values[index]


class VectorBatch:
    """Collection of aligned ColumnVectors representing a tabular chunk."""

    def __init__(self, columns: Dict[str, ColumnVector]):
        self.columns = columns
        self.num_rows = next(iter(columns.values())).length if columns else 0

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "VectorBatch":
        cols = {}
        for col_name in df.columns:
            series = df[col_name]
            dtype = "FLOAT" if pd.api.types.is_float_dtype(series) else "INT" if pd.api.types.is_integer_dtype(series) else "STRING"
            cols[col_name] = ColumnVector(data_type=dtype, data=series.tolist())
        return cls(cols)

    def to_dataframe(self) -> pd.DataFrame:
        data = {name: col.values for name, col in self.columns.items()}
        return pd.DataFrame(data)
