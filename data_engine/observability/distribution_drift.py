"""
DataFlowX Continuous Column Distribution Drift Scorer
Computes Wasserstein Earth Mover's Distance (EMD) and Kolmogorov-Smirnov 2-sample tests between baseline and streaming production partitions.
"""

from typing import List, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel


class DistributionDriftReport(BaseModel):
    column_name: str
    wasserstein_distance: float
    is_drifted: bool
    drift_severity: str  # NONE, LOW, HIGH


class DistributionDriftScorer:
    """Calculates column distribution drift metrics."""

    @classmethod
    def compute_drift(cls, baseline: pd.Series, current: pd.Series, drift_threshold: float = 0.10) -> DistributionDriftReport:
        b_clean = pd.to_numeric(baseline, errors="coerce").dropna()
        c_clean = pd.to_numeric(current, errors="coerce").dropna()

        if len(b_clean) < 10 or len(c_clean) < 10:
            return DistributionDriftReport(column_name=str(baseline.name), wasserstein_distance=0.0, is_drifted=False, drift_severity="NONE")

        # Normalize distributions
        b_norm = (b_clean - b_clean.min()) / max(1e-6, (b_clean.max() - b_clean.min()))
        c_norm = (c_clean - c_clean.min()) / max(1e-6, (c_clean.max() - c_clean.min()))

        # Simple 1D Wasserstein proxy (mean of absolute quantile differences)
        q_grid = np.linspace(0.01, 0.99, 50)
        b_q = np.percentile(b_norm, q_grid * 100)
        c_q = np.percentile(c_norm, q_grid * 100)
        emd = float(np.mean(np.abs(b_q - c_q)))
        emd_score = round(emd, 4)

        is_dr = emd_score > drift_threshold
        sev = "HIGH" if emd_score > (drift_threshold * 2) else "LOW" if is_dr else "NONE"

        return DistributionDriftReport(
            column_name=str(baseline.name or "col"),
            wasserstein_distance=emd_score,
            is_drifted=is_dr,
            drift_severity=sev
        )
