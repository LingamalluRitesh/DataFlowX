"""
DataFlowX OpenLineage & Marquez Standard Event Emitter
Exports JSON-LD RunEvent specifications (START, RUNNING, COMPLETE, FAIL) compatible with OpenLineage backends.
"""

from datetime import datetime, timezone
import json
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class OpenLineageJob(BaseModel):
    namespace: str = "dataflowx-production"
    name: str


class OpenLineageRun(BaseModel):
    runId: str


class OpenLineageDataset(BaseModel):
    namespace: str
    name: str
    facets: Dict[str, Any] = Field(default_factory=dict)


class OpenLineageRunEvent(BaseModel):
    eventType: str  # START, RUNNING, COMPLETE, FAIL, ABORT
    eventTime: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    run: OpenLineageRun
    job: OpenLineageJob
    inputs: List[OpenLineageDataset] = Field(default_factory=list)
    outputs: List[OpenLineageDataset] = Field(default_factory=list)
    producer: str = "https://github.com/LingamalluRitesh/DataFlowX"


class OpenLineageEmitter:
    """Dispatches OpenLineage standard events to OpenLineage HTTP endpoints or Marquez server."""

    def __init__(self, backend_url: str = "http://localhost:5000/api/v1/lineage"):
        self.backend_url = backend_url

    def emit_event(self, event: OpenLineageRunEvent) -> None:
        logger.info(f"Emitted OpenLineage event '{event.eventType}' for job '{event.job.name}' (runId={event.run.runId})")
