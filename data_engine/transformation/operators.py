"""
DataFlowX Transformation Operators Suite
Provides high-performance vectorized transformation operators using Pandas, PyArrow, and DuckDB.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re
import sqlite3
from typing import Any, Callable, Dict, List, Optional, Union
import numpy as np
import pandas as pd

try:
    import duckdb
except Exception:
    duckdb = None
from backend.core.exceptions import ValidationError
from backend.core.logging import get_logger

logger = get_logger(__name__)


class BaseOperator(ABC):
    """Base interface for all data transformation operators."""

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply transformation on incoming DataFrame."""
        pass


class SelectColumnsOperator(BaseOperator):
    """Select specific subset of columns."""

    def __init__(self, columns: List[str]):
        self.columns = columns

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        existing = [c for c in self.columns if c in df.columns]
        return df[existing]


class RenameColumnsOperator(BaseOperator):
    """Rename columns mapping old name -> new name."""

    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns=self.mapping)


class DropColumnsOperator(BaseOperator):
    """Drop specified columns from DataFrame."""

    def __init__(self, columns: List[str]):
        self.columns = columns

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        cols_to_drop = [c for c in self.columns if c in df.columns]
        return df.drop(columns=cols_to_drop)


class CastColumnsOperator(BaseOperator):
    """Cast column data types (int, float, str, datetime, bool)."""

    def __init__(self, type_mapping: Dict[str, str]):
        self.type_mapping = type_mapping

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col, dtype in self.type_mapping.items():
            if col in df.columns:
                try:
                    if dtype.lower() in ("datetime", "timestamp"):
                        df[col] = pd.to_datetime(df[col])
                    else:
                        df[col] = df[col].astype(dtype)
                except Exception as exc:
                    logger.warning(f"Could not cast column '{col}' to {dtype}: {exc}")
        return df


CastTypesOperator = CastColumnsOperator


class CastDataTypesOperator(BaseOperator):
    """Cast column data types (string, int64, float64, boolean, datetime)."""

    def __init__(self, type_mapping: Dict[str, str]):
        self.type_mapping = type_mapping

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        for col, target_type in self.type_mapping.items():
            if col not in df_out.columns:
                continue

            t_norm = target_type.lower()
            try:
                if t_norm in ("int", "int64", "integer"):
                    df_out[col] = pd.to_numeric(df_out[col], errors="coerce").fillna(0).astype("int64")
                elif t_norm in ("float", "float64", "double", "numeric"):
                    df_out[col] = pd.to_numeric(df_out[col], errors="coerce")
                elif t_norm in ("str", "string", "varchar", "text"):
                    df_out[col] = df_out[col].astype(str).replace("nan", "")
                elif t_norm in ("bool", "boolean"):
                    df_out[col] = df_out[col].map({True: True, "True": True, "true": True, "1": True, 1: True, False: False, "False": False, "false": False, "0": False, 0: False})
                elif t_norm in ("datetime", "timestamp", "date"):
                    df_out[col] = pd.to_datetime(df_out[col], errors="coerce")
            except Exception as exc:
                logger.warning(f"Could not cast column '{col}' to '{target_type}': {exc}")
        return df_out


class FilterRowsOperator(BaseOperator):
    """Filter rows matching a condition or predicate."""

    def __init__(self, condition_expr: str):
        self.condition_expr = condition_expr

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self.condition_expr or df.empty:
            return df

        if duckdb is not None:
            try:
                con = duckdb.connect(database=":memory:")
                con.register("input_data", df)
                query = f"SELECT * FROM input_data WHERE {self.condition_expr}"
                res_df = con.execute(query).df()
                con.close()
                return res_df
            except Exception:
                pass

        # Fallback to sqlite3 in-memory
        try:
            con = sqlite3.connect(":memory:")
            df.to_sql("input_data", con, index=False)
            res_df = pd.read_sql_query(f"SELECT * FROM input_data WHERE {self.condition_expr}", con)
            con.close()
            return res_df
        except Exception:
            try:
                return df.query(self.condition_expr)
            except Exception as exc:
                raise ValidationError(f"Invalid filter expression: {self.condition_expr}")


class DeduplicateOperator(BaseOperator):
    """Remove duplicate rows based on subset keys."""

    def __init__(self, subset: Optional[List[str]] = None, keep: str = "first"):
        self.subset = subset
        self.keep = keep  # 'first', 'last', False

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        valid_subset = [c for c in self.subset if c in df.columns] if self.subset else None
        return df.drop_duplicates(subset=valid_subset, keep=self.keep)


class NormalizeStringsOperator(BaseOperator):
    """Normalize string columns: strip whitespace, lowercase/uppercase/titlecase, regex clean."""

    def __init__(
        self,
        columns: List[str],
        case_mode: Optional[str] = None,  # 'lower', 'upper', 'title', 'capitalize'
        strip_whitespace: bool = True,
        remove_special_chars: bool = False,
    ):
        self.columns = columns
        self.case_mode = case_mode
        self.strip_whitespace = strip_whitespace
        self.remove_special_chars = remove_special_chars

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        for col in self.columns:
            if col not in df_out.columns:
                continue

            series = df_out[col].astype(str)
            if self.strip_whitespace:
                series = series.str.strip()

            if self.case_mode == "lower":
                series = series.str.lower()
            elif self.case_mode == "upper":
                series = series.str.upper()
            elif self.case_mode == "title":
                series = series.str.title()
            elif self.case_mode == "capitalize":
                series = series.str.capitalize()

            if self.remove_special_chars:
                series = series.apply(lambda x: re.sub(r"[^a-zA-Z0-9\s]", "", str(x)))

            df_out[col] = series
        return df_out


