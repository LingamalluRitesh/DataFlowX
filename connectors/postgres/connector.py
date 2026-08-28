"""
DataFlowX PostgreSQL Connector
Supports connection pooling, information_schema introspection, and chunked cursor extraction.
"""

from contextlib import contextmanager
from datetime import datetime, timezone
import time
from typing import Any, Dict, Generator, List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
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

PG_TYPE_MAPPING = {
    "integer": FieldType.INTEGER,
    "smallint": FieldType.INTEGER,
    "bigint": FieldType.INTEGER,
    "serial": FieldType.INTEGER,
    "bigserial": FieldType.INTEGER,
    "real": FieldType.FLOAT,
    "double precision": FieldType.FLOAT,
    "numeric": FieldType.FLOAT,
    "decimal": FieldType.FLOAT,
    "boolean": FieldType.BOOLEAN,
    "character varying": FieldType.STRING,
    "varchar": FieldType.STRING,
    "character": FieldType.STRING,
    "char": FieldType.STRING,
    "text": FieldType.STRING,
    "timestamp without time zone": FieldType.TIMESTAMP,
    "timestamp with time zone": FieldType.TIMESTAMP,
    "date": FieldType.DATE,
    "json": FieldType.JSON,
    "jsonb": FieldType.JSON,
    "bytea": FieldType.BINARY,
    "ARRAY": FieldType.ARRAY,
}


class PostgresConnector(BaseConnector):
    """Production connector for PostgreSQL databases."""

    def __init__(self, config: Dict[str, Any], credentials: Optional[Dict[str, Any]] = None):
        super().__init__(config, credentials)
        self.connector_type = "postgres"
        self.host = self.config.get("host", "localhost")
        self.port = int(self.config.get("port", 5432))
        self.database = self.config.get("database", "postgres")
        self.schema = self.config.get("schema", "public")
        self.username = self.credentials.get("username") or self.config.get("username", "postgres")
        self.password = self.credentials.get("password") or self.config.get("password", "")
        self.sslmode = self.config.get("sslmode", "prefer")
        self._conn = None

    def _get_connection_params(self) -> Dict[str, Any]:
        return {
            "host": self.host,
            "port": self.port,
            "dbname": self.database,
            "user": self.username,
            "password": self.password,
            "sslmode": self.sslmode,
            "connect_timeout": 10,
        }

    def connect(self) -> bool:
        try:
            self._conn = psycopg2.connect(**self._get_connection_params())
            self._is_connected = True
            return True
        except Exception as exc:
            self._is_connected = False
            logger.error(f"PostgreSQL connection failed to {self.host}:{self.port}/{self.database}: {exc}")
            raise ConnectorError(self.connector_type, str(exc))

    def disconnect(self) -> None:
        if self._conn and not self._conn.closed:
            self._conn.close()
        self._is_connected = False

    def test_connection(self) -> ConnectionTestResult:
        start = time.time()
        try:
            conn = psycopg2.connect(**self._get_connection_params())
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
            conn.close()
            latency = (time.time() - start) * 1000
            return ConnectionTestResult(
                success=True,
                status="healthy",
                latency_ms=round(latency, 2),
                message="Successfully connected to PostgreSQL database",
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
        if not self._is_connected or self._conn.closed:
            self.connect()

        tables_meta: List[TableMeta] = []
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Query table list
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """, (self.schema,))
            tables = [r["table_name"] for r in cur.fetchall()]

            for tbl in tables:
                # Query columns
                cur.execute("""
                    SELECT 
                        c.column_name,
                        c.data_type,
                        c.is_nullable,
                        c.column_default,
                        c.ordinal_position
                    FROM information_schema.columns c
                    WHERE c.table_schema = %s AND c.table_name = %s
                    ORDER BY c.ordinal_position;
                """, (self.schema, tbl))
                columns_raw = cur.fetchall()

                # Query primary keys
                cur.execute("""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                      AND tc.table_schema = %s
                      AND tc.table_name = %s;
                """, (self.schema, tbl))
                pk_columns = {r["column_name"] for r in cur.fetchall()}

                # Estimate row count
                cur.execute("""
                    SELECT reltuples::bigint AS estimate
                    FROM pg_class C
                    JOIN pg_namespace N ON (N.oid = C.relnamespace)
                    WHERE N.nspname = %s AND C.relname = %s;
                """, (self.schema, tbl))
                est_res = cur.fetchone()
                est_rows = est_res["estimate"] if est_res and est_res["estimate"] is not None else 0

                columns_meta = []
                for col in columns_raw:
                    cname = col["column_name"]
                    raw_type = col["data_type"].lower()
                    field_type = PG_TYPE_MAPPING.get(raw_type, FieldType.STRING)
                    columns_meta.append(ColumnMeta(
                        name=cname,
                        data_type=field_type,
                        is_nullable=(col["is_nullable"] == "YES"),
                        is_primary_key=(cname in pk_columns),
                    ))

                tables_meta.append(TableMeta(
                    name=tbl,
                    schema_name=self.schema,
                    columns=columns_meta,
                    estimated_row_count=est_rows,
                    primary_keys=list(pk_columns)
                ))

        return SchemaDiscoveryResult(
            source_type=self.connector_type,
            tables=tables_meta,
            metadata={"database": self.database, "schema": self.schema}
        )

    def preview_data(self, target: str, limit: int = 50) -> List[Dict[str, Any]]:
        if not self._is_connected or self._conn.closed:
            self.connect()

        safe_target = target.replace('"', '""')
        safe_schema = self.schema.replace('"', '""')
        query = f'SELECT * FROM "{safe_schema}"."{safe_target}" LIMIT %s;'

        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (limit,))
            rows = cur.fetchall()
            return [dict(r) for r in rows]

    def extract_batch(
        self,
        target: str,
        chunk_size: int = 5000,
        incremental_column: Optional[str] = None,
        watermark_value: Optional[Any] = None,
    ) -> Generator[ExtractionChunk, None, None]:
        if not self._is_connected or self._conn.closed:
            self.connect()

        safe_target = target.replace('"', '""')
        safe_schema = self.schema.replace('"', '""')

        cursor_name = f"dfx_cur_{int(time.time())}"
        server_cur = self._conn.cursor(name=cursor_name, cursor_factory=RealDictCursor)

        query = f'SELECT * FROM "{safe_schema}"."{safe_target}"'
        params: List[Any] = []

        if incremental_column and watermark_value is not None:
            safe_col = incremental_column.replace('"', '""')
            query += f' WHERE "{safe_col}" > %s ORDER BY "{safe_col}" ASC'
            params.append(watermark_value)
        elif incremental_column:
            safe_col = incremental_column.replace('"', '""')
            query += f' ORDER BY "{safe_col}" ASC'

        server_cur.execute(query, params)

        chunk_idx = 0
        latest_watermark = watermark_value

        while True:
            records = server_cur.fetchmany(chunk_size)
            if not records:
                break

            record_dicts = [dict(r) for r in records]
            if incremental_column and record_dicts:
                latest_watermark = record_dicts[-1].get(incremental_column, latest_watermark)

            is_last = len(record_dicts) < chunk_size
            yield ExtractionChunk(
                chunk_index=chunk_idx,
                record_count=len(record_dicts),
                data=record_dicts,
                is_last_chunk=is_last,
                watermark_value=latest_watermark
            )
            chunk_idx += 1
            if is_last:
                break

        server_cur.close()
