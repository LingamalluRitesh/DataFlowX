"""
DataFlowX Autoregressive Integrated Moving Average (ARIMA) Baseline
Fits AR(p) and MA(q) parameters using least squares linear regression over differenced time-series series.
"""

from typing import List, Tuple
import numpy as np


class ARIMABaseline:
    """Lightweight AR(1) differencing model."""

    @classmethod
    def fit_and_predict(cls, series: List[float], steps_ahead: int = 5) -> List[float]:
        if len(series) < 5:
            return [round(series[-1], 2)] * steps_ahead if series else [0.0] * steps_ahead

        # 1st order differencing
        diff = np.diff(series)
        # AR(1) coefficient estimation
        x = diff[:-1]
        y = diff[1:]
        if len(x) == 0 or np.var(x) == 0:
            phi = 0.5
        else:
            phi = float(np.cov(x, y)[0, 1] / np.var(x))
            phi = max(-0.95, min(0.95, phi))

        last_val = series[-1]
        last_diff = diff[-1]
        preds = []

        for _ in range(steps_ahead):
            next_diff = phi * last_diff
            next_val = last_val + next_diff
            preds.append(round(float(next_val), 2))
            last_val = next_val
            last_diff = next_diff

        return preds
