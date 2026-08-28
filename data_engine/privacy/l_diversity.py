"""
DataFlowX L-Diversity Privacy Protection Engine
Ensures that each equivalence class in a quasi-identifier group contains at least l well-represented distinct values for sensitive attributes (e.g. Medical Diagnosis).
"""

from typing import List
import pandas as pd
from pydantic import BaseModel


class LDiversityReport(BaseModel):
    is_l_diverse: bool
    l_value: int
    min_distinct_sensitive_values: int
    violating_groups_count: int


class LDiversityEngine:
    """Evaluates distinct l-diversity."""

    @classmethod
    def evaluate_distinct_l_diversity(cls, df: pd.DataFrame, quasi_identifiers: List[str], sensitive_column: str, target_l: int = 3) -> LDiversityReport:
        if df.empty or not quasi_identifiers or sensitive_column not in df.columns:
            return LDiversityReport(is_l_diverse=True, l_value=target_l, min_distinct_sensitive_values=0, violating_groups_count=0)

        group_diversity = df.groupby(quasi_identifiers)[sensitive_column].nunique()
        min_distinct = int(group_diversity.min()) if not group_diversity.empty else 0
        violations = int((group_diversity < target_l).sum())

        return LDiversityReport(
            is_l_diverse=min_distinct >= target_l,
            l_value=target_l,
            min_distinct_sensitive_values=min_distinct,
            violating_groups_count=violations
        )
