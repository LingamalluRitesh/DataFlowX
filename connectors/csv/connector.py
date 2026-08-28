"""
DataFlowX CSV File Connector
High-performance streaming CSV parser with delimiter sniffing, header inference, and chunked extraction.
"""

import csv
from datetime import datetime
import io
import os
import time
from typing import Any, Dict, Generator, List, Optional
import pandas as pd
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


def infer_dtype(val: str) -> FieldType:
    if val is None or val == "":
        return FieldType.STRING
    # Check boolean
    if val.lower() in ("true", "false", "yes", "no"):
        return FieldType.BOOLEAN
    # Check integer
    try:
        int(val)
        return FieldType.INTEGER
    except ValueError:
        pass
    # Check float
    try:
        float(val)
        return FieldType.FLOAT
    except ValueError:
        pass
    # Check ISO timestamp
    if len(val) >= 10 and ("-" in val or "/" in val):
        try:
            pd.to_datetime(val)
            return FieldType.TIMESTAMP
        except Exception:
            pass
    return FieldType.STRING


class CsvConnector(BaseConnector):
    """Production connector for CSV / TSV / Delimited flat files."""

    def __init__(self, config: Dict[str, Any], credentials: Optional[Dict[str, Any]] = None):
        super().__init__(config, credentials)
        self.connector_type = "csv"
        self.file_path = self.config.get("file_path", "")
        self.delimiter = self.config.get("delimiter", ",")
        self.has_header = self.config.get("has_header", True)
        self.encoding = self.config.get("encoding", "utf-8")
        self.quote_char = self.config.get("quote_char", '"')

    def connect(self) -> bool:
        if not os.path.exists(self.file_path):
            raise ConnectorError(self.connector_type, f"CSV file not found at: {self.file_path}")
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
            latency = (time.time() - start) * 1000
            return ConnectionTestResult(
                success=True,
                status="healthy",
                latency_ms=round(latency, 2),
                message="CSV file verified accessible",
                details={"file_size_bytes": size_bytes, "path": self.file_path}
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

        # Read first 100 rows for schema inference
        df_sample = pd.read_csv(
            self.file_path,
            sep=self.delimiter,
            encoding=self.encoding,
            nrows=100,
            dtype=str
        )

        columns_meta: List[ColumnMeta] = []
        for col_name in df_sample.columns:
            series = df_sample[col_name].dropna()
            inferred = FieldType.STRING
            if not series.empty:
                inferred = infer_dtype(str(series.iloc[0]))

            columns_meta.append(ColumnMeta(
                name=str(col_name),
                data_type=inferred,
                is_nullable=df_sample[col_name].isnull().any(),
                is_primary_key=(str(col_name).lower() in ("id", "key")),
                sample_values=series.head(3).tolist()
            ))

        table_name = os.path.splitext(os.path.basename(self.file_path))[0]
        table_meta = TableMeta(
            name=table_name,
            schema_name="file_system",
            columns=columns_meta,
            estimated_row_count=None,
            primary_keys=["id"] if any(c.name.lower() == "id" for c in columns_meta) else []
        )

        return SchemaDiscoveryResult(
            source_type=self.connector_type,
            tables=[table_meta],
            metadata={"file_path": self.file_path, "encoding": self.encoding}
        )

    def preview_data(self, target: str, limit: int = 50) -> List[Dict[str, Any]]:
        path = target or self.file_path
        if not os.path.exists(path):
            raise ConnectorError(self.connector_type, f"File not found: {path}")

        df = pd.read_csv(
            path,
            sep=self.delimiter,
            encoding=self.encoding,
            nrows=limit
        )
        return df.where(pd.notnull(df), None).to_dict(orient="records")

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

        for df_chunk in pd.read_csv(
            path,
            sep=self.delimiter,
            encoding=self.encoding,
            chunksize=chunk_size
        ):
            # Clean NaNs to None for JSON serialization
            records = df_chunk.where(pd.notnull(df_chunk), None).to_dict(orient="records")

            if incremental_column and records:
                latest_watermark = records[-1].get(incremental_column, latest_watermark)

            is_last = len(records) < chunk_size
            yield ExtractionChunk(
                chunk_index=chunk_idx,
                record_count=len(records),
                data=records,
                is_last_chunk=is_last,
                watermark_value=latest_watermark
            )
            chunk_idx += 1
            if is_last:
                break
