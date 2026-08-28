"""
DataFlowX Multi-Dimensional Z-Order Curve Indexer
Computes Morton space-filling Z-curve codes by bit-interleaving multiple column coordinates to optimize spatial data locality in Parquet files.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


def interleave_bits_2d(x: int, y: int) -> int:
    """Interleave 32-bit integers into 64-bit Morton code (Z-value)."""
    x = (x | (x << 16)) & 0x0000FFFF0000FFFF
    x = (x | (x << 8)) & 0x00FF00FF00FF00FF
    x = (x | (x << 4)) & 0x0F0F0F0F0F0F0F0F
    x = (x | (x << 2)) & 0x3333333333333333
    x = (x | (x << 1)) & 0x5555555555555555

    y = (y | (y << 16)) & 0x0000FFFF0000FFFF
    y = (y | (y << 8)) & 0x00FF00FF00FF00FF
    y = (y | (y << 4)) & 0x0F0F0F0F0F0F0F0F
    y = (y | (y << 2)) & 0x3333333333333333
    y = (y | (y << 1)) & 0x5555555555555555

    return x | (y << 1)


class ZOrderIndexer:
    """Sorts DataFrame rows along Z-order space-filling curve across multiple filtering columns."""

    @staticmethod
    def apply_zorder(df: pd.DataFrame, col_x: str, col_y: str, output_col: str = "z_order_key") -> pd.DataFrame:
        if df.empty or col_x not in df.columns or col_y not in df.columns:
            return df
        df = df.copy()

        # Map to integer ranks [0, 65535]
        rank_x = (df[col_x].rank(pct=True) * 65535).fillna(0).astype(int)
        rank_y = (df[col_y].rank(pct=True) * 65535).fillna(0).astype(int)

        z_values = [interleave_bits_2d(int(rx), int(ry)) for rx, ry in zip(rank_x, rank_y)]
        df[output_col] = z_values
        return df.sort_values(by=output_col).reset_index(drop=True)
