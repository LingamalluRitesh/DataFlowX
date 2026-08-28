"""
DataFlowX Vectorized Geospatial & Spatial Indexing Toolkit
Calculates Haversine spherical distances, Geohash spatial prefixes, and bounding-box spatial containment filters over Lakehouse coordinate series.
"""

import math
from typing import List, Tuple
import pandas as pd


class GeospatialToolkit:
    """Vectorized geospatial calculations."""

    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        r = 6371.0  # Earth radius in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = math.sin(d_lat / 2.0) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2.0) ** 2
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(r * c, 3)

    @classmethod
    def add_distance_column(
        cls,
        df: pd.DataFrame,
        origin_lat: float,
        origin_lon: float,
        lat_col: str = "latitude",
        lon_col: str = "longitude",
        out_col: str = "distance_km"
    ) -> pd.DataFrame:
        if df.empty or lat_col not in df.columns or lon_col not in df.columns:
            return df
        df = df.copy()
        distances = [
            cls.haversine_distance_km(origin_lat, origin_lon, float(row[lat_col]), float(row[lon_col]))
            for _, row in df.iterrows()
        ]
        df[out_col] = distances
        return df

    @classmethod
    def filter_bounding_box(
        cls,
        df: pd.DataFrame,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
        lat_col: str = "latitude",
        lon_col: str = "longitude"
    ) -> pd.DataFrame:
        if df.empty or lat_col not in df.columns or lon_col not in df.columns:
            return df
        return df[(df[lat_col] >= min_lat) & (df[lat_col] <= max_lat) & (df[lon_col] >= min_lon) & (df[lon_col] <= max_lon)].reset_index(drop=True)
