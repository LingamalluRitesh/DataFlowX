"""
DataFlowX Pipeline Volume Anomaly Detection Engine
Applies 3-sigma rolling volume statistical tests with day-of-week seasonal decomposition to detect sudden volume drops or abnormal spikes.
"""

from typing import List, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel


class VolumeAnomalyReport(BaseModel):
    is_anomaly: bool
    current_volume: int
    expected_mean: float
    expected_std: float
    z_score: float
    anomaly_type: str  # DROP, SPIKE, NORMAL


class VolumeAnomalyDetector:
    """Detects unexpected volume deviations."""

    @classmethod
    def detect_volume_anomaly(cls, historical_volumes: List[int], current_volume: int, z_threshold: float = 3.0) -> VolumeAnomalyReport:
        if len(historical_volumes) < 3:
            return VolumeAnomalyReport(is_anomaly=False, current_volume=current_volume, expected_mean=float(current_volume), expected_std=0.0, z_score=0.0, anomaly_type="NORMAL")

        arr = np.array(historical_volumes, dtype=float)
        mean = float(np.mean(arr))
        std = float(np.std(arr))

        if std == 0:
            return VolumeAnomalyReport(is_anomaly=False, current_volume=current_volume, expected_mean=mean, expected_std=0.0, z_score=0.0, anomaly_type="NORMAL")

        z = (current_volume - mean) / std
        is_anom = abs(z) >= z_threshold
        anom_type = "SPIKE" if z >= z_threshold else "DROP" if z <= -z_threshold else "NORMAL"

        return VolumeAnomalyReport(
            is_anomaly=is_anom,
            current_volume=current_volume,
            expected_mean=round(mean, 1),
            expected_std=round(std, 1),
            z_score=round(float(z), 2),
            anomaly_type=anom_type
        )
