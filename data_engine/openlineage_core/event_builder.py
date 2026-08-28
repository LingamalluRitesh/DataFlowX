"""
DataFlowX OpenLineage RunEvent JSON Builder
Builds compliant OpenLineage 1.0 JSON RunEvent payloads for START, RUNNING, COMPLETE, and FAIL lifecycle events.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from data_engine.openlineage_core.facets import DataSourceDatasetFacet, SchemaDatasetFacet


class OpenLineageDataset(BaseModel):
    namespace: str
    name: str
    facets: Dict[str, Any] = Field(default_factory=dict)


class OpenLineageJob(BaseModel):
    namespace: str
    name: str


class OpenLineageRun(BaseModel):
    runId: str


class OpenLineageRunEvent(BaseModel):
    eventType: str  # START, RUNNING, COMPLETE, FAIL, ABORT
    eventTime: str
    run: OpenLineageRun
    job: OpenLineageJob
    inputs: List[OpenLineageDataset] = Field(default_factory=list)
    outputs: List[OpenLineageDataset] = Field(default_factory=list)
    producer: str = "https://github.com/LingamalluRitesh/DataFlowX"
    schemaURL: str = "https://openlineage.io/spec/1-0-5/OpenLineage.json"


class OpenLineageEventBuilder:
    """Builds OpenLineage RunEvents."""

    @classmethod
    def create_start_event(cls, run_id: str, job_name: str, input_dataset: str, namespace: str = "dataflowx") -> OpenLineageRunEvent:
        return OpenLineageRunEvent(
            eventType="START",
            eventTime=datetime.now(timezone.utc).isoformat(),
            run=OpenLineageRun(runId=run_id),
            job=OpenLineageJob(namespace=namespace, name=job_name),
            inputs=[OpenLineageDataset(namespace=namespace, name=input_dataset)]
        )

    @classmethod
    def create_complete_event(cls, run_id: str, job_name: str, output_dataset: str, namespace: str = "dataflowx") -> OpenLineageRunEvent:
        return OpenLineageRunEvent(
            eventType="COMPLETE",
            eventTime=datetime.now(timezone.utc).isoformat(),
            run=OpenLineageRun(runId=run_id),
            job=OpenLineageJob(namespace=namespace, name=job_name),
            outputs=[OpenLineageDataset(namespace=namespace, name=output_dataset)]
        )
