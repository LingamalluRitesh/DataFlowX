"""
DataFlowX Composite Lakehouse Trust Score Calculator
Calculates a 0-100 Trust Index score combining Freshness SLA compliance (25%), Quality Assertion Pass Rate (40%), Volume Stability (20%), and Schema Health (15%).
"""

from typing import Dict
from pydantic import BaseModel


class DatasetTrustScore(BaseModel):
    table_name: str
    overall_trust_score: float  # 0.0 - 100.0
    quality_component: float
    freshness_component: float
    volume_component: float
    schema_component: float
    trust_grade: str  # AAA, AA, A, B, C, F


class TrustScoreCalculator:
    """Calculates dataset trust scores."""

    @classmethod
    def calculate_score(
        cls,
        table_name: str,
        assertion_pass_rate: float = 1.0,  # 0.0 - 1.0
        is_fresh: bool = True,
        volume_z_score: float = 0.5,
        schema_breaking_changes: int = 0
    ) -> DatasetTrustScore:
        q_score = assertion_pass_rate * 40.0
        f_score = 25.0 if is_fresh else 5.0
        v_score = max(0.0, 20.0 - (abs(volume_z_score) * 4.0))
        s_score = max(0.0, 15.0 - (schema_breaking_changes * 15.0))

        total = round(q_score + f_score + v_score + s_score, 1)
        grade = "AAA" if total >= 95 else "AA" if total >= 90 else "A" if total >= 80 else "B" if total >= 70 else "C" if total >= 50 else "F"

        return DatasetTrustScore(
            table_name=table_name,
            overall_trust_score=total,
            quality_component=round(q_score, 1),
            freshness_component=round(f_score, 1),
            volume_component=round(v_score, 1),
            schema_component=round(s_score, 1),
            trust_grade=grade
        )
