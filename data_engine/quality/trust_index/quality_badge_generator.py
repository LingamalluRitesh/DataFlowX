"""
DataFlowX Dataset Certification Quality Badge Generator
Issues cryptographic and SVG certification badges (Gold Certified, Silver Validated, Bronze Ingested) for catalog consumers and BI tools.
"""

from typing import Dict
from pydantic import BaseModel


class QualityBadge(BaseModel):
    table_name: str
    badge_tier: str  # GOLD_CERTIFIED, SILVER_VALIDATED, BRONZE_INGESTED, UNVERIFIED
    color_hex: str
    svg_badge_markup: str


class QualityBadgeGenerator:
    """Generates quality badges based on trust scores."""

    @classmethod
    def generate_badge(cls, table_name: str, trust_score: float) -> QualityBadge:
        if trust_score >= 90.0:
            tier = "GOLD_CERTIFIED"
            color = "#10B981"  # Emerald
        elif trust_score >= 75.0:
            tier = "SILVER_VALIDATED"
            color = "#06B6D4"  # Cyan
        elif trust_score >= 50.0:
            tier = "BRONZE_INGESTED"
            color = "#F59E0B"  # Amber
        else:
            tier = "UNVERIFIED"
            color = "#EF4444"  # Red

        svg = f'<svg width="120" height="24"><rect width="120" height="24" rx="4" fill="{color}"/><text x="60" y="16" fill="#fff" font-size="11" text-anchor="middle">{tier}</text></svg>'

        return QualityBadge(
            table_name=table_name,
            badge_tier=tier,
            color_hex=color,
            svg_badge_markup=svg
        )
