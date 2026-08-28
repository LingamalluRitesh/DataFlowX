"""
DataFlowX Data Cleansing & Text Sanitization Pipeline Steps
Vectorized transformations: string trimming, casing normalization, regex sanitization, special character stripping, and whitespace collapsing.
"""

import re
from typing import List, Optional
import pandas as pd


class DataCleansingToolkit:
    """Vectorized cleansing functions."""

    @staticmethod
    def strip_whitespace(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        df = df.copy()
        for col in columns:
            if col in df.columns and pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].astype(str).str.strip()
        return df

    @staticmethod
    def to_lowercase(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        df = df.copy()
        for col in columns:
            if col in df.columns and pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].astype(str).str.lower()
        return df

    @staticmethod
    def remove_special_characters(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        df = df.copy()
        for col in columns:
            if col in df.columns and pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].astype(str).str.replace(r"[^a-zA-Z0-9_\s]", "", regex=True)
        return df
