"""
DataFlowX Amazon S3 & MinIO Object Storage Connector
Supports S3 / MinIO object listing, multipart streaming, Parquet/CSV/JSON object reads, and schema discovery.
"""

from datetime import datetime
import io
import time
from typing import Any, Dict, Generator, List, Optional
import pandas as pd
import pyarrow.parquet as pq
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


class S3Connector(BaseConnector):
    """Production connector for AWS S3 and MinIO object storage."""

    def __init__(self, config: Dict[str, Any], credentials: Optional[Dict[str, Any]] = None):
        super().__init__(config, credentials)
        self.connector_type = self.config.get("connector_type", "s3")
        self.bucket = self.config.get("bucket", "dataflowx-lake")
        self.prefix = self.config.get("prefix", "").lstrip("/")
        self.endpoint_url = self.config.get("endpoint_url")  # e.g., http://localhost:9000 for MinIO
        self.region = self.config.get("region", "us-east-1")
        self.file_format = self.config.get("file_format", "parquet")  # parquet, csv, json
        self.access_key = self.credentials.get("access_key") or self.config.get("access_key")
        self.secret_key = self.credentials.get("secret_key") or self.config.get("secret_key")
        self._s3_client = None

    def _get_client(self):
        import boto3
        from botocore.client import Config
        kwargs = {
            "region_name": self.region,
            "config": Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        }
        if self.endpoint_url:
            kwargs["endpoint_url"] = self.endpoint_url
        if self.access_key and self.secret_key:
            kwargs["aws_access_key_id"] = self.access_key
            kwargs["aws_secret_access_key"] = self.secret_key

        return boto3.client("s3", **kwargs)

    def connect(self) -> bool:
        try:
            self._s3_client = self._get_client()
            self._is_connected = True
            return True
        except Exception as exc:
            self._is_connected = False
            logger.error(f"S3 connection failed: {exc}")
            raise ConnectorError(self.connector_type, str(exc))

    def disconnect(self) -> None:
        self._is_connected = False

    def test_connection(self) -> ConnectionTestResult:
        start = time.time()
        try:
            client = self._get_client()
            client.head_bucket(Bucket=self.bucket)
            latency = (time.time() - start) * 1000
            return ConnectionTestResult(
                success=True,
                status="healthy",
                latency_ms=round(latency, 2),
                message=f"Bucket '{self.bucket}' accessible",
                details={"bucket": self.bucket, "endpoint": self.endpoint_url or "AWS S3"}
            )
        except Exception as exc:
            latency = (time.time() - start) * 1000
            return ConnectionTestResult(
                success=False,
                status="unhealthy",
                latency_ms=round(latency, 2),
                message=str(exc)
            )

    def discover_schema(self) -> SchemaDiscoveryResult:
        if not self._is_connected or not self._s3_client:
            self.connect()

        response = self._s3_client.list_objects_v2(Bucket=self.bucket, Prefix=self.prefix, MaxKeys=50)
        contents = response.get("Contents", [])

        tables_meta: List[TableMeta] = []
        if contents:
            first_obj = contents[0]
            key = first_obj["Key"]
            sample_df = self._read_s3_object_to_df(key, nrows=50)

            cols = []
            for c in sample_df.columns:
                cols.append(ColumnMeta(
                    name=str(c),
                    data_type=FieldType.STRING,
                    is_nullable=sample_df[c].isnull().any(),
                    is_primary_key=(str(c).lower() in ("id", "uuid", "key"))
                ))

            tbl = TableMeta(
                name=self.bucket,
                schema_name="s3_bucket",
                columns=cols,
                estimated_row_count=len(contents),
                primary_keys=["id"] if any(c.name == "id" for c in cols) else []
            )
            tables_meta.append(tbl)

        return SchemaDiscoveryResult(
            source_type=self.connector_type,
            tables=tables_meta,
            metadata={"bucket": self.bucket, "prefix": self.prefix}
        )

    def _read_s3_object_to_df(self, key: str, nrows: Optional[int] = None) -> pd.DataFrame:
        obj = self._s3_client.get_object(Bucket=self.bucket, Key=key)
        body = obj["Body"].read()

        if key.endswith(".parquet") or self.file_format == "parquet":
            table = pq.read_table(io.BytesIO(body))
            df = table.to_pandas()
            if nrows:
                df = df.head(nrows)
            return df
        elif key.endswith(".csv") or self.file_format == "csv":
            return pd.read_csv(io.BytesIO(body), nrows=nrows)
        elif key.endswith(".json") or self.file_format == "json":
            return pd.read_json(io.BytesIO(body), nrows=nrows)
        else:
            return pd.read_csv(io.BytesIO(body), nrows=nrows)

    def preview_data(self, target: str, limit: int = 50) -> List[Dict[str, Any]]:
        if not self._is_connected or not self._s3_client:
            self.connect()

        key = target or self.prefix
        if not key:
            res = self._s3_client.list_objects_v2(Bucket=self.bucket, MaxKeys=1)
            contents = res.get("Contents", [])
            if not contents:
                return []
            key = contents[0]["Key"]

        df = self._read_s3_object_to_df(key, nrows=limit)
        return df.where(pd.notnull(df), None).to_dict(orient="records")

    def extract_batch(
        self,
        target: str,
        chunk_size: int = 5000,
        incremental_column: Optional[str] = None,
        watermark_value: Optional[Any] = None,
    ) -> Generator[ExtractionChunk, None, None]:
        if not self._is_connected or not self._s3_client:
            self.connect()

        prefix = target or self.prefix
        paginator = self._s3_client.get_paginator("list_objects_v2")

        chunk_idx = 0
        latest_watermark = watermark_value

        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            for obj_info in page.get("Contents", []):
                key = obj_info["Key"]
                if key.endswith("/"):
                    continue

                df = self._read_s3_object_to_df(key)
                records = df.where(pd.notnull(df), None).to_dict(orient="records")

                if incremental_column and records:
                    latest_watermark = records[-1].get(incremental_column, latest_watermark)

                yield ExtractionChunk(
                    chunk_index=chunk_idx,
                    record_count=len(records),
                    data=records,
                    is_last_chunk=False,
                    watermark_value=latest_watermark
                )
                chunk_idx += 1


class MinIOConnector(S3Connector):
    """MinIO connector alias with default local endpoints."""

    def __init__(self, config: Dict[str, Any], credentials: Optional[Dict[str, Any]] = None):
        if "endpoint_url" not in config:
            config["endpoint_url"] = "http://localhost:9000"
        super().__init__(config, credentials)
        self.connector_type = "minio"
