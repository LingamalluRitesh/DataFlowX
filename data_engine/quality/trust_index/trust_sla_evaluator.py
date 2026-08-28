"""
DataFlowX Rolling Trust SLA Evaluator & Compliance Tracker
Tracks historical dataset trust trends across 30, 60, and 90-day rolling evaluation windows.
"""

from typing import Dict, List
from pydantic import BaseModel


class TrustSLAReport(BaseModel):
    table_name: str
    sla_target_score: float
    rolling_30d_avg_score: float
    is_sla_met: bool
    breach_incidents_30d: int


class TrustSLAEvaluator:
    """Evaluates long-term trust SLA performance."""

    @classmethod
    def evaluate_sla(cls, table_name: str, historical_scores: List[float], sla_target: float = 85.0) -> TrustSLAReport:
        if not historical_scores:
            return TrustSLAReport(table_name=table_name, sla_target_score=sla_target, rolling_30d_avg_score=100.0, is_sla_met=True, breach_incidents_30d=0)

        avg = round(sum(historical_scores) / len(historical_scores), 1)
        breaches = sum(1 for s in historical_scores if s < sla_target)

        return TrustSLAReport(
            table_name=table_name,
            sla_target_score=sla_target,
            rolling_30d_avg_score=avg,
            is_sla_met=avg >= sla_target,
            breach_incidents_30d=breaches
        )
