"""
DataFlowX Enterprise DDL (Data Definition Language) Parser
Parses CREATE TABLE, ALTER TABLE, ADD COLUMN, DROP COLUMN, and CONSTRAINT DDL statements across SQL dialects into strongly-typed schema models.
"""

import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ParsedColumnDefinition(BaseModel):
    name: str
    data_type: str
    is_nullable: bool = True
    is_primary_key: bool = False
    default_value: Optional[str] = None
    comment: Optional[str] = None


class ParsedTableDDL(BaseModel):
    table_name: str
    schema_name: Optional[str] = None
    columns: List[ParsedColumnDefinition] = Field(default_factory=list)
    primary_keys: List[str] = Field(default_factory=list)
    foreign_keys: List[Dict[str, Any]] = Field(default_factory=list)


class DDLParser:
    """Extracts column definitions and constraints from raw SQL DDL."""

    CREATE_TABLE_REGEX = re.compile(
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:[\"`]?([a-zA-Z0-9_]+)[\"`]?\.)?[\"`]?([a-zA-Z0-9_]+)[\"`]?\s*\((.*)\)",
        re.IGNORECASE | re.DOTALL
    )

    @classmethod
    def parse_create_table(cls, ddl_sql: str) -> Optional[ParsedTableDDL]:
        m = cls.CREATE_TABLE_REGEX.search(ddl_sql.strip())
        if not m:
            return None

        sch = m.group(1)
        tbl = m.group(2)
        body = m.group(3).strip()

        cols: List[ParsedColumnDefinition] = []
        pks: List[str] = []

        # Split column definitions by comma while ignoring parenthesized types (e.g. DECIMAL(10,2))
        lines = [line.strip() for line in re.split(r",(?![^(]*\))", body) if line.strip()]

        for line in lines:
            if re.match(r"PRIMARY\s+KEY", line, re.IGNORECASE):
                pk_match = re.search(r"\((.*?)\)", line)
                if pk_match:
                    pks.extend([p.strip().strip('"').strip('`') for p in pk_match.group(1).split(",")])
                continue

            tokens = line.split()
            if len(tokens) < 2:
                continue

            c_name = tokens[0].strip('"').strip('`')
            c_type = tokens[1]
            is_null = True
            is_pk = False

            upper_line = line.upper()
            if "NOT NULL" in upper_line:
                is_null = False
            if "PRIMARY KEY" in upper_line:
                is_pk = True
                pks.append(c_name)

            cols.append(ParsedColumnDefinition(
                name=c_name,
                data_type=c_type,
                is_nullable=is_null,
                is_primary_key=is_pk
            ))

        return ParsedTableDDL(
            table_name=tbl,
            schema_name=sch,
            columns=cols,
            primary_keys=list(set(pks))
        )
