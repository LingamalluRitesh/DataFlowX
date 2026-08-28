"""
DataFlowX Data Outage Blast Radius Impact Calculator
Quantifies downstream blast radius impact: identifies affected executive dashboards, machine learning models, and business stakeholder teams.
"""

from typing import Dict, List
from pydantic import BaseModel, Field


class BlastRadiusReport(BaseModel):
    failed_table: str
    impacted_dashboards: List[str] = Field(default_factory=list)
    impacted_ml_models: List[str] = Field(default_factory=list)
    impacted_teams: List[str] = Field(default_factory=list)
    severity_level: str  # TIER_1_OUTAGE, TIER_2_OUTAGE, MINOR


class BlastRadiusCalculator:
    """Calculates downstream business impact."""

    @classmethod
    def calculate_blast_radius(cls, failed_table: str) -> BlastRadiusReport:
        if "gold" in failed_table or "orders" in failed_table:
            return BlastRadiusReport(
                failed_table=failed_table,
                impacted_dashboards=["Executive Daily Revenue Dashboard", "CFO Monthly ARR Tracker"],
                impacted_ml_models=["ChurnPrediction_v3", "LTV_Forecasting_Model"],
                impacted_teams=["Finance", "Executive Leadership", "Growth Marketing"],
                severity_level="TIER_1_OUTAGE"
            )

        return BlastRadiusReport(
            failed_table=failed_table,
            impacted_dashboards=["Operational Health Board"],
            impacted_ml_models=[],
            impacted_teams=["Data Engineering"],
            severity_level="MINOR"
        )
