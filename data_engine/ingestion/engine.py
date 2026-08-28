"""
DataFlowX Batch Ingestion Engine
Orchestrates high-throughput extraction from heterogeneous connectors and persists raw immutable data to the Bronze layer.
"""

from datetime import datetime, timezone
import os
import time
from typing import Any, Dict, Generator, List, Optional
from pydantic import BaseModel, Field
from backend.core.exceptions import ConnectorError
from backend.core.logging import get_logger
from connectors.base import BaseConnector, ExtractionChunk
from connectors.registry import ConnectorRegistry
from data_engine.ingestion.watermark import WatermarkTracker
from storage import ParquetManager, storage_engine

logger = get_logger(__name__)


class IngestionJobConfig(BaseModel):
    pipeline_id: str
    execution_id: str
    source_id: str
    connector_type: str
    target_table_or_endpoint: str
    connector_config: Dict[str, Any]
    credentials: Optional[Dict[str, Any]] = None
    ingestion_mode: str = "full"  # full, incremental, append
    incremental_column: Optional[str] = None
    chunk_size: int = 5000
    destination_bronze_path: Optional[str] = None


class IngestionResult(BaseModel):
    success: bool
    pipeline_id: str
    execution_id: str
    total_records: int
    total_bytes: int
    chunks_count: int
    duration_seconds: float
    bronze_files: List[str] = Field(default_factory=list)
    new_watermark: Optional[Any] = None
    error_message: Optional[str] = None


class IngestionEngine:
    """Enterprise batch ingestion processor."""

    def __init__(self, watermark_tracker: Optional[WatermarkTracker] = None):
        self.watermark_tracker = watermark_tracker or WatermarkTracker()

    def run_ingestion(self, job: IngestionJobConfig) -> IngestionResult:
        start_time = time.time()
        logger.info(
            f"Starting ingestion job for pipeline '{job.pipeline_id}', execution '{job.execution_id}', "
            f"source '{job.connector_type}' -> '{job.target_table_or_endpoint}' (mode={job.ingestion_mode})"
        )

        connector: BaseConnector = ConnectorRegistry.create(
            job.connector_type,
            config=job.connector_config,
            credentials=job.credentials
        )

        total_records = 0
        total_bytes = 0
        chunks_count = 0
        bronze_files: List[str] = []
        current_watermark = None

        if job.ingestion_mode == "incremental" and job.incremental_column:
            wm_entry = self.watermark_tracker.get_watermark(job.pipeline_id, job.source_id, job.target_table_or_endpoint)
            current_watermark = wm_entry.get("value") if isinstance(wm_entry, dict) else wm_entry

        try:
            connector.connect()

            # Date partition path
            now = datetime.now(timezone.utc)
            date_str = now.strftime("%Y-%m-%d")
            base_bronze = job.destination_bronze_path or f"bronze/{job.source_id}/{job.target_table_or_endpoint.replace('/', '_')}/{date_str}"

            extractor: Generator[ExtractionChunk, None, None] = connector.extract_batch(
                target=job.target_table_or_endpoint,
                chunk_size=job.chunk_size,
                incremental_column=job.incremental_column if job.ingestion_mode == "incremental" else None,
                watermark_value=current_watermark,
            )

            for chunk in extractor:
                if not chunk.data:
                    continue

                # Add metadata envelope to raw records
                enriched_records = []
                for rec in chunk.data:
                    enriched = dict(rec)
                    enriched["_dfx_ingested_at"] = now.isoformat()
                    enriched["_dfx_execution_id"] = job.execution_id
                    enriched["_dfx_pipeline_id"] = job.pipeline_id
                    enriched["_dfx_source_id"] = job.source_id
                    enriched_records.append(enriched)

                # Convert to Parquet bytes and persist
                parquet_bytes = ParquetManager.records_to_parquet_bytes(enriched_records)
                filename = f"chunk_{job.execution_id[:8]}_{chunk.chunk_index:04d}.parquet"
                storage_key = f"{base_bronze}/{filename}"

                storage_engine.put_object(storage_key, parquet_bytes, content_type="application/octet-stream")
                bronze_files.append(storage_key)

                total_records += chunk.record_count
                total_bytes += len(parquet_bytes)
                chunks_count += 1
                current_watermark = chunk.watermark_value

            connector.disconnect()

            # Commit new watermark if incremental
            if job.ingestion_mode == "incremental" and current_watermark is not None:
                self.watermark_tracker.set_watermark(
                    job.pipeline_id,
                    job.source_id,
                    job.target_table_or_endpoint,
                    current_watermark
                )

            duration = time.time() - start_time
            logger.info(
                f"Ingestion completed successfully: {total_records} records ({total_bytes / 1024:.2f} KB) "
                f"across {chunks_count} chunks in {duration:.2f}s"
            )

            return IngestionResult(
                success=True,
                pipeline_id=job.pipeline_id,
                execution_id=job.execution_id,
                total_records=total_records,
                total_bytes=total_bytes,
                chunks_count=chunks_count,
                duration_seconds=round(duration, 2),
                bronze_files=bronze_files,
                new_watermark=current_watermark
            )

        except Exception as exc:
            connector.disconnect()
            duration = time.time() - start_time
            logger.exception(f"Ingestion failed for execution {job.execution_id}: {exc}")
            return IngestionResult(
                success=False,
                pipeline_id=job.pipeline_id,
                execution_id=job.execution_id,
                total_records=total_records,
                total_bytes=total_bytes,
                chunks_count=chunks_count,
                duration_seconds=round(duration, 2),
                bronze_files=bronze_files,
                error_message=str(exc)
            )
