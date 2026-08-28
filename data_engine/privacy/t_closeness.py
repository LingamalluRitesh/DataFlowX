"""
DataFlowX T-Closeness Privacy Engine
Computes Earth Mover's Distance (EMD) between group sensitive attribute distributions and the global population distribution to prevent attribute disclosure.
"""

from typing import List
import numpy as np
import pandas as pd
from pydantic import BaseModel


class TClosenessReport(BaseModel):
    is_t_close: bool
    t_threshold: float
    max_observed_emd: float


class TClosenessEngine:
    """Calculates Earth Mover's Distance for t-closeness verification."""

    @classmethod
    def evaluate_t_closeness(cls, df: pd.DataFrame, quasi_identifiers: List[str], sensitive_column: str, t_threshold: float = 0.15) -> TClosenessReport:
        if df.empty or not quasi_identifiers or sensitive_column not in df.columns:
            return TClosenessReport(is_t_close=True, t_threshold=t_threshold, max_observed_emd=0.0)

        global_dist = df[sensitive_column].value_counts(normalize=True)
        categories = list(global_dist.index)
        global_probs = np.array([global_dist[cat] for cat in categories])

        max_emd = 0.0
        for _, group in df.groupby(quasi_identifiers):
            grp_dist = group[sensitive_column].value_counts(normalize=True)
            grp_probs = np.array([grp_dist.get(cat, 0.0) for cat in categories])
            # Total variation distance as standard categorical EMD metric
            emd = 0.5 * np.sum(np.abs(grp_probs - global_probs))
            max_emd = max(max_emd, float(emd))

        return TClosenessReport(
            is_t_close=max_emd <= t_threshold,
            t_threshold=t_threshold,
            max_observed_emd=round(max_emd, 4)
        )
