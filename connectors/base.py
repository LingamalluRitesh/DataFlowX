"""
DataFlowX Base Connector Interface
Defines the standard contract for all heterogeneous data source connectors.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import time
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional
from pydantic import BaseModel, Field
from backend.core.logging import get_logger

logger = get_logger(__name__)


class ConnectorType(str, Enum):
    POSTGRES = "postgres"
    MYSQL = "mysql"
    MONGODB = "mongodb"
    REST = "rest"
    CSV = "csv"
    EXCEL = "excel"
    JSON = "json"
    KAFKA = "kafka"
    S3 = "s3"
    MINIO = "minio"


class FieldType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    TIMESTAMP = "timestamp"
    DATE = "date"
    JSON = "json"
    ARRAY = "array"
    BINARY = "binary"


class ColumnMeta(BaseModel):
    name: str
    data_type: FieldType
    is_nullable: bool = True
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_target: Optional[str] = None
    sample_values: List[Any] = Field(default_factory=list)
    description: Optional[str] = None


class TableMeta(BaseModel):
    name: str
    schema_name: Optional[str] = None
    columns: List[ColumnMeta] = Field(default_factory=list)
    estimated_row_count: Optional[int] = None
    primary_keys: List[str] = Field(default_factory=list)


class SchemaDiscoveryResult(BaseModel):
    source_type: str
    tables: List[TableMeta] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    discovered_at: datetime = Field(default_factory=datetime.utcnow)


ColumnSchema = ColumnMeta
TableSchema = TableMeta
SchemaInfo = SchemaDiscoveryResult


class ConnectionTestResult(BaseModel):
    success: bool
    status: str  # healthy, unhealthy
    latency_ms: float
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class ExtractionChunk(BaseModel):
    chunk_index: int
    record_count: int
    data: List[Dict[str, Any]]
    is_last_chunk: bool = False
    watermark_value: Optional[Any] = None


class BaseConnector(ABC):
    """Abstract Base Connector for all data source integrations."""

    def __init__(self, config: Dict[str, Any], credentials: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.credentials = credentials or {}
        self.connector_type: str = "generic"
        self._is_connected: bool = False

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to data source."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Release all connections and resources."""
        pass

    @abstractmethod
    def test_connection(self) -> ConnectionTestResult:
        """Verify connectivity and credentials with latency check."""
        pass

    @abstractmethod
    def discover_schema(self) -> SchemaDiscoveryResult:
        """Introspect tables, columns, constraints, and data types."""
        pass

    @abstractmethod
    def preview_data(self, target: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Extract a small sample of records for preview in UI."""
        pass

    @abstractmethod
    def extract_batch(
        self,
        target: str,
        chunk_size: int = 5000,
        incremental_column: Optional[str] = None,
        watermark_value: Optional[Any] = None,
    ) -> Generator[ExtractionChunk, None, None]:
        """Yield stream of chunks for batch processing."""
        pass

    def validate_credentials(self) -> bool:
        """Validate format of provided credentials."""
        return True

    def get_health(self) -> ConnectionTestResult:
        """Execute non-intrusive health check."""
        start = time.time()
        try:
            return self.test_connection()
        except Exception as exc:
            duration = (time.time() - start) * 1000
            return ConnectionTestResult(
                success=False,
                status="unhealthy",
                latency_ms=duration,
                message=str(exc)
            )

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
