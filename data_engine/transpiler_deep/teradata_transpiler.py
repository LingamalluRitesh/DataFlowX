"""
DataFlowX Teradata to Snowflake / DuckDB Transpiler
Translates Teradata legacy SQL syntax (QUALIFY, CSUM, ZEROIFNULL, SEL, DATE formats) into modern Snowflake / DuckDB ANSI SQL.
"""

import re
from typing import Dict, List


class TeradataTranspiler:
    """Transpiles Teradata SQL into Snowflake SQL."""

    @classmethod
    def transpile_sql(cls, teradata_sql: str) -> str:
        sql = teradata_sql
        # SEL -> SELECT
        sql = re.sub(r"\bSEL\b", "SELECT", sql, flags=re.IGNORECASE)
        # ZEROIFNULL(x) -> COALESCE(x, 0)
        sql = re.sub(r"\bZEROIFNULL\s*\((.*?)\)", r"COALESCE(\1, 0)", sql, flags=re.IGNORECASE)
        # NULLIFZERO(x) -> NULLIF(x, 0)
        sql = re.sub(r"\bNULLIFZERO\s*\((.*?)\)", r"NULLIF(\1, 0)", sql, flags=re.IGNORECASE)
        # CSUM(col, sort_col) -> SUM(col) OVER (ORDER BY sort_col ROWS UNBOUNDED PRECEDING)
        sql = re.sub(r"\bCSUM\s*\((.*?),\s*(.*?)\)", r"SUM(\1) OVER (ORDER BY \2 ROWS UNBOUNDED PRECEDING)", sql, flags=re.IGNORECASE)
        return sql
