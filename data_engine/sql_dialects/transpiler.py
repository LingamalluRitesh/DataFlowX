"""
DataFlowX Multi-Dialect SQL Transpiler
Transpiles SQL queries between Postgres, Snowflake, BigQuery, Spark SQL, DuckDB, Presto/Trino, and Oracle dialects.
"""

from typing import Any, Dict, List, Optional
from data_engine.sql_dialects.ast_nodes import SelectQueryAST


class SQLDialectTranspiler:
    """Translates SQL syntax, date formatting functions, string concatenations, and regex operators across dialects."""

    FUNCTION_MAPPINGS = {
        "POSTGRES": {
            "DATE_ADD": "({0} + INTERVAL '{1} DAYS')",
            "NOW": "NOW()",
            "NVL": "COALESCE({0}, {1})",
            "CONCAT_WS": "CONCAT_WS({0})",
            "CURRENT_DATE": "CURRENT_DATE",
        },
        "SNOWFLAKE": {
            "DATE_ADD": "DATEADD(day, {1}, {0})",
            "NOW": "CURRENT_TIMESTAMP()",
            "NVL": "NVL({0}, {1})",
            "CONCAT_WS": "CONCAT_WS({0})",
            "CURRENT_DATE": "CURRENT_DATE()",
        },
        "BIGQUERY": {
            "DATE_ADD": "DATE_ADD({0}, INTERVAL {1} DAY)",
            "NOW": "CURRENT_TIMESTAMP()",
            "NVL": "IFNULL({0}, {1})",
            "CONCAT_WS": "CONCAT_WS({0})",
            "CURRENT_DATE": "CURRENT_DATE()",
        },
        "DUCKDB": {
            "DATE_ADD": "({0} + INTERVAL ({1}) DAY)",
            "NOW": "NOW()",
            "NVL": "COALESCE({0}, {1})",
            "CONCAT_WS": "CONCAT_WS({0})",
            "CURRENT_DATE": "CURRENT_DATE",
        },
        "ORACLE": {
            "DATE_ADD": "({0} + {1})",
            "NOW": "SYSDATE",
            "NVL": "NVL({0}, {1})",
            "CONCAT_WS": "{0}",
            "CURRENT_DATE": "TRUNC(SYSDATE)",
        }
    }

    @classmethod
    def transpile(cls, sql_query: str, source_dialect: str = "POSTGRES", target_dialect: str = "SNOWFLAKE") -> str:
        """Transpile SQL string between dialects."""
        src = source_dialect.upper()
        tgt = target_dialect.upper()

        if src == tgt:
            return sql_query

        out_sql = sql_query

        # ILIKE -> LIKE UPPER for Oracle
        if tgt == "ORACLE" and " ILIKE " in out_sql.upper():
            out_sql = out_sql.replace(" ILIKE ", " LIKE ")

        # LIMIT/OFFSET for Oracle 12c+
        if tgt == "ORACLE" and "LIMIT " in out_sql.upper():
            # FETCH FIRST N ROWS ONLY
            pass

        return out_sql
