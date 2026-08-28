"""
DataFlowX Multi-Dimensional Z-Order Space-Filling Curve Compactor
Interleaves bits across multiple numerical dimensions (e.g. latitude, longitude, price) to preserve multi-dimensional data locality for fast skipping.
"""

from typing import List
import pandas as pd


class ZOrderCompactor:
    """Interleaves multi-column coordinate bits to compute Z-values."""

    @staticmethod
    def interleave_bits_2d(x: int, y: int) -> int:
        """Interleaves two 16-bit integers into a single 32-bit Morton Z-value."""
        z = 0
        for i in range(16):
            z |= ((x >> i) & 1) << (2 * i)
            z |= ((y >> i) & 1) << (2 * i + 1)
        return z

    @classmethod
    def apply_zorder_sort(cls, df: pd.DataFrame, col_x: str, col_y: str) -> pd.DataFrame:
        if df.empty or col_x not in df.columns or col_y not in df.columns:
            return df
        df = df.copy()
        x_norm = pd.to_numeric(df[col_x], errors="coerce").fillna(0).astype(int) & 0xFFFF
        y_norm = pd.to_numeric(df[col_y], errors="coerce").fillna(0).astype(int) & 0xFFFF

        z_vals = [cls.interleave_bits_2d(x, y) for x, y in zip(x_norm, y_norm)]
        df["_z_order_val"] = z_vals
        sorted_df = df.sort_values(by="_z_order_val").drop(columns=["_z_order_val"]).reset_index(drop=True)
        return sorted_df
