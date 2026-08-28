"""
DataFlowX Connector Registry & Factory
Allows dynamic discovery, instantiation, and validation of all supported data source connectors.
"""

from typing import Any, Dict, List, Optional, Type
from backend.core.exceptions import ConnectorError
from connectors.base import BaseConnector, ConnectorType
from connectors.azure_blob import AzureBlobConnector
from connectors.bigquery import BigQueryConnector
from connectors.cassandra import CassandraConnector
from connectors.clickhouse import ClickHouseConnector
from connectors.csv import CsvConnector
from connectors.duckdb import DuckDBConnector
from connectors.dynamodb import DynamoDBConnector
from connectors.elasticsearch import ElasticsearchConnector
from connectors.excel import ExcelConnector
from connectors.google_sheets import GoogleSheetsConnector
from connectors.grpc import GrpcConnector
from connectors.hubspot import HubSpotConnector
from connectors.jira import JiraConnector
from connectors.json import JsonConnector
from connectors.kafka import KafkaConnector
from connectors.mongodb import MongoConnector
from connectors.mysql import MySQLConnector
from connectors.neo4j import Neo4jConnector
from connectors.oracle import OracleConnector
from connectors.postgres import PostgresConnector
from connectors.redis_stream import RedisStreamConnector
from connectors.redshift import RedshiftConnector
from connectors.rest import RestApiConnector
from connectors.s3 import MinIOConnector, S3Connector
from connectors.salesforce import SalesforceConnector
from connectors.sap_hana import SapHanaConnector
from connectors.service_now import ServiceNowConnector
from connectors.snowflake import SnowflakeConnector
from connectors.sqlserver import SQLServerConnector
from connectors.stripe import StripeConnector
from connectors.teradata import TeradataConnector
from connectors.zendesk import ZendeskConnector


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
        # Enterprise Cloud Warehouses
        "snowflake": SnowflakeConnector,
        "bigquery": BigQueryConnector,
        "redshift": RedshiftConnector,
        "teradata": TeradataConnector,
        "sap_hana": SapHanaConnector,
        # Real-Time, Analytical & NoSQL Databases
        "elasticsearch": ElasticsearchConnector,
        "opensearch": ElasticsearchConnector,
        "redis_stream": RedisStreamConnector,
        "grpc": GrpcConnector,
        "dynamodb": DynamoDBConnector,
        "cassandra": CassandraConnector,
        "clickhouse": ClickHouseConnector,
        "duckdb": DuckDBConnector,
        "neo4j": Neo4jConnector,
        # SaaS Applications & CRMs
        "salesforce": SalesforceConnector,
        "hubspot": HubSpotConnector,
        "stripe": StripeConnector,
        "google_sheets": GoogleSheetsConnector,
        "servicenow": ServiceNowConnector if 'ServiceNowConnector' in locals() else None,
        "jira": JiraConnector,
        "zendesk": ZendeskConnector,
        # Cloud Object Stores & RDBMS
        "azure_blob": AzureBlobConnector,
        "adls": AzureBlobConnector,
        "oracle": OracleConnector,
        "sqlserver": SQLServerConnector,
    }

    @classmethod
    def register(cls, connector_type: str, connector_cls: Type[BaseConnector]) -> None:
        """Register a custom or third-party connector class."""
        cls._registry[connector_type.lower()] = connector_cls

    @classmethod
    def get_connector_class(cls, connector_type: str) -> Type[BaseConnector]:
        """Retrieve connector class by type identifier."""
        norm_type = connector_type.lower()
        if norm_type not in cls._registry or cls._registry[norm_type] is None:
            raise ConnectorError(
                norm_type,
                f"Unsupported connector type: '{connector_type}'. Available: {[k for k, v in cls._registry.items() if v is not None]}"
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
        return sorted([k for k, v in cls._registry.items() if v is not None])


# Direct helper
def get_connector(
    connector_type: str,
    config: Dict[str, Any],
    credentials: Optional[Dict[str, Any]] = None
) -> BaseConnector:
    return ConnectorRegistry.create(connector_type, config, credentials)
