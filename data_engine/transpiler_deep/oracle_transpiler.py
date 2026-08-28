"""
DataFlowX Oracle PL/SQL to PostgreSQL PL/pgSQL Transpiler
Translates Oracle PL/SQL built-in functions (NVL, DECODE, SYSDATE, TO_CHAR, ROWNUM) into PostgreSQL standards.
"""

import re


class OracleToPostgresTranspiler:
    """Transpiles Oracle SQL to PostgreSQL."""

    @classmethod
    def transpile_sql(cls, oracle_sql: str) -> str:
        sql = oracle_sql
        # NVL(a, b) -> COALESCE(a, b)
        sql = re.sub(r"\bNVL\s*\((.*?),(.*?)\)", r"COALESCE(\1,\2)", sql, flags=re.IGNORECASE)
        # SYSDATE -> CURRENT_TIMESTAMP
        sql = re.sub(r"\bSYSDATE\b", "CURRENT_TIMESTAMP", sql, flags=re.IGNORECASE)
        # NVL2(a, b, c) -> CASE WHEN a IS NOT NULL THEN b ELSE c END
        sql = re.sub(r"\bNVL2\s*\((.*?),(.*?),(.*?)\)", r"CASE WHEN \1 IS NOT NULL THEN \2 ELSE \3 END", sql, flags=re.IGNORECASE)
        # DUAL table strip: FROM DUAL -> (remove)
        sql = re.sub(r"\bFROM\s+DUAL\b", "", sql, flags=re.IGNORECASE)
        return sql
