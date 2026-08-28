"""
DataFlowX Cypher Graph Query Language Mini-Parser
Parses declarative Cypher pattern queries (e.g. `MATCH (u:User)-[r:TRANSFERRED_TO]->(m:Merchant) RETURN u.id, m.name`).
"""

import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CypherPattern(BaseModel):
    source_alias: str
    source_label: Optional[str] = None
    relationship_alias: Optional[str] = None
    relationship_type: Optional[str] = None
    target_alias: str
    target_label: Optional[str] = None


class CypherQuery(BaseModel):
    pattern: CypherPattern
    where_predicate: Optional[str] = None
    return_columns: List[str] = Field(default_factory=list)


class CypherMiniParser:
    """Parses lightweight Cypher graph queries."""

    PATTERN_REGEX = re.compile(
        r"MATCH\s*\((?P<src_alias>\w+)(?::(?P<src_label>\w+))?\)\s*-\[\s*(?P<rel_alias>\w+)?(?::(?P<rel_type>\w+))?\s*\]->\s*\((?P<tgt_alias>\w+)(?::(?P<tgt_label>\w+))?\)\s*(?:WHERE\s+(?P<where_clause>.+?))?\s*RETURN\s+(?P<ret_cols>.+)",
        re.IGNORECASE
    )

    @classmethod
    def parse_query(cls, cypher_sql: str) -> Optional[CypherQuery]:
        match = cls.PATTERN_REGEX.search(cypher_sql.strip())
        if not match:
            return None

        gd = match.groupdict()
        pattern = CypherPattern(
            source_alias=gd.get("src_alias", "a"),
            source_label=gd.get("src_label"),
            relationship_alias=gd.get("rel_alias"),
            relationship_type=gd.get("rel_type"),
            target_alias=gd.get("tgt_alias", "b"),
            target_label=gd.get("tgt_label")
        )

        ret_raw = gd.get("ret_cols", "")
        cols = [c.strip() for c in ret_raw.split(",") if c.strip()]

        return CypherQuery(
            pattern=pattern,
            where_predicate=gd.get("where_clause"),
            return_columns=cols
        )
