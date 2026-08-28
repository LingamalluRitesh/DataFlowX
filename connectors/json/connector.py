"""
DataFlowX JSON / NDJSON File Connector
Supports JSON arrays, newline-delimited JSON (JSONLines/NDJSON), and streaming chunked reads.
"""

from datetime import datetime
import json
import os
import time
from typing import Any, Dict, Generator, List, Optional
from backend.core.exceptions import ConnectorError
from backend.core.logging import get_logger
from connectors.base import (
    BaseConnector,
    ColumnMeta,
    ConnectionTestResult,
    ExtractionChunk,
    FieldType,
    SchemaDiscoveryResult,
    TableMeta,
)

logger = get_logger(__name__)


def infer_json_field_type(v: Any) -> FieldType:
    if isinstance(v, bool):
        return FieldType.BOOLEAN
    if isinstance(v, int):
        return FieldType.INTEGER
    if isinstance(v, float):
        return FieldType.FLOAT
    if isinstance(v, dict):
        return FieldType.JSON
    if isinstance(v, list):
        return FieldType.ARRAY
    return FieldType.STRING


class JsonConnector(BaseConnector):
    """Production connector for JSON and NDJSON files."""

    def __init__(self, config: Dict[str, Any], credentials: Optional[Dict[str, Any]] = None):
        super().__init__(config, credentials)
        self.connector_type = "json"
        self.file_path = self.config.get("file_path", "")
        self.is_ndjson = self.config.get("is_ndjson", False) or self.file_path.endswith((".jsonl", ".ndjson"))
        self.encoding = self.config.get("encoding", "utf-8")

    def connect(self) -> bool:
        if not os.path.exists(self.file_path):
            raise ConnectorError(self.connector_type, f"JSON file not found: {self.file_path}")
        self._is_connected = True
        return True

    def disconnect(self) -> None:
        self._is_connected = False

    def test_connection(self) -> ConnectionTestResult:
        start = time.time()
        try:
            if not os.path.exists(self.file_path):
                return ConnectionTestResult(
                    success=False,
                    status="unhealthy",
                    latency_ms=(time.time() - start) * 1000,
                    message=f"File not found: {self.file_path}"
                )
            size_bytes = os.path.getsize(self.file_path)
            return ConnectionTestResult(
                success=True,
                status="healthy",
                latency_ms=round((time.time() - start) * 1000, 2),
                message="JSON file accessible",
                details={"file_size_bytes": size_bytes, "is_ndjson": self.is_ndjson}
            )
        except Exception as exc:
            return ConnectionTestResult(
                success=False,
                status="unhealthy",
                latency_ms=(time.time() - start) * 1000,
                message=str(exc)
            )

    def discover_schema(self) -> SchemaDiscoveryResult:
        if not os.path.exists(self.file_path):
            self.connect()

        preview = self.preview_data(self.file_path, limit=50)
        fields: Dict[str, FieldType] = {}
        for record in preview:
            for k, v in record.items():
                if k not in fields:
                    fields[k] = infer_json_field_type(v)

        columns_meta = [
            ColumnMeta(
                name=k,
                data_type=v,
                is_nullable=True,
                is_primary_key=(k.lower() in ("id", "_id", "key")),
            )
            for k, v in fields.items()
        ]

        table_name = os.path.splitext(os.path.basename(self.file_path))[0]
        tbl = TableMeta(
            name=table_name,
            schema_name="json_file",
            columns=columns_meta,
            primary_keys=["id"] if any(c.name == "id" for c in columns_meta) else []
        )

        return SchemaDiscoveryResult(
            source_type=self.connector_type,
            tables=[tbl],
            metadata={"file_path": self.file_path, "is_ndjson": self.is_ndjson}
        )

    def preview_data(self, target: str, limit: int = 50) -> List[Dict[str, Any]]:
        path = target or self.file_path
        if not os.path.exists(path):
            raise ConnectorError(self.connector_type, f"File not found: {path}")

        records: List[Dict[str, Any]] = []
        with open(path, "r", encoding=self.encoding) as f:
            if self.is_ndjson:
                for line in f:
                    line = line.strip()
                    if line:
                        records.append(json.loads(line))
                        if len(records) >= limit:
                            break
            else:
                data = json.load(f)
                if isinstance(data, list):
                    records = [d for d in data if isinstance(d, dict)][:limit]
                elif isinstance(data, dict):
                    records = [data]
        return records

    def extract_batch(
        self,
        target: str,
        chunk_size: int = 5000,
        incremental_column: Optional[str] = None,
        watermark_value: Optional[Any] = None,
    ) -> Generator[ExtractionChunk, None, None]:
        path = target or self.file_path
        if not os.path.exists(path):
            raise ConnectorError(self.connector_type, f"File not found: {path}")

        chunk_idx = 0
        latest_watermark = watermark_value
        batch: List[Dict[str, Any]] = []

        with open(path, "r", encoding=self.encoding) as f:
            if self.is_ndjson:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    record = json.loads(line)
                    if incremental_column and watermark_value is not None:
                        if record.get(incremental_column, "") <= watermark_value:
                            continue
                    batch.append(record)
                    if incremental_column:
                        latest_watermark = record.get(incremental_column, latest_watermark)

                    if len(batch) >= chunk_size:
                        yield ExtractionChunk(
                            chunk_index=chunk_idx,
                            record_count=len(batch),
                            data=batch,
                            is_last_chunk=False,
                            watermark_value=latest_watermark
                        )
                        chunk_idx += 1
                        batch = []

                if batch or chunk_idx == 0:
                    yield ExtractionChunk(
                        chunk_index=chunk_idx,
                        record_count=len(batch),
                        data=batch,
                        is_last_chunk=True,
                        watermark_value=latest_watermark
                    )
            else:
                data = json.load(f)
                all_records = data if isinstance(data, list) else [data]
                total = len(all_records)
                for start_idx in range(0, total, chunk_size):
                    chunk_slice = all_records[start_idx : start_idx + chunk_size]
                    if incremental_column and chunk_slice:
                        latest_watermark = chunk_slice[-1].get(incremental_column, latest_watermark)

                    is_last = (start_idx + chunk_size) >= total
                    yield ExtractionChunk(
                        chunk_index=chunk_idx,
                        record_count=len(chunk_slice),
                        data=chunk_slice,
                        is_last_chunk=is_last,
                        watermark_value=latest_watermark
                    )
                    chunk_idx += 1
