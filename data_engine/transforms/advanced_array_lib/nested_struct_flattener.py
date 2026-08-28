"""
DataFlowX Vectorized Nested Struct & JSON Flattener
Flattens deeply nested JSON structures, records, and maps into dot-notated tabular columns (`user.address.city`).
"""

from typing import Any, Dict, List
import pandas as pd


class NestedStructFlattener:
    """Flattens nested dictionaries/records in DataFrames."""

    @classmethod
    def flatten_dict(cls, d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(cls.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @classmethod
    def flatten_dataframe(cls, df: pd.DataFrame, struct_column: str, sep: str = ".") -> pd.DataFrame:
        if df.empty or struct_column not in df.columns:
            return df

        flattened_records = []
        for _, row in df.iterrows():
            base_dict = row.to_dict()
            struct_val = base_dict.pop(struct_column, {})
            if isinstance(struct_val, dict):
                flat_struct = cls.flatten_dict(struct_val, parent_key=struct_column, sep=sep)
                base_dict.update(flat_struct)
            flattened_records.append(base_dict)

        return pd.DataFrame(flattened_records)
