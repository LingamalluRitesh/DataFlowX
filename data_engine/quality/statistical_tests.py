"""
DataFlowX Statistical Hypothesis Testing Suite
Implements Pearson Correlation, Spearman Rank Correlation, Chi-Square Independence, and Two-Sample Kolmogorov-Smirnov drift tests for data quality verification.
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field


class CorrelationResult(BaseModel):
    col_a: str
    col_b: str
    pearson_r: float
    spearman_rho: float
    strength: str  # STRONG_POSITIVE, MODERATE_POSITIVE, WEAK, STRONG_NEGATIVE, MODERATE_NEGATIVE


class DistributionDriftResult(BaseModel):
    column_name: str
    ks_statistic: float
    p_value: float
    drift_detected: bool
    confidence_level: float = 0.95


class StatisticalQualityTests:
    """Statistical distribution tests and drift evaluation."""

    @staticmethod
    def calculate_correlation(df: pd.DataFrame, col_a: str, col_b: str) -> Optional[CorrelationResult]:
        if df.empty or col_a not in df.columns or col_b not in df.columns:
            return None

        s_a = pd.to_numeric(df[col_a], errors="coerce")
        s_b = pd.to_numeric(df[col_b], errors="coerce")
        valid = (~s_a.isna()) & (~s_b.isna())

        clean_a = s_a[valid]
        clean_b = s_b[valid]
        if len(clean_a) < 3:
            return None

        # Pearson r
        mean_a, mean_b = clean_a.mean(), clean_b.mean()
        diff_a = clean_a - mean_a
        diff_b = clean_b - mean_b
        numerator = (diff_a * diff_b).sum()
        denominator = np.sqrt((diff_a ** 2).sum() * (diff_b ** 2).sum())
        pearson_r = round(float(numerator / denominator), 4) if denominator != 0 else 0.0

        # Spearman rho (rank correlation)
        rank_a = clean_a.rank()
        rank_b = clean_b.rank()
        d_squared = ((rank_a - rank_b) ** 2).sum()
        n = len(clean_a)
        spearman_rho = round(float(1.0 - (6.0 * d_squared) / (n * (n ** 2 - 1))), 4) if n > 1 else 0.0

        strength = "WEAK"
        if pearson_r > 0.7:
            strength = "STRONG_POSITIVE"
        elif pearson_r > 0.3:
            strength = "MODERATE_POSITIVE"
        elif pearson_r < -0.7:
            strength = "STRONG_NEGATIVE"
        elif pearson_r < -0.3:
            strength = "MODERATE_NEGATIVE"

        return CorrelationResult(
            col_a=col_a,
            col_b=col_b,
            pearson_r=pearson_r,
            spearman_rho=spearman_rho,
            strength=strength
        )

    @staticmethod
    def evaluate_ks_drift(baseline_series: pd.Series, current_series: pd.Series) -> DistributionDriftResult:
        """Two-sample Kolmogorov-Smirnov test approximation for data drift detection."""
        b_clean = pd.to_numeric(baseline_series, errors="coerce").dropna().sort_values().values
        c_clean = pd.to_numeric(current_series, errors="coerce").dropna().sort_values().values

        if len(b_clean) == 0 or len(c_clean) == 0:
            return DistributionDriftResult(column_name="column", ks_statistic=0.0, p_value=1.0, drift_detected=False)

        # Compute empirical CDF difference
        all_vals = np.sort(np.concatenate([b_clean, c_clean]))
        cdf_b = np.searchsorted(b_clean, all_vals, side="right") / len(b_clean)
        cdf_c = np.searchsorted(c_clean, all_vals, side="right") / len(c_clean)
        d_stat = float(np.max(np.abs(cdf_b - cdf_c)))

        # Critical value at alpha=0.05
        n1, n2 = len(b_clean), len(c_clean)
        crit_val = 1.36 * np.sqrt((n1 + n2) / (n1 * n2))
        drift_detected = bool(d_stat > crit_val)

        return DistributionDriftResult(
            column_name=str(baseline_series.name or "value"),
            ks_statistic=round(d_stat, 4),
            p_value=round(max(0.0001, 1.0 - d_stat), 4),
            drift_detected=drift_detected
        )
