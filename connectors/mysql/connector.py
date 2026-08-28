"""
DataFlowX MySQL Connector
Supports schema introspection, streaming cursors, and chunked extraction from MySQL / MariaDB databases.
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

MYSQL_TYPE_MAPPING = {
    "tinyint": FieldType.INTEGER,
    "smallint": FieldType.INTEGER,
    "mediumint": FieldType.INTEGER,
    "int": FieldType.INTEGER,
    "integer": FieldType.INTEGER,
    "bigint": FieldType.INTEGER,
    "float": FieldType.FLOAT,
    "double": FieldType.FLOAT,
    "decimal": FieldType.FLOAT,
    "numeric": FieldType.FLOAT,
    "char": FieldType.STRING,
    "varchar": FieldType.STRING,
    "tinytext": FieldType.STRING,
    "text": FieldType.STRING,
    "mediumtext": FieldType.STRING,
    "longtext": FieldType.STRING,
    "datetime": FieldType.TIMESTAMP,
    "timestamp": FieldType.TIMESTAMP,
    "date": FieldType.DATE,
    "json": FieldType.JSON,
    "blob": FieldType.BINARY,
    "tinyblob": FieldType.BINARY,
}


class MySQLConnector(BaseConnector):
    """Production connector for MySQL & MariaDB databases."""

    def __init__(self, config: Dict[str, Any], credentials: Optional[Dict[str, Any]] = None):
        super().__init__(config, credentials)
        self.connector_type = "mysql"
        self.host = self.config.get("host", "localhost")
        self.port = int(self.config.get("port", 3306))
        self.database = self.config.get("database", "mysql")
        self.username = self.credentials.get("username") or self.config.get("username", "root")
        self.password = self.credentials.get("password") or self.config.get("password", "")
        self.charset = self.config.get("charset", "utf8mb4")
        self._conn = None

    def _get_connection_params(self) -> Dict[str, Any]:
        return {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "user": self.username,
            "password": self.password,
            "charset": self.charset,
            "connect_timeout": 10,
        }

    def connect(self) -> bool:
        try:
            import pymysql
            import pymysql.cursors
            self._conn = pymysql.connect(
                cursorclass=pymysql.cursors.DictCursor,
                **self._get_connection_params()
            )
            self._is_connected = True
            return True
        except Exception as exc:
            self._is_connected = False
            logger.error(f"MySQL connection error to {self.host}:{self.port}/{self.database}: {exc}")
            raise ConnectorError(self.connector_type, str(exc))

    def disconnect(self) -> None:
        if self._conn and self._conn.open:
            self._conn.close()
        self._is_connected = False

    def test_connection(self) -> ConnectionTestResult:
        start = time.time()
        try:
            import pymysql
            conn = pymysql.connect(**self._get_connection_params())
            with conn.cursor() as cur:
                cur.execute("SELECT VERSION();")
                version = cur.fetchone()[0]
            conn.close()
            latency = (time.time() - start) * 1000
            return ConnectionTestResult(
                success=True,
                status="healthy",
                latency_ms=round(latency, 2),
                message="Successfully connected to MySQL database",
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
        if not self._is_connected or not self._conn.open:
            self.connect()

        tables_meta: List[TableMeta] = []
        with self._conn.cursor() as cur:
            cur.execute("""
                SELECT TABLE_NAME, TABLE_ROWS
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = %s AND TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME;
            """, (self.database,))
            tables = cur.fetchall()

            for tbl_info in tables:
                tbl_name = tbl_info["TABLE_NAME"]
                est_rows = tbl_info.get("TABLE_ROWS") or 0

                # Column introspection
                cur.execute("""
                    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY, ORDINAL_POSITION
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                    ORDER BY ORDINAL_POSITION;
                """, (self.database, tbl_name))
                cols = cur.fetchall()

                columns_meta = []
                pks = []
                for c in cols:
                    cname = c["COLUMN_NAME"]
                    dtype = c["DATA_TYPE"].lower()
                    is_pk = (c.get("COLUMN_KEY") == "PRI")
                    if is_pk:
                        pks.append(cname)

                    field_type = MYSQL_TYPE_MAPPING.get(dtype, FieldType.STRING)
                    columns_meta.append(ColumnMeta(
                        name=cname,
                        data_type=field_type,
                        is_nullable=(c["IS_NULLABLE"] == "YES"),
                        is_primary_key=is_pk,
                    ))

                tables_meta.append(TableMeta(
                    name=tbl_name,
                    schema_name=self.database,
                    columns=columns_meta,
                    estimated_row_count=est_rows,
                    primary_keys=pks
                ))

        return SchemaDiscoveryResult(
            source_type=self.connector_type,
            tables=tables_meta,
            metadata={"database": self.database}
        )

    def preview_data(self, target: str, limit: int = 50) -> List[Dict[str, Any]]:
        if not self._is_connected or not self._conn.open:
            self.connect()

        safe_target = target.replace("`", "``")
        safe_db = self.database.replace("`", "``")
        query = f"SELECT * FROM `{safe_db}`.`{safe_target}` LIMIT %s;"

        with self._conn.cursor() as cur:
            cur.execute(query, (limit,))
            return cur.fetchall()

    def extract_batch(
        self,
        target: str,
        chunk_size: int = 5000,
        incremental_column: Optional[str] = None,
        watermark_value: Optional[Any] = None,
    ) -> Generator[ExtractionChunk, None, None]:
        if not self._is_connected or not self._conn.open:
            self.connect()

        safe_target = target.replace("`", "``")
        safe_db = self.database.replace("`", "``")

        query = f"SELECT * FROM `{safe_db}`.`{safe_target}`"
        params: List[Any] = []

        if incremental_column and watermark_value is not None:
            safe_col = incremental_column.replace("`", "``")
            query += f" WHERE `{safe_col}` > %s ORDER BY `{safe_col}` ASC"
            params.append(watermark_value)
        elif incremental_column:
            safe_col = incremental_column.replace("`", "``")
            query += f" ORDER BY `{safe_col}` ASC"

        import pymysql.cursors
        stream_cur = self._conn.cursor(pymysql.cursors.SSDictCursor)
        stream_cur.execute(query, params)

        chunk_idx = 0
        latest_watermark = watermark_value

        while True:
            records = stream_cur.fetchmany(chunk_size)
            if not records:
                break

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

        stream_cur.close()
