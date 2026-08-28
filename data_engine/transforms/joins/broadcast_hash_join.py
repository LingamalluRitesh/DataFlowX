"""
DataFlowX Vectorized Broadcast Hash Join Operator
Executes in-memory hash joins by broadcasting small dimension tables to worker memory partitions.
"""

from collections import defaultdict
from typing import Any, Dict, List, Optional
import pandas as pd


class BroadcastHashJoin:
    """In-memory vectorized hash join."""

    @classmethod
    def execute_join(
        cls,
        probe_df: pd.DataFrame,
        build_df: pd.DataFrame,
        probe_key: str,
        build_key: str,
        how: str = "inner",
        suffixes: tuple[str, str] = ("", "_dim")
    ) -> pd.DataFrame:
        if probe_df.empty or build_df.empty:
            return pd.DataFrame()

        # Build hash table: key -> list of build row dicts
        hash_table = defaultdict(list)
        build_cols = [c for c in build_df.columns if c != build_key]

        for _, row in build_df.iterrows():
            k = row[build_key]
            hash_table[k].append(row.to_dict())

        joined_records = []
        for _, p_row in probe_df.iterrows():
            p_dict = p_row.to_dict()
            p_k = p_dict.get(probe_key)
            matches = hash_table.get(p_k, [])

            if matches:
                for b_dict in matches:
                    merged = dict(p_dict)
                    for k, v in b_dict.items():
                        if k == build_key:
                            continue
                        out_k = f"{k}{suffixes[1]}" if k in merged else k
                        merged[out_k] = v
                    joined_records.append(merged)
            elif how.lower() in ("left", "outer"):
                merged = dict(p_dict)
                for c in build_cols:
                    out_c = f"{c}{suffixes[1]}" if c in merged else c
                    merged[out_c] = None
                joined_records.append(merged)

        return pd.DataFrame(joined_records)
