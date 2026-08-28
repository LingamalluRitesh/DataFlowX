"""
DataFlowX Automated Dataset Profiling Engine
Calculates comprehensive column-level statistics, distributions, cardinalities, null percentages, and memory footprints.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from backend.core.logging import get_logger

logger = get_logger(__name__)


class ColumnProfile(BaseModel):
    column_name: str
    data_type: str
    total_count: int
    null_count: int
    null_percentage: float
    distinct_count: int
    unique_percentage: float
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    mean_value: Optional[float] = None
    median_value: Optional[float] = None
    std_dev: Optional[float] = None
    top_frequent_values: List[Dict[str, Any]] = Field(default_factory=list)


class DatasetProfileReport(BaseModel):
    total_rows: int
    total_columns: int
    null_cells: int
    null_percentage_overall: float
    duplicate_rows: int
    memory_bytes: int
    columns: List[ColumnProfile] = Field(default_factory=list)


class DataProfiler:
    """Enterprise statistical profiling engine."""

    @staticmethod
    def profile_dataframe(df: pd.DataFrame) -> DatasetProfileReport:
        total_rows = len(df)
        total_columns = len(df.columns)

        if total_rows == 0:
            return DatasetProfileReport(
                total_rows=0,
                total_columns=total_columns,
                null_cells=0,
                null_percentage_overall=0.0,
                duplicate_rows=0,
                memory_bytes=0,
                columns=[]
            )

        null_cells = int(df.isnull().sum().sum())
        total_cells = total_rows * total_columns
        null_pct_overall = (null_cells / total_cells * 100.0) if total_cells > 0 else 0.0
        duplicate_rows = int(df.duplicated().sum())
        memory_bytes = int(df.memory_usage(deep=True).sum())

        col_profiles: List[ColumnProfile] = []

        for col in df.columns:
            series = df[col]
            null_count = int(series.isnull().sum())
            null_pct = round((null_count / total_rows * 100.0), 2)

            non_null_series = series.dropna()
            distinct_count = int(non_null_series.nunique())
            unique_pct = round((distinct_count / total_rows * 100.0), 2) if total_rows > 0 else 0.0

            dtype_str = str(series.dtype)
            min_val = None
            max_val = None
            mean_val = None
            median_val = None
            std_val = None

            # Numeric computations
            if pd.api.types.is_numeric_dtype(series) and not non_null_series.empty:
                min_val = float(non_null_series.min()) if not np.isnan(non_null_series.min()) else None
                max_val = float(non_null_series.max()) if not np.isnan(non_null_series.max()) else None
                mean_val = round(float(non_null_series.mean()), 4) if not np.isnan(non_null_series.mean()) else None
                median_val = round(float(non_null_series.median()), 4) if not np.isnan(non_null_series.median()) else None
                std_val = round(float(non_null_series.std()), 4) if len(non_null_series) > 1 and not np.isnan(non_null_series.std()) else 0.0
            elif pd.api.types.is_datetime64_any_dtype(series) and not non_null_series.empty:
                min_val = str(non_null_series.min())
                max_val = str(non_null_series.max())
            elif not non_null_series.empty:
                # String / Categorical min/max
                try:
                    min_val = str(non_null_series.min())[:50]
                    max_val = str(non_null_series.max())[:50]
                except Exception:
                    pass

            # Top frequent values
            top_vals = []
            if not non_null_series.empty:
                vc = non_null_series.value_counts().head(5)
                for val, count in vc.items():
                    top_vals.append({
                        "value": str(val)[:100],
                        "count": int(count),
                        "percentage": round(count / total_rows * 100.0, 2)
                    })

            col_profiles.append(ColumnProfile(
                column_name=str(col),
                data_type=dtype_str,
                total_count=total_rows,
                null_count=null_count,
                null_percentage=null_pct,
                distinct_count=distinct_count,
                unique_percentage=unique_pct,
                min_value=min_val,
                max_value=max_val,
                mean_value=mean_val,
                median_value=median_val,
                std_dev=std_val,
                top_frequent_values=top_vals
            ))

        return DatasetProfileReport(
            total_rows=total_rows,
            total_columns=total_columns,
            null_cells=null_cells,
            null_percentage_overall=round(null_pct_overall, 2),
            duplicate_rows=duplicate_rows,
            memory_bytes=memory_bytes,
            columns=col_profiles
        )
