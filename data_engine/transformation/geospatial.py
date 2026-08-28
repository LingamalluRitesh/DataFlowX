"""
DataFlowX Geospatial Transformation & Distance Operators
Calculates Great-Circle Haversine distance, bounding box filtering, and spatial geo-hashing.
"""

import math
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd

from backend.core.logging import get_logger
from data_engine.transformation.operators import BaseOperator

logger = get_logger(__name__)


def haversine_np(lat1: np.ndarray, lon1: np.ndarray, lat2: float, lon2: float, radius_km: float = 6371.0) -> np.ndarray:
    """Calculate Great-Circle distance using vectorized spherical trigonometry."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0)**2
    c = 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
    return radius_km * c


class HaversineDistanceOperator(BaseOperator):
    """Computes distance in kilometers between origin coordinate columns and a reference point."""

    def __init__(
        self,
        lat_col: str,
        lon_col: str,
        ref_lat: float,
        ref_lon: float,
        output_col: str = "distance_km",
        unit: str = "km"
    ):
        self.lat_col = lat_col
        self.lon_col = lon_col
        self.ref_lat = ref_lat
        self.ref_lon = ref_lon
        self.output_col = output_col
        self.radius = 6371.0 if unit == "km" else 3958.8  # miles

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.lat_col not in df.columns or self.lon_col not in df.columns:
            return df
        df = df.copy()

        lats = pd.to_numeric(df[self.lat_col], errors="coerce").values
        lons = pd.to_numeric(df[self.lon_col], errors="coerce").values

        distances = haversine_np(lats, lons, self.ref_lat, self.ref_lon, self.radius)
        df[self.output_col] = np.round(distances, 2)
        return df


class BoundingBoxFilterOperator(BaseOperator):
    """Filters records whose lat/long coordinates fall strictly within a geographic bounding box."""

    def __init__(
        self,
        lat_col: str,
        lon_col: str,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float
    ):
        self.lat_col = lat_col
        self.lon_col = lon_col
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.lat_col not in df.columns or self.lon_col not in df.columns:
            return df
        df = df.copy()

        lat = pd.to_numeric(df[self.lat_col], errors="coerce")
        lon = pd.to_numeric(df[self.lon_col], errors="coerce")

        mask = (lat >= self.min_lat) & (lat <= self.max_lat) & (lon >= self.min_lon) & (lon <= self.max_lon)
        return df[mask].reset_index(drop=True)
