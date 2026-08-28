"""
DataFlowX Vectorized Complex Types (Array, Map, Struct, JSON) Library
Provides functions for manipulating embedded nested arrays, key-value maps, and JSON payloads.
"""

import json
from typing import Any, Dict, List, Optional
import pandas as pd


class ArrayMapFunctions:
    """Vectorized array, map, and json functions."""

    @staticmethod
    def array_size(series: pd.Series) -> pd.Series:
        return series.apply(lambda x: len(x) if isinstance(x, (list, tuple, set)) else (0 if pd.isna(x) else 1))

    @staticmethod
    def array_contains(series: pd.Series, element: Any) -> pd.Series:
        return series.apply(lambda x: element in x if isinstance(x, (list, tuple, set)) else False)

    @staticmethod
    def array_distinct(series: pd.Series) -> pd.Series:
        return series.apply(lambda x: list(dict.fromkeys(x)) if isinstance(x, (list, tuple)) else x)

    @staticmethod
    def array_join(series: pd.Series, delimiter: str = ",") -> pd.Series:
        return series.apply(lambda x: delimiter.join(str(i) for i in x) if isinstance(x, (list, tuple)) else str(x))

    @staticmethod
    def array_slice(series: pd.Series, start_idx: int, length: int) -> pd.Series:
        return series.apply(lambda x: x[start_idx:start_idx + length] if isinstance(x, list) else [])

    @staticmethod
    def map_keys(series: pd.Series) -> pd.Series:
        return series.apply(lambda x: list(x.keys()) if isinstance(x, dict) else [])

    @staticmethod
    def map_values(series: pd.Series) -> pd.Series:
        return series.apply(lambda x: list(x.values()) if isinstance(x, dict) else [])

    @staticmethod
    def json_extract_path(series: pd.Series, json_path: str) -> pd.Series:
        keys = json_path.strip(".").split(".")

        def _extract(val: Any) -> Any:
            if isinstance(val, str):
                try:
                    val = json.loads(val)
                except Exception:
                    return None
            curr = val
            for k in keys:
                if isinstance(curr, dict) and k in curr:
                    curr = curr[k]
                else:
                    return None
            return curr

        return series.apply(_extract)
