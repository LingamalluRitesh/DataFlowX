"""
DataFlowX Deep JSON & Semi-Structured Document Flattener
Recursively flattens deeply nested JSON structures, explodes arrays into relational rows, and standardizes field keys.
"""

import json
from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd

from backend.core.logging import get_logger
from data_engine.transformation.operators import BaseOperator

logger = get_logger(__name__)


def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = "_") -> Dict[str, Any]:
    """Recursively flatten nested dictionary using custom separator."""
    items: List[Tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class DeepJSONFlattenerOperator(BaseOperator):
    """Parses and flattens nested JSON strings or dictionary columns into discrete tabular columns."""

    def __init__(self, json_column: str, separator: str = "_", drop_original: bool = True):
        self.json_column = json_column
        self.separator = separator
        self.drop_original = drop_original

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.json_column not in df.columns:
            return df
        df = df.copy()

        def parse_and_flatten(val: Any) -> Dict[str, Any]:
            if not val or pd.isna(val):
                return {}
            if isinstance(val, str):
                try:
                    parsed = json.loads(val)
                    if isinstance(parsed, dict):
                        return flatten_dict(parsed, parent_key=self.json_column, sep=self.separator)
                except Exception:
                    return {}
            elif isinstance(val, dict):
                return flatten_dict(val, parent_key=self.json_column, sep=self.separator)
            return {}

        flattened_records = df[self.json_column].apply(parse_and_flatten).tolist()
        df_flat = pd.DataFrame(flattened_records, index=df.index)

        if self.drop_original:
            df = df.drop(columns=[self.json_column])
        return pd.concat([df, df_flat], axis=1)


class ArrayExplodeOperator(BaseOperator):
    """Explodes JSON array or list column into individual rows (1-to-many relationship)."""

    def __init__(self, array_column: str, preserve_nulls: bool = True):
        self.array_column = array_column
        self.preserve_nulls = preserve_nulls

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.array_column not in df.columns:
            return df
        df = df.copy()

        def to_list(val: Any) -> List[Any]:
            if not val or pd.isna(val):
                return [] if not self.preserve_nulls else [None]
            if isinstance(val, list):
                return val
            if isinstance(val, str):
                try:
                    parsed = json.loads(val)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    return [val]
            return [val]

        df[self.array_column] = df[self.array_column].apply(to_list)
        return df.explode(self.array_column, ignore_index=True)
