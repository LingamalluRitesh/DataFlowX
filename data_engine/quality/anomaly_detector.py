"""
DataFlowX Time-Series Anomaly Detector & Statistical Control Charts
Implements Exponentially Weighted Moving Average (EWMA), 3-Sigma Shewhart control limits, and historical baseline anomaly scoring.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

from backend.core.logging import get_logger

logger = get_logger(__name__)


class MetricAnomalyDetector:
    """Detects unexpected volume spikes, latency degradations, or row count drops across historical pipeline runs."""

    def __init__(self, alpha: float = 0.3, num_sigmas: float = 3.0):
        self.alpha = alpha
        self.num_sigmas = num_sigmas

    def evaluate_metric_history(
        self,
        historical_values: List[float],
        current_value: float
    ) -> Dict[str, Any]:
        """
        Evaluate current metric reading against EWMA baseline.
        Returns anomaly status, z-score, expected bounds [lower_bound, upper_bound].
        """
        if len(historical_values) < 3:
            return {
                "is_anomaly": False,
                "confidence": 0.0,
                "current_value": current_value,
                "expected_mean": current_value,
                "lower_bound": current_value * 0.5,
                "upper_bound": current_value * 1.5,
                "reason": "Insufficient history for baseline"
            }

        arr = np.array(historical_values, dtype=float)
        # Compute EWMA mean
        weights = (1 - self.alpha) ** np.arange(len(arr))[::-1]
        weights /= weights.sum()
        ewma_mean = np.sum(arr * weights)
        std_dev = np.std(arr)

        if std_dev == 0 or np.isnan(std_dev):
            std_dev = max(abs(ewma_mean) * 0.05, 1.0)

        lower_bound = max(0.0, ewma_mean - (self.num_sigmas * std_dev))
        upper_bound = ewma_mean + (self.num_sigmas * std_dev)

        z_score = abs(current_value - ewma_mean) / std_dev
        is_anomaly = bool((current_value < lower_bound) or (current_value > upper_bound))

        severity = "INFO"
        if is_anomaly:
            severity = "CRITICAL" if z_score > 4.5 else "WARNING"

        return {
            "is_anomaly": is_anomaly,
            "severity": severity,
            "z_score": round(float(z_score), 2),
            "current_value": round(float(current_value), 2),
            "expected_mean": round(float(ewma_mean), 2),
            "lower_bound": round(float(lower_bound), 2),
            "upper_bound": round(float(upper_bound), 2),
            "std_dev": round(float(std_dev), 2)
        }
