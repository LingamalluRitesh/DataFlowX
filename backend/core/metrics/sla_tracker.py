"""
DataFlowX SLA Latency & Availability Percentile Tracker
Calculates P50, P90, P95, and P99 latency percentiles, error rate percentages, and SLA breach counters over sliding time windows.
"""

from typing import Dict, List, Optional
import numpy as np
from pydantic import BaseModel, Field


class SLAPercentilesReport(BaseModel):
    pipeline_id: str
    p50_seconds: float
    p90_seconds: float
    p95_seconds: float
    p99_seconds: float
    sla_target_seconds: float
    is_sla_compliant: bool
    breach_count: int = 0


class SLAPercentileTracker:
    """Calculates percentile adherence."""

    @classmethod
    def compute_percentiles(cls, pipeline_id: str, run_durations: List[float], sla_target_seconds: float = 60.0) -> SLAPercentilesReport:
        if not run_durations:
            return SLAPercentilesReport(
                pipeline_id=pipeline_id,
                p50_seconds=0.0, p90_seconds=0.0, p95_seconds=0.0, p99_seconds=0.0,
                sla_target_seconds=sla_target_seconds, is_sla_compliant=True
            )

        arr = np.array(run_durations)
        p50 = float(np.percentile(arr, 50))
        p90 = float(np.percentile(arr, 90))
        p95 = float(np.percentile(arr, 95))
        p99 = float(np.percentile(arr, 99))
        breaches = int((arr > sla_target_seconds).sum())

        return SLAPercentilesReport(
            pipeline_id=pipeline_id,
            p50_seconds=round(p50, 2),
            p90_seconds=round(p90, 2),
            p95_seconds=round(p95, 2),
            p99_seconds=round(p99, 2),
            sla_target_seconds=sla_target_seconds,
            is_sla_compliant=p95 <= sla_target_seconds,
            breach_count=breaches
        )
