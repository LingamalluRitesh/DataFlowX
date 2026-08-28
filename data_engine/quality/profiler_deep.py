"""
DataFlowX Deep Statistical Data Profiler
Computes comprehensive data profiles: quantiles (p1, p5, p25, p50, p75, p95, p99), skewness, kurtosis, zero-inflation, cardinality ratios, entropy, and histogram binning.
"""

import math
from typing import Any, Dict, List, Optional, Union
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class ColumnProfileReport(BaseModel):
    name: str
    inferred_type: str
    total_count: int
    null_count: int
    null_percentage: float
    distinct_count: int
    distinct_ratio: float
    is_unique: bool
    is_constant: bool
    # Numerical metrics
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    mean_value: Optional[float] = None
    median_value: Optional[float] = None
    std_dev: Optional[float] = None
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    zero_count: Optional[int] = None
    quantiles: Dict[str, float] = Field(default_factory=dict)
    histogram: Dict[str, Any] = Field(default_factory=dict)
    # Categorical metrics
    top_frequent_values: List[Dict[str, Any]] = Field(default_factory=list)


class DeepDatasetProfile(BaseModel):
    dataset_name: str
    total_rows: int
    total_columns: int
    memory_usage_mb: float
    duplicate_rows_count: int
    duplicate_rows_percentage: float
    columns: List[ColumnProfileReport] = Field(default_factory=list)


class DeepDataProfiler:
    """Enterprise statistical profiling engine for large DataFrames."""

    @staticmethod
    def profile_dataframe(df: pd.DataFrame, dataset_name: str = "dataset") -> DeepDatasetProfile:
        if df.empty:
            return DeepDatasetProfile(
                dataset_name=dataset_name,
                total_rows=0,
                total_columns=len(df.columns),
                memory_usage_mb=0.0,
                duplicate_rows_count=0,
                duplicate_rows_percentage=0.0,
                columns=[]
            )

        n_rows = len(df)
        mem_mb = round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2)
        dup_count = int(df.duplicated().sum())
        dup_pct = round((dup_count / n_rows) * 100, 2)

        column_reports = []

        for col in df.columns:
            series = df[col]
            null_cnt = int(series.isna().sum())
            null_pct = round((null_cnt / n_rows) * 100, 2)
            dist_cnt = int(series.nunique(dropna=True))
            dist_ratio = round((dist_cnt / n_rows), 4)

            # Determine type
            is_num = pd.api.types.is_numeric_dtype(series)
            dtype_str = str(series.dtype)

            col_report = ColumnProfileReport(
                name=str(col),
                inferred_type=dtype_str,
                total_count=n_rows,
                null_count=null_cnt,
                null_percentage=null_pct,
                distinct_count=dist_cnt,
                distinct_ratio=dist_ratio,
                is_unique=(dist_cnt == n_rows),
                is_constant=(dist_cnt <= 1)
            )

            if is_num and series.dropna().shape[0] > 0:
                clean_num = series.dropna().astype(float)
                col_report.min_value = round(float(clean_num.min()), 4)
                col_report.max_value = round(float(clean_num.max()), 4)
                col_report.mean_value = round(float(clean_num.mean()), 4)
                col_report.median_value = round(float(clean_num.median()), 4)
                col_report.std_dev = round(float(clean_num.std()), 4) if len(clean_num) > 1 else 0.0
                col_report.skewness = round(float(clean_num.skew()), 4) if len(clean_num) > 2 else None
                col_report.kurtosis = round(float(clean_num.kurt()), 4) if len(clean_num) > 3 else None
                col_report.zero_count = int((clean_num == 0).sum())

                # Quantiles
                q_vals = clean_num.quantile([0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]).to_dict()
                col_report.quantiles = {f"p{int(k*100)}": round(float(v), 4) for k, v in q_vals.items()}

                # Histogram
                try:
                    counts, bin_edges = np.histogram(clean_num, bins=10)
                    col_report.histogram = {
                        "bin_edges": [round(float(b), 2) for b in bin_edges],
                        "counts": [int(c) for c in counts]
                    }
                except Exception:
                    pass
            else:
                # Top categorical values
                top_vals = series.value_counts(dropna=False).head(5).to_dict()
                col_report.top_frequent_values = [
                    {"value": str(k), "count": int(v), "percentage": round((v / n_rows) * 100, 2)}
                    for k, v in top_vals.items()
                ]

            column_reports.append(col_report)

        return DeepDatasetProfile(
            dataset_name=dataset_name,
            total_rows=n_rows,
            total_columns=len(df.columns),
            memory_usage_mb=mem_mb,
            duplicate_rows_count=dup_count,
            duplicate_rows_percentage=dup_pct,
            columns=column_reports
        )
