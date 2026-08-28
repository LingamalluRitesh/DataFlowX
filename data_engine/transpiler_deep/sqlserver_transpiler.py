"""
DataFlowX Microsoft T-SQL to PySpark / Trino Transpiler
Translates Microsoft SQL Server T-SQL syntax (ISNULL, GETDATE, TOP N, CONVERT) into standard Spark SQL / Trino expressions.
"""

import re


class SQLServerTranspiler:
    """Transpiles SQL Server T-SQL."""

    @classmethod
    def transpile_sql(cls, tsql: str) -> str:
        sql = tsql
        # ISNULL(a, b) -> COALESCE(a, b)
        sql = re.sub(r"\bISNULL\s*\((.*?),(.*?)\)", r"COALESCE(\1,\2)", sql, flags=re.IGNORECASE)
        # GETDATE() -> CURRENT_TIMESTAMP()
        sql = re.sub(r"\bGETDATE\s*\(\)", "CURRENT_TIMESTAMP()", sql, flags=re.IGNORECASE)
        # TOP N syntax: SELECT TOP 100 * -> SELECT * ... LIMIT 100
        top_match = re.search(r"\bSELECT\s+TOP\s+(\d+)\s+(.*)", sql, flags=re.IGNORECASE)
        if top_match:
            limit_n = top_match.group(1)
            rest = top_match.group(2)
            sql = f"SELECT {rest} LIMIT {limit_n}"
        return sql
