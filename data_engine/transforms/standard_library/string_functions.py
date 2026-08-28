"""
DataFlowX Vectorized String Standard Library
Provides 35+ high-performance vectorized string functions for string cleansing, regex parsing, and hashing.
"""

import hashlib
import re
from typing import Any, List, Optional, Union
import numpy as np
import pandas as pd


class StringFunctions:
    """Vectorized String transformation functions."""

    @staticmethod
    def concat(*series_list: pd.Series) -> pd.Series:
        if not series_list:
            return pd.Series([], dtype=str)
        res = series_list[0].astype(str)
        for s in series_list[1:]:
            res = res + s.astype(str)
        return res

    @staticmethod
    def concat_ws(separator: str, *series_list: pd.Series) -> pd.Series:
        if not series_list:
            return pd.Series([], dtype=str)
        res = series_list[0].astype(str)
        for s in series_list[1:]:
            res = res + separator + s.astype(str)
        return res

    @staticmethod
    def lower(series: pd.Series) -> pd.Series:
        return series.astype(str).str.lower()

    @staticmethod
    def upper(series: pd.Series) -> pd.Series:
        return series.astype(str).str.upper()

    @staticmethod
    def initcap(series: pd.Series) -> pd.Series:
        return series.astype(str).str.title()

    @staticmethod
    def length(series: pd.Series) -> pd.Series:
        return series.astype(str).str.len()

    @staticmethod
    def byte_length(series: pd.Series) -> pd.Series:
        return series.astype(str).apply(lambda x: len(x.encode("utf-8")))

    @staticmethod
    def substring(series: pd.Series, start: int, length: Optional[int] = None) -> pd.Series:
        # SQL 1-indexed conversion
        s_idx = max(0, start - 1)
        if length is not None:
            return series.astype(str).str.slice(s_idx, s_idx + length)
        return series.astype(str).str.slice(s_idx)

    @staticmethod
    def left(series: pd.Series, num_chars: int) -> pd.Series:
        return series.astype(str).str.slice(0, num_chars)

    @staticmethod
    def right(series: pd.Series, num_chars: int) -> pd.Series:
        return series.astype(str).str.slice(-num_chars)

    @staticmethod
    def trim(series: pd.Series) -> pd.Series:
        return series.astype(str).str.strip()

    @staticmethod
    def ltrim(series: pd.Series) -> pd.Series:
        return series.astype(str).str.lstrip()

    @staticmethod
    def rtrim(series: pd.Series) -> pd.Series:
        return series.astype(str).str.rstrip()

    @staticmethod
    def pad_left(series: pd.Series, target_len: int, pad_char: str = " ") -> pd.Series:
        return series.astype(str).str.rjust(target_len, pad_char)

    @staticmethod
    def pad_right(series: pd.Series, target_len: int, pad_char: str = " ") -> pd.Series:
        return series.astype(str).str.ljust(target_len, pad_char)

    @staticmethod
    def reverse(series: pd.Series) -> pd.Series:
        return series.astype(str).str[::-1]

    @staticmethod
    def replace(series: pd.Series, pattern: str, replacement: str) -> pd.Series:
        return series.astype(str).str.replace(pattern, replacement, regex=False)

    @staticmethod
    def regex_replace(series: pd.Series, pattern: str, replacement: str) -> pd.Series:
        return series.astype(str).str.replace(pattern, replacement, regex=True)

    @staticmethod
    def regex_extract(series: pd.Series, pattern: str, group_idx: int = 0) -> pd.Series:
        return series.astype(str).str.extract(pattern, expand=False)

    @staticmethod
    def split(series: pd.Series, delimiter: str) -> pd.Series:
        return series.astype(str).str.split(delimiter)

    @staticmethod
    def contains(series: pd.Series, substring: str, case_sensitive: bool = True) -> pd.Series:
        return series.astype(str).str.contains(substring, case=case_sensitive, regex=False)

    @staticmethod
    def starts_with(series: pd.Series, prefix: str) -> pd.Series:
        return series.astype(str).str.startswith(prefix)

    @staticmethod
    def ends_with(series: pd.Series, suffix: str) -> pd.Series:
        return series.astype(str).str.endswith(suffix)

    @staticmethod
    def md5(series: pd.Series) -> pd.Series:
        return series.astype(str).apply(lambda x: hashlib.md5(x.encode("utf-8")).hexdigest())

    @staticmethod
    def sha1(series: pd.Series) -> pd.Series:
        return series.astype(str).apply(lambda x: hashlib.sha1(x.encode("utf-8")).hexdigest())

    @staticmethod
    def sha256(series: pd.Series) -> pd.Series:
        return series.astype(str).apply(lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest())

    @staticmethod
    def mask_middle(series: pd.Series, unmasked_start: int = 2, unmasked_end: int = 2, mask_char: str = "*") -> pd.Series:
        def _mask(val: str) -> str:
            if len(val) <= (unmasked_start + unmasked_end):
                return mask_char * len(val)
            middle_count = len(val) - unmasked_start - unmasked_end
            return val[:unmasked_start] + (mask_char * middle_count) + val[-unmasked_end:]

        return series.astype(str).apply(_mask)
