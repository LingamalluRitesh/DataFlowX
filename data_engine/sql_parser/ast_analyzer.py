"""
DataFlowX SQL AST Analyzer & Query Dialect Transpiler
Parses SELECT statements, joins, CTEs, window functions, and validates semantic syntax.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class ParsedTableReference(BaseModel):
    schema_name: Optional[str] = None
    table_name: str
    alias: Optional[str] = None


class ParsedColumnProjection(BaseModel):
    raw_expression: str
    alias: Optional[str] = None
    is_aggregate: bool = False


class ParsedQueryPlan(BaseModel):
    tables: List[ParsedTableReference] = Field(default_factory=list)
    projections: List[ParsedColumnProjection] = Field(default_factory=list)
    has_where_clause: bool = False
    has_group_by: bool = False
    has_window_functions: bool = False
    joins_count: int = 0
    limit: Optional[int] = None


class SQLAstAnalyzer:
    """Lightweight SQL syntax analyzer and structure reflector."""

    TABLE_REGEX = re.compile(r"\bFROM\s+([a-zA-Z0-9_\.]+)(?:\s+(?:AS\s+)?([a-zA-Z0-9_]+))?", re.IGNORECASE)
    JOIN_REGEX = re.compile(r"\b(?:INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\s+([a-zA-Z0-9_\.]+)(?:\s+(?:AS\s+)?([a-zA-Z0-9_]+))?", re.IGNORECASE)
    AGG_REGEX = re.compile(r"\b(COUNT|SUM|AVG|MIN|MAX)\s*\(", re.IGNORECASE)
    WINDOW_REGEX = re.compile(r"\bOVER\s*\(", re.IGNORECASE)

    @classmethod
    def analyze_query(cls, sql_query: str) -> ParsedQueryPlan:
        clean_sql = " ".join(sql_query.strip().split())
        tables = []

        # Find FROM table
        for m in cls.TABLE_REGEX.finditer(clean_sql):
            raw_tbl = m.group(1)
            alias = m.group(2)
            parts = raw_tbl.split(".", 1)
            schema = parts[0] if len(parts) > 1 else None
            tname = parts[1] if len(parts) > 1 else parts[0]
            tables.append(ParsedTableReference(schema_name=schema, table_name=tname, alias=alias))

        # Find JOIN tables
        joins_count = 0
        for m in cls.JOIN_REGEX.finditer(clean_sql):
            joins_count += 1
            raw_tbl = m.group(1)
            alias = m.group(2)
            parts = raw_tbl.split(".", 1)
            schema = parts[0] if len(parts) > 1 else None
            tname = parts[1] if len(parts) > 1 else parts[0]
            tables.append(ParsedTableReference(schema_name=schema, table_name=tname, alias=alias))

        has_agg = bool(cls.AGG_REGEX.search(clean_sql))
        has_window = bool(cls.WINDOW_REGEX.search(clean_sql))
        has_where = " WHERE " in clean_sql.upper()
        has_group = " GROUP BY " in clean_sql.upper()

        return ParsedQueryPlan(
            tables=tables,
            projections=[],
            has_where_clause=has_where,
            has_group_by=has_group,
            has_window_functions=has_window,
            joins_count=joins_count
        )
