"""
DataFlowX K-Anonymity Generalization & Suppression Engine
Verifies and transforms quasi-identifier attributes (Age, Gender, ZipCode) such that each equivalence class contains at least k distinct individuals.
"""

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from pydantic import BaseModel, Field


class KAnonymityReport(BaseModel):
    is_k_anonymous: bool
    k_value: int
    min_equivalence_class_size: int
    violating_groups_count: int
    suppressed_rows_count: int = 0


class KAnonymityEngine:
    """Evaluates and enforces k-anonymity over quasi-identifiers."""

    @classmethod
    def evaluate_k_anonymity(cls, df: pd.DataFrame, quasi_identifiers: List[str], target_k: int = 5) -> KAnonymityReport:
        if df.empty or not quasi_identifiers:
            return KAnonymityReport(is_k_anonymous=True, k_value=target_k, min_equivalence_class_size=len(df), violating_groups_count=0)

        group_counts = df.groupby(quasi_identifiers, as_index=False).size()
        min_size = int(group_counts["size"].min()) if not group_counts.empty else 0
        violations = group_counts[group_counts["size"] < target_k]

        return KAnonymityReport(
            is_k_anonymous=min_size >= target_k,
            k_value=target_k,
            min_equivalence_class_size=min_size,
            violating_groups_count=len(violations)
        )

    @classmethod
    def enforce_k_anonymity_by_suppression(cls, df: pd.DataFrame, quasi_identifiers: List[str], target_k: int = 5) -> pd.DataFrame:
        """Suppresses (drops) records in equivalence classes smaller than k."""
        if df.empty or not quasi_identifiers:
            return df

        counts = df.groupby(quasi_identifiers)[quasi_identifiers[0]].transform("count")
        return df[counts >= target_k].reset_index(drop=True)
