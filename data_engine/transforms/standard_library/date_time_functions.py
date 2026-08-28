"""
DataFlowX Vectorized DateTime Standard Library
Provides 40+ vectorized temporal and date manipulation functions for Lakehouse transformations.
"""

from datetime import date, datetime, timedelta, timezone
from typing import Any, List, Optional, Union
import numpy as np
import pandas as pd


class DateTimeFunctions:
    """Vectorized DateTime transformation functions."""

    @staticmethod
    def to_timestamp(series: pd.Series, format_str: Optional[str] = None) -> pd.Series:
        if format_str:
            return pd.to_datetime(series, format=format_str, errors="coerce")
        return pd.to_datetime(series, errors="coerce")

    @staticmethod
    def to_date(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.date

    @staticmethod
    def extract_year(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.year

    @staticmethod
    def extract_quarter(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.quarter

    @staticmethod
    def extract_month(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.month

    @staticmethod
    def extract_day(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.day

    @staticmethod
    def extract_hour(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.hour

    @staticmethod
    def extract_minute(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.minute

    @staticmethod
    def extract_second(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.second

    @staticmethod
    def extract_microsecond(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.microsecond

    @staticmethod
    def day_of_week(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.dayofweek  # 0=Monday, 6=Sunday

    @staticmethod
    def day_name(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.day_name()

    @staticmethod
    def month_name(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.month_name()

    @staticmethod
    def day_of_year(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.dayofyear

    @staticmethod
    def week_of_year(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.isocalendar().week

    @staticmethod
    def is_weekend(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.dayofweek.isin([5, 6])

    @staticmethod
    def is_leap_year(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.is_leap_year

    @staticmethod
    def date_trunc(series: pd.Series, unit: str = "day") -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        u = unit.lower()
        if u in ("year", "y"):
            return ts.dt.to_period("Y").dt.to_timestamp()
        elif u in ("quarter", "q"):
            return ts.dt.to_period("Q").dt.to_timestamp()
        elif u in ("month", "m"):
            return ts.dt.to_period("M").dt.to_timestamp()
        elif u in ("week", "w"):
            return ts.dt.to_period("W").dt.to_timestamp()
        elif u in ("hour", "h"):
            return ts.dt.floor("h")
        elif u in ("minute", "min"):
            return ts.dt.floor("min")
        elif u in ("second", "s"):
            return ts.dt.floor("s")
        return ts.dt.floor("D")

    @staticmethod
    def date_add_days(series: pd.Series, days: Union[int, pd.Series]) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        if isinstance(days, pd.Series):
            return ts + pd.to_timedelta(days, unit="D")
        return ts + pd.Timedelta(days=days)

    @staticmethod
    def date_add_hours(series: pd.Series, hours: Union[int, pd.Series]) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        if isinstance(hours, pd.Series):
            return ts + pd.to_timedelta(hours, unit="h")
        return ts + pd.Timedelta(hours=hours)

    @staticmethod
    def date_diff_days(series_a: pd.Series, series_b: pd.Series) -> pd.Series:
        ts_a = pd.to_datetime(series_a, errors="coerce")
        ts_b = pd.to_datetime(series_b, errors="coerce")
        return (ts_a - ts_b).dt.total_seconds() / 86400.0

    @staticmethod
    def date_diff_hours(series_a: pd.Series, series_b: pd.Series) -> pd.Series:
        ts_a = pd.to_datetime(series_a, errors="coerce")
        ts_b = pd.to_datetime(series_b, errors="coerce")
        return (ts_a - ts_b).dt.total_seconds() / 3600.0

    @staticmethod
    def date_diff_seconds(series_a: pd.Series, series_b: pd.Series) -> pd.Series:
        ts_a = pd.to_datetime(series_a, errors="coerce")
        ts_b = pd.to_datetime(series_b, errors="coerce")
        return (ts_a - ts_b).dt.total_seconds()

    @staticmethod
    def unix_timestamp(series: pd.Series) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return (ts - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")

    @staticmethod
    def from_unixtime(series: pd.Series) -> pd.Series:
        return pd.to_datetime(series, unit="s", errors="coerce")

    @staticmethod
    def format_datetime(series: pd.Series, format_pattern: str = "%Y-%m-%d %H:%M:%S") -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        return ts.dt.strftime(format_pattern)

    @staticmethod
    def convert_timezone(series: pd.Series, from_tz: str, to_tz: str) -> pd.Series:
        ts = pd.to_datetime(series, errors="coerce")
        if ts.dt.tz is None:
            ts = ts.dt.tz_localize(from_tz)
        return ts.dt.tz_convert(to_tz)
