"""
DataFlowX 3-Dimensional Morton Space-Filling Curve (Z-Curve) Generator
Interleaves binary bits across 3 numeric/timestamp dimensions to produce 64-bit integer Morton indices for multidimensional data clustering.
"""

from typing import List, Tuple
import pandas as pd


class MortonCurve3D:
    """Computes 3D Z-order curve keys."""

    @staticmethod
    def _spread_bits(val: int) -> int:
        """Spreads the lower 21 bits of val into 63 bits (every 3rd bit)."""
        x = val & 0x1FFFFF  # 21 bits
        x = (x | (x << 32)) & 0x1F00000000FFFF
        x = (x | (x << 16)) & 0x1F0000FF0000FF
        x = (x | (x << 8)) & 0x100F00F00F00F00F
        x = (x | (x << 4)) & 0x10C30C30C30C30C3
        x = (x | (x << 2)) & 0x1249249249249249
        return x

    @classmethod
    def encode_3d(cls, x: int, y: int, z: int) -> int:
        """Interleaves bits of x, y, and z into a single 64-bit Morton code."""
        return (cls._spread_bits(x) << 2) | (cls._spread_bits(y) << 1) | cls._spread_bits(z)

    @classmethod
    def add_z_order_column(
        cls,
        df: pd.DataFrame,
        col_x: str,
        col_y: str,
        col_z: str,
        out_col: str = "z_order_index"
    ) -> pd.DataFrame:
        if df.empty or col_x not in df.columns or col_y not in df.columns or col_z not in df.columns:
            return df

        df = df.copy()
        # Rank-normalize columns to 0..2^20 integers
        rx = pd.qcut(df[col_x], q=min(len(df), 1024), labels=False, duplicates="drop").fillna(0).astype(int)
        ry = pd.qcut(df[col_y], q=min(len(df), 1024), labels=False, duplicates="drop").fillna(0).astype(int)
        rz = pd.qcut(df[col_z], q=min(len(df), 1024), labels=False, duplicates="drop").fillna(0).astype(int)

        z_codes = [cls.encode_3d(int(x), int(y), int(z)) for x, y, z in zip(rx, ry, rz)]
        df[out_col] = z_codes
        return df.sort_values(by=out_col).reset_index(drop=True)
