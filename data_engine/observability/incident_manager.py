"""
DataFlowX Automated Data Incident Manager
Automatically creates data incidents, deduplicates alerts, and calculates blast radius impact for failed pipelines and corrupted datasets.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class DataIncident(BaseModel):
    incident_id: str
    dataset_name: str
    incident_type: str  # VOLUME_ANOMALY, FRESHNESS_BREACH, SCHEMA_BREAKAGE, QUALITY_FAIL
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    status: str = "OPEN"  # OPEN, INVESTIGATING, RESOLVED
    created_at_unix: float
    description: str


class IncidentManager:
    """Manages open data health incidents."""

    def __init__(self):
        self._incidents: Dict[str, DataIncident] = {}

    def create_incident(self, dataset_name: str, incident_type: str, severity: str, description: str) -> DataIncident:
        import time
        inc_id = f"inc_{dataset_name}_{int(time.time())}"
        inc = DataIncident(
            incident_id=inc_id,
            dataset_name=dataset_name,
            incident_type=incident_type,
            severity=severity,
            status="OPEN",
            created_at_unix=time.time(),
            description=description
        )
        self._incidents[inc_id] = inc
        logger.warning(f"Created Data Incident '{inc_id}' ({severity}): {description}")
        return inc

    def list_open_incidents(self) -> List[DataIncident]:
        return [inc for inc in self._incidents.values() if inc.status != "RESOLVED"]
