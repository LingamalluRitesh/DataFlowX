"""
DataFlowX MongoDB NoSQL Connector
Supports document schema sampling, nested field flattening, and chunked cursor extraction.
"""

from datetime import datetime
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


def infer_mongo_type(val: Any) -> FieldType:
    if isinstance(val, bool):
        return FieldType.BOOLEAN
    if isinstance(val, int):
        return FieldType.INTEGER
    if isinstance(val, float):
        return FieldType.FLOAT
    if isinstance(val, datetime):
        return FieldType.TIMESTAMP
    if isinstance(val, dict):
        return FieldType.JSON
    if isinstance(val, list):
        return FieldType.ARRAY
    return FieldType.STRING


class MongoConnector(BaseConnector):
    """Production connector for MongoDB databases."""

    def __init__(self, config: Dict[str, Any], credentials: Optional[Dict[str, Any]] = None):
        super().__init__(config, credentials)
        self.connector_type = "mongodb"
        self.host = self.config.get("host", "localhost")
        self.port = int(self.config.get("port", 27017))
        self.database = self.config.get("database", "admin")
        self.auth_source = self.config.get("auth_source", "admin")
        self.uri = self.config.get("uri")
        self.username = self.credentials.get("username") or self.config.get("username")
        self.password = self.credentials.get("password") or self.config.get("password")
        self._client = None
        self._db = None

    def _get_client(self):
        from pymongo import MongoClient
        if self.uri:
            return MongoClient(self.uri, serverSelectionTimeoutMS=5000)
        if self.username and self.password:
            return MongoClient(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                authSource=self.auth_source,
                serverSelectionTimeoutMS=5000
            )
        return MongoClient(host=self.host, port=self.port, serverSelectionTimeoutMS=5000)

    def connect(self) -> bool:
        try:
            self._client = self._get_client()
            # Force server handshake
            self._client.admin.command("ping")
            self._db = self._client[self.database]
            self._is_connected = True
            return True
        except Exception as exc:
            self._is_connected = False
            logger.error(f"MongoDB connection failed: {exc}")
            raise ConnectorError(self.connector_type, str(exc))

    def disconnect(self) -> None:
        if self._client:
            self._client.close()
        self._is_connected = False

    def test_connection(self) -> ConnectionTestResult:
        start = time.time()
        try:
            client = self._get_client()
            client.admin.command("ping")
            server_info = client.server_info()
            version = server_info.get("version", "unknown")
            client.close()
            latency = (time.time() - start) * 1000
            return ConnectionTestResult(
                success=True,
                status="healthy",
                latency_ms=round(latency, 2),
                message="Successfully connected to MongoDB server",
                details={"version": version, "database": self.database}
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
        if not self._is_connected or not self._client:
            self.connect()

        collections = self._db.list_collection_names()
        tables_meta: List[TableMeta] = []

        for coll_name in collections:
            if coll_name.startswith("system."):
                continue

            coll = self._db[coll_name]
            est_count = coll.estimated_document_count()

            # Sample first 100 documents to infer dynamic schema
            sample_docs = list(coll.find().limit(100))
            fields_detected: Dict[str, FieldType] = {}
            for doc in sample_docs:
                for k, v in doc.items():
                    if k not in fields_detected:
                        fields_detected[k] = infer_mongo_type(v)

            columns_meta = []
            for col_name, ftype in fields_detected.items():
                columns_meta.append(ColumnMeta(
                    name=col_name,
                    data_type=ftype,
                    is_nullable=True,
                    is_primary_key=(col_name == "_id"),
                ))

            tables_meta.append(TableMeta(
                name=coll_name,
                schema_name=self.database,
                columns=columns_meta,
                estimated_row_count=est_count,
                primary_keys=["_id"]
            ))

        return SchemaDiscoveryResult(
            source_type=self.connector_type,
            tables=tables_meta,
            metadata={"database": self.database}
        )

    def preview_data(self, target: str, limit: int = 50) -> List[Dict[str, Any]]:
        if not self._is_connected or not self._client:
            self.connect()

        coll = self._db[target]
        docs = list(coll.find().limit(limit))
        # Convert ObjectId and binary types to string for serialization
        return [self._sanitize_document(d) for d in docs]

    def extract_batch(
        self,
        target: str,
        chunk_size: int = 5000,
        incremental_column: Optional[str] = None,
        watermark_value: Optional[Any] = None,
    ) -> Generator[ExtractionChunk, None, None]:
        if not self._is_connected or not self._client:
            self.connect()

        coll = self._db[target]
        query = {}
        if incremental_column and watermark_value is not None:
            query[incremental_column] = {"$gt": watermark_value}

        cursor = coll.find(query)
        if incremental_column:
            cursor = cursor.sort(incremental_column, 1)

        batch: List[Dict[str, Any]] = []
        chunk_idx = 0
        latest_watermark = watermark_value

        for doc in cursor:
            clean_doc = self._sanitize_document(doc)
            batch.append(clean_doc)
            if incremental_column:
                latest_watermark = clean_doc.get(incremental_column, latest_watermark)

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

    def _sanitize_document(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert BSON ObjectIds, timestamps, and binary payloads into serializable types."""
        sanitized = {}
        for k, v in doc.items():
            if hasattr(v, "__str__") and type(v).__name__ in ("ObjectId", "Binary"):
                sanitized[k] = str(v)
            elif isinstance(v, datetime):
                sanitized[k] = v.isoformat()
            elif isinstance(v, dict):
                sanitized[k] = self._sanitize_document(v)
            elif isinstance(v, list):
                sanitized[k] = [self._sanitize_document(i) if isinstance(i, dict) else str(i) if type(i).__name__ == "ObjectId" else i for i in v]
            else:
                sanitized[k] = v
        return sanitized
