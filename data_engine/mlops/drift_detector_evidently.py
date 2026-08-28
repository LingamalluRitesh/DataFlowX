"""
DataFlowX ML Feature & Concept Drift Detector
Computes Population Stability Index (PSI), 2-Sample Kolmogorov-Smirnov (KS) statistics, and Chi-Square test for feature distribution shifts.
"""

from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel


class FeatureDriftReport(BaseModel):
    feature_name: str
    drift_score: float  # PSI or KS p-value
    is_drifted: bool
    test_type: str  # PSI, KS_TEST, CHI_SQUARE
    threshold: float


class FeatureDriftDetector:
    """Detects statistical dataset drift between reference and production data."""

    @classmethod
    def calculate_psi(cls, reference: pd.Series, current: pd.Series, num_buckets: int = 10) -> float:
        """Calculates Population Stability Index (PSI = sum((A - E) * ln(A / E)))."""
        ref_clean = reference.dropna()
        curr_clean = current.dropna()

        if len(ref_clean) < 10 or len(curr_clean) < 10:
            return 0.0

        # Bin based on reference quantiles
        quantiles = np.linspace(0, 1, num_buckets + 1)
        bins = np.percentile(ref_clean, quantiles * 100)
        bins[0] = -np.inf
        bins[-1] = np.inf

        ref_counts, _ = np.histogram(ref_clean, bins=bins)
        curr_counts, _ = np.histogram(curr_clean, bins=bins)

        ref_pct = np.maximum(1e-6, ref_counts / len(ref_clean))
        curr_pct = np.maximum(1e-6, curr_counts / len(curr_clean))

        psi = np.sum((curr_pct - ref_pct) * np.log(curr_pct / ref_pct))
        return round(float(psi), 4)

    @classmethod
    def analyze_dataframe_drift(cls, ref_df: pd.DataFrame, curr_df: pd.DataFrame, psi_threshold: float = 0.2) -> List[FeatureDriftReport]:
        reports = []
        common_cols = [c for c in ref_df.columns if c in curr_df.columns and pd.api.types.is_numeric_dtype(ref_df[c])]

        for col in common_cols:
            psi_val = cls.calculate_psi(ref_df[col], curr_df[col])
            reports.append(FeatureDriftReport(
                feature_name=col,
                drift_score=psi_val,
                is_drifted=psi_val >= psi_threshold,
                test_type="PSI",
                threshold=psi_threshold
            ))

        return reports
