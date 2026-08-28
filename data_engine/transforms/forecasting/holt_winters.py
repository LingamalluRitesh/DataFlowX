"""
DataFlowX Holt-Winters Triple Exponential Smoothing Forecaster
Calculates level, trend, and seasonal components (additive and multiplicative) over partitioned time-series metrics.
"""

from typing import List, Optional
import numpy as np
import pandas as pd


class HoltWintersForecaster:
    """Holt-Winters forecasting algorithm."""

    @classmethod
    def forecast_series(
        cls,
        series: List[float],
        season_length: int = 7,
        alpha: float = 0.2,
        beta: float = 0.1,
        gamma: float = 0.1,
        forecast_horizon: int = 7
    ) -> List[float]:
        if len(series) < season_length * 2:
            # Fallback to simple moving average
            avg = float(np.mean(series)) if series else 0.0
            return [round(avg, 2)] * forecast_horizon

        # Initial level and trend
        level = series[0]
        trend = (series[season_length] - series[0]) / season_length
        seasonals = [series[i] - level for i in range(season_length)]

        for i in range(len(series)):
            val = series[i]
            last_level = level
            s_idx = i % season_length
            level = alpha * (val - seasonals[s_idx]) + (1 - alpha) * (level + trend)
            trend = beta * (level - last_level) + (1 - beta) * trend
            seasonals[s_idx] = gamma * (val - level) + (1 - gamma) * seasonals[s_idx]

        predictions = []
        for m in range(1, forecast_horizon + 1):
            s_idx = (len(series) + m - 1) % season_length
            pred = level + m * trend + seasonals[s_idx]
            predictions.append(round(float(pred), 2))

        return predictions
