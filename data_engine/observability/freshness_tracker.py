"""
DataFlowX Dataset Freshness & SLA Latency Tracker
Monitors latest partition timestamps and ingestion intervals, calculating SLA breach risk scores before SLAs expire.
"""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel


class FreshnessStatusReport(BaseModel):
    dataset_name: str
    last_updated_utc: str
    age_seconds: float
    sla_max_age_seconds: float
    is_stale: bool
    breach_risk: str  # LOW, MEDIUM, CRITICAL


class FreshnessTracker:
    """Monitors dataset freshness."""

    @classmethod
    def evaluate_freshness(cls, dataset_name: str, last_updated_unix: float, sla_max_age_seconds: float = 3600.0) -> FreshnessStatusReport:
        import time
        now = time.time()
        age = now - last_updated_unix
        is_stale = age > sla_max_age_seconds

        risk = "CRITICAL" if is_stale else "MEDIUM" if age > (sla_max_age_seconds * 0.8) else "LOW"

        return FreshnessStatusReport(
            dataset_name=dataset_name,
            last_updated_utc=datetime.fromtimestamp(last_updated_unix, timezone.utc).isoformat(),
            age_seconds=round(age, 1),
            sla_max_age_seconds=sla_max_age_seconds,
            is_stale=is_stale,
            breach_risk=risk
        )
