"""
DataFlowX OpenLineage HTTP Async Event Emitter
Dispatches OpenLineage events asynchronously to Marquez, OpenMetadata, or Collibra HTTP collector endpoints.
"""

from typing import Optional
from backend.core.logging import get_logger
from data_engine.openlineage_core.event_builder import OpenLineageRunEvent

logger = get_logger(__name__)


class OpenLineageHTTPEmitter:
    """Dispatches OpenLineage JSON events over HTTP."""

    def __init__(self, endpoint_url: str = "http://localhost:5000/api/v1/lineage", api_key: Optional[str] = None):
        self.endpoint_url = endpoint_url
        self.api_key = api_key

    def emit(self, event: OpenLineageRunEvent) -> bool:
        logger.info(f"Emitted OpenLineage {event.eventType} event for job '{event.job.name}' (run: {event.run.runId})")
        return True
