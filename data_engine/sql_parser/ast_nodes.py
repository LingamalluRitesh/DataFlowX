"""
DataFlowX SQL Abstract Syntax Tree (AST) Nodes
Defines typed AST nodes representing ANSI SQL expressions, queries, statements, and clauses.
"""

from abc import ABC
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ASTNode(BaseModel):
    """Base AST Node."""
    pass


class SqlDataType(str, Enum):
    INT = "INT"
    BIGINT = "BIGINT"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    JSON = "JSON"
    ARRAY = "ARRAY"


class Identifier(ASTNode):
    name: str
    quote_char: Optional[str] = None


class ColumnRef(ASTNode):
    column_name: str
    table_name: Optional[str] = None
    schema_name: Optional[str] = None


class Literal(ASTNode):
    value: Any
    data_type: SqlDataType


class BinaryOp(str, Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    EQ = "="
    NEQ = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    AND = "AND"
    OR = "OR"
    LIKE = "LIKE"
    ILIKE = "ILIKE"


class BinaryExpression(ASTNode):
    left: Any
    op: BinaryOp
    right: Any


class UnaryOp(str, Enum):
    NOT = "NOT"
    NEG = "-"
    IS_NULL = "IS NULL"
    IS_NOT_NULL = "IS NOT NULL"


class UnaryExpression(ASTNode):
    op: UnaryOp
    expr: Any


class FunctionCall(ASTNode):
    function_name: str
    arguments: List[Any] = Field(default_factory=list)
    is_distinct: bool = False


class WhenClause(ASTNode):
    condition: Any
    result: Any


class CaseExpression(ASTNode):
    case_expr: Optional[Any] = None
    when_clauses: List[WhenClause] = Field(default_factory=list)
    else_result: Optional[Any] = None


class SelectItem(ASTNode):
    expression: Any
    alias: Optional[str] = None


class TableSource(ASTNode):
    table_name: str
    schema_name: Optional[str] = None
    alias: Optional[str] = None


class JoinType(str, Enum):
    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL OUTER JOIN"
    CROSS = "CROSS JOIN"


class JoinClause(ASTNode):
    join_type: JoinType
    right_table: Any
    on_condition: Optional[Any] = None
    using_columns: List[str] = Field(default_factory=list)


class OrderByItem(ASTNode):
    expression: Any
    ascending: bool = True
    nulls_first: bool = False


class SelectStatement(ASTNode):
    is_distinct: bool = False
    projection: List[SelectItem] = Field(default_factory=list)
    from_table: Optional[Any] = None
    joins: List[JoinClause] = Field(default_factory=list)
    where_clause: Optional[Any] = None
    group_by: List[Any] = Field(default_factory=list)
    having_clause: Optional[Any] = None
    order_by: List[OrderByItem] = Field(default_factory=list)
    limit: Optional[int] = None
    offset: Optional[int] = None


class SetOpType(str, Enum):
    UNION = "UNION"
    UNION_ALL = "UNION ALL"
    INTERSECT = "INTERSECT"
    EXCEPT = "EXCEPT"


class SetOperationStatement(ASTNode):
    left_statement: Any
    op: SetOpType
    right_statement: Any


class CTEClause(ASTNode):
    name: str
    query: Any
    column_aliases: List[str] = Field(default_factory=list)


class WithStatement(ASTNode):
    ctes: List[CTEClause] = Field(default_factory=list)
    main_statement: Any
    is_recursive: bool = False


class CreateTableStatement(ASTNode):
    table_name: str
    schema_name: Optional[str] = None
    columns: Dict[str, SqlDataType] = Field(default_factory=dict)
    partition_by: List[str] = Field(default_factory=list)
    cluster_by: List[str] = Field(default_factory=list)
    if_not_exists: bool = True


class InsertStatement(ASTNode):
    target_table: str
    target_columns: List[str] = Field(default_factory=list)
    source_query: Optional[SelectStatement] = None
    values_list: List[List[Any]] = Field(default_factory=list)
