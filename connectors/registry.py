"""
DataFlowX Connector Registry & Factory
Allows dynamic discovery, instantiation, and validation of all supported data source connectors.
"""

from typing import Any, Dict, List, Optional, Type
from backend.core.exceptions import ConnectorError
from connectors.base import BaseConnector, ConnectorType
from connectors.csv import CsvConnector
from connectors.excel import ExcelConnector
from connectors.json import JsonConnector
from connectors.kafka import KafkaConnector
from connectors.mongodb import MongoConnector
from connectors.mysql import MySQLConnector
from connectors.postgres import PostgresConnector
from connectors.rest import RestApiConnector
from connectors.s3 import MinIOConnector, S3Connector


class ConnectorRegistry:
    """Central registry and factory for all data source connectors."""

    _registry: Dict[str, Type[BaseConnector]] = {
        ConnectorType.POSTGRES.value: PostgresConnector,
        ConnectorType.MYSQL.value: MySQLConnector,
        ConnectorType.MONGODB.value: MongoConnector,
        ConnectorType.REST.value: RestApiConnector,
        ConnectorType.CSV.value: CsvConnector,
        ConnectorType.EXCEL.value: ExcelConnector,
        ConnectorType.JSON.value: JsonConnector,
        ConnectorType.KAFKA.value: KafkaConnector,
        ConnectorType.S3.value: S3Connector,
        ConnectorType.MINIO.value: MinIOConnector,
    }

    @classmethod
    def register(cls, connector_type: str, connector_cls: Type[BaseConnector]) -> None:
        """Register a custom or third-party connector class."""
        cls._registry[connector_type.lower()] = connector_cls

    @classmethod
    def get_connector_class(cls, connector_type: str) -> Type[BaseConnector]:
        """Retrieve connector class by type identifier."""
        norm_type = connector_type.lower()
        if norm_type not in cls._registry:
            raise ConnectorError(
                norm_type,
                f"Unsupported connector type: '{connector_type}'. Available: {list(cls._registry.keys())}"
            )
        return cls._registry[norm_type]

    @classmethod
    def create(
        cls,
        connector_type: str,
        config: Dict[str, Any],
        credentials: Optional[Dict[str, Any]] = None
    ) -> BaseConnector:
        """Instantiate a connector with configuration and decrypted credentials."""
        connector_cls = cls.get_connector_class(connector_type)
        return connector_cls(config=config, credentials=credentials)

    @classmethod
    def list_available_connectors(cls) -> List[str]:
        """Return list of all registered connector types."""
        return sorted(list(cls._registry.keys()))


# Direct helper
def get_connector(
    connector_type: str,
    config: Dict[str, Any],
    credentials: Optional[Dict[str, Any]] = None
) -> BaseConnector:
    return ConnectorRegistry.create(connector_type, config, credentials)