class FillMissingOperator(BaseOperator):
    """Fill NaN / null values with fixed constants or statistical values (mean, median, mode)."""

    def __init__(self, strategies: Dict[str, Union[Any, str]]):
        self.strategies = strategies  # {'col1': 0, 'col2': 'unknown', 'age': 'mean'}

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        for col, strategy in self.strategies.items():
            if col not in df_out.columns:
                continue

            if strategy == "mean" and pd.api.types.is_numeric_dtype(df_out[col]):
                df_out[col] = df_out[col].fillna(df_out[col].mean())
            elif strategy == "median" and pd.api.types.is_numeric_dtype(df_out[col]):
                df_out[col] = df_out[col].fillna(df_out[col].median())
            elif strategy == "mode":
                mode_val = df_out[col].mode()
                if not mode_val.empty:
                    df_out[col] = df_out[col].fillna(mode_val.iloc[0])
            elif strategy == "ffill":
                df_out[col] = df_out[col].ffill()
            elif strategy == "bfill":
                df_out[col] = df_out[col].bfill()
            else:
                df_out[col] = df_out[col].fillna(strategy)
        return df_out


class CalculatedColumnOperator(BaseOperator):
    """Compute new column using math expression or string concatenation."""

    def __init__(self, new_column_name: str, expression: str):
        self.new_column_name = new_column_name
        self.expression = expression

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if duckdb is not None:
            try:
                con = duckdb.connect(database=":memory:")
                con.register("input_data", df)
                query = f"SELECT *, ({self.expression}) AS {self.new_column_name} FROM input_data"
                res_df = con.execute(query).df()
                con.close()
                return res_df
            except Exception:
                pass

        # SQLite fallback
        con = sqlite3.connect(":memory:")
        df.to_sql("input_data", con, index=False)
        query = f"SELECT *, ({self.expression}) AS {self.new_column_name} FROM input_data"
        res_df = pd.read_sql_query(query, con)
        con.close()
        return res_df


class ConditionalColumnOperator(BaseOperator):
    """Compute new column based on CASE-WHEN logic."""

    def __init__(
        self,
        new_column_name: str,
        conditions: List[Dict[str, Any]],  # [{'when': 'age < 18', 'then': 'Minor'}, ...]
        else_value: Any = "Other"
    ):
        self.new_column_name = new_column_name
        self.conditions = conditions
        self.else_value = else_value

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        case_clauses = []
        for c in self.conditions:
            when_expr = c.get("when")
            then_val = c.get("then")
            then_repr = f"'{then_val}'" if isinstance(then_val, str) else str(then_val)
            case_clauses.append(f"WHEN {when_expr} THEN {then_repr}")

        else_repr = f"'{self.else_value}'" if isinstance(self.else_value, str) else str(self.else_value)
        sql_case = f"CASE {' '.join(case_clauses)} ELSE {else_repr} END"

        if duckdb is not None:
            try:
                con = duckdb.connect(database=":memory:")
                con.register("input_data", df)
                query = f"SELECT *, ({sql_case}) AS {self.new_column_name} FROM input_data"
                res_df = con.execute(query).df()
                con.close()
                return res_df
            except Exception:
                pass

        # SQLite fallback
        con = sqlite3.connect(":memory:")
        df.to_sql("input_data", con, index=False)
        query = f"SELECT *, ({sql_case}) AS {self.new_column_name} FROM input_data"
        res_df = pd.read_sql_query(query, con)
        con.close()
        return res_df


class AggregateOperator(BaseOperator):
    """Group by keys and aggregate measures."""

    def __init__(
        self,
        group_by: List[str],
        aggregations: Dict[str, Union[str, List[str]]],  # {'amount': ['sum', 'avg', 'count'], 'user_id': 'count'}
    ):
        self.group_by = group_by
        self.aggregations = aggregations

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        valid_gb = [c for c in self.group_by if c in df.columns]
        if not valid_gb or df.empty:
            return df

        agg_dict = {}
        for col, funcs in self.aggregations.items():
            if col in df.columns:
                agg_dict[col] = funcs

        df_agg = df.groupby(valid_gb).agg(agg_dict)
        # Flatten multi-level column names
        if isinstance(df_agg.columns, pd.MultiIndex):
            df_agg.columns = [f"{c[0]}_{c[1]}" for c in df_agg.columns]
        return df_agg.reset_index()


class SortOperator(BaseOperator):
    """Sort DataFrame by columns ascending/descending."""

    def __init__(self, by: List[str], ascending: Union[bool, List[bool]] = True):
        self.by = by
        self.ascending = ascending

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        valid_by = [c for c in self.by if c in df.columns]
        if not valid_by:
            return df
        return df.sort_values(by=valid_by, ascending=self.ascending)


class JoinOperator(BaseOperator):
    """Join primary DataFrame with a secondary DataFrame."""

    def __init__(
        self,
        right_df: pd.DataFrame,
        on: Optional[Union[str, List[str]]] = None,
        left_on: Optional[Union[str, List[str]]] = None,
        right_on: Optional[Union[str, List[str]]] = None,
        how: str = "inner",  # 'inner', 'left', 'right', 'outer'
        suffixes: tuple = ("_left", "_right"),
    ):
        self.right_df = right_df
        self.on = on
        self.left_on = left_on
        self.right_on = right_on
        self.how = how
        self.suffixes = suffixes

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.merge(
            df,
            self.right_df,
            on=self.on,
            left_on=self.left_on,
            right_on=self.right_on,
            how=self.how,
            suffixes=self.suffixes
        )


JoinDataFramesOperator = JoinOperator
SortRowsOperator = SortOperator
CastTypesOperator = CastColumnsOperator
