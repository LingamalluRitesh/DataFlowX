"""
DataFlowX Data Source Connectors
"""

from connectors.base import (
    BaseConnector,
    ColumnMeta,
    ConnectionTestResult,
    ConnectorType,
    ExtractionChunk,
    FieldType,
    SchemaDiscoveryResult,
    TableMeta,
)
from connectors.csv import CsvConnector
from connectors.excel import ExcelConnector
from connectors.json import JsonConnector
from connectors.kafka import KafkaConnector
from connectors.mongodb import MongoConnector
from connectors.mysql import MySQLConnector
from connectors.postgres import PostgresConnector
from connectors.registry import ConnectorRegistry, get_connector
from connectors.rest import RestApiConnector
from connectors.s3 import MinIOConnector, S3Connector

__all__ = [
    "BaseConnector",
    "ConnectorType",
    "FieldType",
    "ColumnMeta",
    "TableMeta",
    "SchemaDiscoveryResult",
    "ConnectionTestResult",
    "ExtractionChunk",
    "PostgresConnector",
    "MySQLConnector",
    "MongoConnector",
    "RestApiConnector",
    "CsvConnector",
    "ExcelConnector",
    "JsonConnector",
    "KafkaConnector",
    "S3Connector",
    "MinIOConnector",
    "ConnectorRegistry",
    "get_connector",
]
