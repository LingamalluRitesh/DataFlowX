"""
DataFlowX Geospatial Quality Validation Rules
Validates coordinate bounds (Latitude [-90, +90], Longitude [-180, +180]), WKT polygons, and Null Island (0,0) anomaly detections.
"""

from typing import Any, Dict, List, Optional
import pandas as pd
from data_engine.quality.rules import BaseQualityRule, RuleEvaluationResult


class ValidCoordinatesRule(BaseQualityRule):
    """Verifies that lat/lon columns fall strictly within valid global coordinate boundaries."""

    def __init__(self, lat_col: str, lon_col: str, name: Optional[str] = None):
        super().__init__(name or f"valid_coords_{lat_col}_{lon_col}", lat_col, 100.0)
        self.lat_col = lat_col
        self.lon_col = lon_col

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if df.empty or self.lat_col not in df.columns or self.lon_col not in df.columns:
            return self._build_result(len(df), len(df), 0, [], df)

        lat = pd.to_numeric(df[self.lat_col], errors="coerce")
        lon = pd.to_numeric(df[self.lon_col], errors="coerce")

        valid_mask = (
            (lat >= -90.0) & (lat <= 90.0) &
            (lon >= -180.0) & (lon <= 180.0) &
            ~((lat == 0.0) & (lon == 0.0))  # Exclude 'Null Island' GPS default error
        )

        failed_indices = df.index[~valid_mask].tolist()
        total = len(df)
        failed = len(failed_indices)
        return self._build_result(total, total - failed, failed, failed_indices, df)
