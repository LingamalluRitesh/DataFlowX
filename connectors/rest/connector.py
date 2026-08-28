"""
DataFlowX REST API Connector
Supports HTTP/HTTPS APIs with authentication, flexible pagination, JSONPath data extraction, and schema discovery.
"""

from datetime import datetime
import time
from typing import Any, Dict, Generator, List, Optional
import httpx
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


class RestApiConnector(BaseConnector):
    """Production connector for RESTful Web APIs."""

    def __init__(self, config: Dict[str, Any], credentials: Optional[Dict[str, Any]] = None):
        super().__init__(config, credentials)
        self.connector_type = "rest"
        self.base_url = self.config.get("base_url", "").rstrip("/")
        self.auth_type = self.config.get("auth_type", "none")  # none, bearer, api_key, basic
        self.pagination_type = self.config.get("pagination_type", "page")  # page, offset, cursor, none
        self.page_param = self.config.get("page_param", "page")
        self.limit_param = self.config.get("limit_param", "limit")
        self.results_path = self.config.get("results_path", "data")  # JSON path key containing array of records
        self.default_headers = self.config.get("headers", {})
        self.timeout = float(self.config.get("timeout_seconds", 30))
        self._client: Optional[httpx.Client] = None

    def _get_headers(self) -> Dict[str, str]:
        headers = dict(self.default_headers)
        headers["User-Agent"] = "DataFlowX-Ingestion-Engine/1.0"
        headers["Accept"] = "application/json"

        if self.auth_type == "bearer":
            token = self.credentials.get("token") or self.credentials.get("api_key")
            if token:
                headers["Authorization"] = f"Bearer {token}"
        elif self.auth_type == "api_key":
            key_name = self.config.get("api_key_header", "X-API-Key")
            key_val = self.credentials.get("api_key") or self.credentials.get("token")
            if key_val:
                headers[key_name] = str(key_val)

        return headers

    def _get_auth(self) -> Optional[httpx.BasicAuth]:
        if self.auth_type == "basic":
            user = self.credentials.get("username", "")
            pwd = self.credentials.get("password", "")
            return httpx.BasicAuth(username=user, password=pwd)
        return None

    def connect(self) -> bool:
        try:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers=self._get_headers(),
                auth=self._get_auth(),
                timeout=self.timeout,
                follow_redirects=True,
            )
            self._is_connected = True
            return True
        except Exception as exc:
            self._is_connected = False
            logger.error(f"Failed to initialize REST connector for {self.base_url}: {exc}")
            raise ConnectorError(self.connector_type, str(exc))

    def disconnect(self) -> None:
        if self._client:
            self._client.close()
        self._is_connected = False

    def test_connection(self) -> ConnectionTestResult:
        start = time.time()
        health_endpoint = self.config.get("health_endpoint", "/")
        try:
            with httpx.Client(
                base_url=self.base_url,
                headers=self._get_headers(),
                auth=self._get_auth(),
                timeout=self.timeout,
                follow_redirects=True,
            ) as client:
                res = client.get(health_endpoint)
                latency = (time.time() - start) * 1000
                if res.is_success or res.status_code in (200, 201, 204, 401, 403):
                    return ConnectionTestResult(
                        success=res.is_success,
                        status="healthy" if res.is_success else "unhealthy",
                        latency_ms=round(latency, 2),
                        message=f"HTTP {res.status_code} {res.reason_phrase}",
                        details={"status_code": res.status_code, "url": str(res.url)}
                    )
                return ConnectionTestResult(
                    success=False,
                    status="unhealthy",
                    latency_ms=round(latency, 2),
                    message=f"HTTP Error {res.status_code}: {res.text[:200]}"
                )
        except Exception as exc:
            latency = (time.time() - start) * 1000
            return ConnectionTestResult(
                success=False,
                status="unhealthy",
                latency_ms=round(latency, 2),
                message=str(exc)
            )

    def _extract_records_from_response(self, data: Any) -> List[Dict[str, Any]]:
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
        if isinstance(data, dict):
            if self.results_path and self.results_path in data:
                res = data[self.results_path]
                if isinstance(res, list):
                    return [d for d in res if isinstance(d, dict)]
            # Check common result keys
            for key in ("items", "data", "results", "records", "rows"):
                if key in data and isinstance(data[key], list):
                    return [d for d in data[key] if isinstance(d, dict)]
            return [data]
        return []

    def discover_schema(self) -> SchemaDiscoveryResult:
        endpoint = self.config.get("endpoint", "/")
        preview = self.preview_data(endpoint, limit=20)
        columns_meta: List[ColumnMeta] = []

        if preview:
            sample = preview[0]
            for k, v in sample.items():
                col_type = FieldType.STRING
                if isinstance(v, bool):
                    col_type = FieldType.BOOLEAN
                elif isinstance(v, int):
                    col_type = FieldType.INTEGER
                elif isinstance(v, float):
                    col_type = FieldType.FLOAT
                elif isinstance(v, dict):
                    col_type = FieldType.JSON
                elif isinstance(v, list):
                    col_type = FieldType.ARRAY

                columns_meta.append(ColumnMeta(
                    name=k,
                    data_type=col_type,
                    is_nullable=True,
                    is_primary_key=(k in ("id", "_id", "uuid")),
                ))

        tbl = TableMeta(
            name=endpoint.strip("/").replace("/", "_") or "api_response",
            schema_name="rest_api",
            columns=columns_meta,
            estimated_row_count=None,
            primary_keys=["id"] if any(c.name == "id" for c in columns_meta) else []
        )

        return SchemaDiscoveryResult(
            source_type=self.connector_type,
            tables=[tbl],
            metadata={"base_url": self.base_url, "endpoint": endpoint}
        )

    def preview_data(self, target: str, limit: int = 50) -> List[Dict[str, Any]]:
        if not self._is_connected or not self._client:
            self.connect()

        params = {self.limit_param: limit}
        res = self._client.get(target, params=params)
        if not res.is_success:
            raise ConnectorError(self.connector_type, f"Failed to preview data: HTTP {res.status_code} {res.text[:200]}")

        json_data = res.json()
        return self._extract_records_from_response(json_data)[:limit]

    def extract_batch(
        self,
        target: str,
        chunk_size: int = 5000,
        incremental_column: Optional[str] = None,
        watermark_value: Optional[Any] = None,
    ) -> Generator[ExtractionChunk, None, None]:
        if not self._is_connected or not self._client:
            self.connect()

        page = 1
        offset = 0
        chunk_idx = 0
        latest_watermark = watermark_value

        while True:
            params: Dict[str, Any] = {}
            if self.pagination_type == "page":
                params[self.page_param] = page
                params[self.limit_param] = chunk_size
            elif self.pagination_type == "offset":
                params[self.page_param] = offset
                params[self.limit_param] = chunk_size

            if incremental_column and watermark_value is not None:
                params[f"since_{incremental_column}"] = watermark_value

            res = self._client.get(target, params=params)
            if not res.is_success:
                raise ConnectorError(self.connector_type, f"Extraction failed on {target}: HTTP {res.status_code}")

            json_data = res.json()
            records = self._extract_records_from_response(json_data)

            if not records:
                break

            if incremental_column and records:
                latest_watermark = records[-1].get(incremental_column, latest_watermark)

            is_last = len(records) < chunk_size or self.pagination_type == "none"
            yield ExtractionChunk(
                chunk_index=chunk_idx,
                record_count=len(records),
                data=records,
                is_last_chunk=is_last,
                watermark_value=latest_watermark
            )

            chunk_idx += 1
            page += 1
            offset += len(records)

            if is_last:
                break
