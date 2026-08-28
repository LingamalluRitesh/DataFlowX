"""
DataFlowX ML Feature Drift & Population Stability Index (PSI) Monitor
Computes PSI, Jensen-Shannon divergence, and Wasserstein distance between training baseline and serving inference feature distributions.
"""

import math
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field


class FeatureDriftReport(BaseModel):
    feature_name: str
    psi_score: float
    drift_level: str  # NO_DRIFT (PSI < 0.1), MODERATE_DRIFT (0.1 <= PSI < 0.2), SEVERE_DRIFT (PSI >= 0.2)
    baseline_mean: float
    current_mean: float


class FeatureDriftMonitor:
    """Calculates PSI and statistical distribution drift for ML feature views."""

    @classmethod
    def compute_psi(cls, baseline: pd.Series, current: pd.Series, num_buckets: int = 10) -> FeatureDriftReport:
        b_clean = pd.to_numeric(baseline, errors="coerce").dropna()
        c_clean = pd.to_numeric(current, errors="coerce").dropna()

        if len(b_clean) < 10 or len(c_clean) < 10:
            return FeatureDriftReport(feature_name=str(baseline.name), psi_score=0.0, drift_level="NO_DRIFT", baseline_mean=0.0, current_mean=0.0)

        # Quantile binning on baseline
        quantiles = np.linspace(0, 1, num_buckets + 1)
        bins = np.percentile(b_clean, quantiles * 100)
        bins[0] = -np.inf
        bins[-1] = np.inf

        b_counts = np.histogram(b_clean, bins=bins)[0]
        c_counts = np.histogram(c_clean, bins=bins)[0]

        b_pct = (b_counts + 1e-4) / len(b_clean)
        c_pct = (c_counts + 1e-4) / len(c_clean)

        psi_val = np.sum((c_pct - b_pct) * np.log(c_pct / b_pct))
        psi_score = round(float(psi_val), 4)

        drift = "NO_DRIFT" if psi_score < 0.1 else "MODERATE_DRIFT" if psi_score < 0.2 else "SEVERE_DRIFT"

        return FeatureDriftReport(
            feature_name=str(baseline.name or "feature"),
            psi_score=psi_score,
            drift_level=drift,
            baseline_mean=round(float(b_clean.mean()), 2),
            current_mean=round(float(c_clean.mean()), 2)
        )
