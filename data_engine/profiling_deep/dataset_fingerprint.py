"""
DataFlowX Probabilistic Dataset Statistical Fingerprinter
Combines HyperLogLog distinct cardinalities, T-Digest quantiles, and null fractions into a compact binary fingerprint for dataset comparison.
"""

from typing import Any, Dict, List, Optional
import pandas as pd
from pydantic import BaseModel, Field

from data_engine.profiling_deep.hyperloglog import HyperLogLog
from data_engine.profiling_deep.t_digest import TDigest


class ColumnFingerprint(BaseModel):
    column_name: str
    data_type: str
    estimated_cardinality: int
    null_fraction: float
    p50: Optional[float] = None
    p95: Optional[float] = None
    p99: Optional[float] = None


class DatasetFingerprint(BaseModel):
    dataset_name: str
    total_row_count: int
    columns: Dict[str, ColumnFingerprint] = Field(default_factory=dict)


class DatasetFingerprinter:
    """Computes probabilistic dataset fingerprints."""

    @classmethod
    def fingerprint_dataframe(cls, df: pd.DataFrame, dataset_name: str) -> DatasetFingerprint:
        cols = {}
        for col in df.columns:
            series = df[col]
            hll = HyperLogLog(p=10)
            for v in series.dropna():
                hll.add(v)
            card = hll.estimate_cardinality()
            null_frac = round(float(series.isna().mean()), 4)

            p50, p95, p99 = None, None, None
            if pd.api.types.is_numeric_dtype(series):
                td = TDigest()
                for v in series.dropna():
                    td.add(float(v))
                p50 = td.estimate_quantile(0.50)
                p95 = td.estimate_quantile(0.95)
                p99 = td.estimate_quantile(0.99)

            dtype_str = "NUMERIC" if pd.api.types.is_numeric_dtype(series) else "STRING"
            cols[col] = ColumnFingerprint(
                column_name=col,
                data_type=dtype_str,
                estimated_cardinality=card,
                null_fraction=null_frac,
                p50=p50,
                p95=p95,
                p99=p99
            )

        return DatasetFingerprint(dataset_name=dataset_name, total_row_count=len(df), columns=cols)
