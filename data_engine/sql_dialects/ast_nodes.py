"""
DataFlowX SQL Abstract Syntax Tree (AST) Hierarchy
Defines object models for parsed SQL expressions: Select, Table, Column, Join, Where, GroupBy, Window, CaseWhen, FunctionCall, and BinaryOp.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class ASTNode(BaseModel):
    pass


class LiteralNode(ASTNode):
    value: Any
    data_type: str = "STRING"  # STRING, NUMBER, BOOLEAN, NULL


class IdentifierNode(ASTNode):
    name: str
    qualifier: Optional[str] = None  # e.g., schema or table alias


class BinaryOpNode(ASTNode):
    left: Any
    op: str  # '=', '!=', '<', '>', 'AND', 'OR', '+', '-', '*', '/', 'LIKE', 'IN'
    right: Any


class UnaryOpNode(ASTNode):
    op: str  # 'NOT', '-'
    operand: Any


class FunctionCallNode(ASTNode):
    name: str
    arguments: List[Any] = Field(default_factory=list)
    is_distinct: bool = False


class WindowSpecNode(ASTNode):
    partition_by: List[IdentifierNode] = Field(default_factory=list)
    order_by: List[Tuple[IdentifierNode, str]] = Field(default_factory=list)  # (col, 'ASC'/'DESC')
    frame_clause: Optional[str] = None


class WindowFunctionNode(ASTNode):
    function: FunctionCallNode
    over: WindowSpecNode


class CaseWhenBranch(BaseModel):
    condition: Any
    then_expr: Any


class CaseWhenNode(ASTNode):
    branches: List[CaseWhenBranch] = Field(default_factory=list)
    else_expr: Optional[Any] = None


class ColumnProjectionNode(ASTNode):
    expression: Any
    alias: Optional[str] = None


class TableRefNode(ASTNode):
    schema_name: Optional[str] = None
    table_name: str
    alias: Optional[str] = None


class JoinNode(ASTNode):
    join_type: str = "INNER"  # INNER, LEFT, RIGHT, FULL, CROSS
    table: TableRefNode
    condition: Optional[Any] = None


class SelectQueryAST(ASTNode):
    projections: List[ColumnProjectionNode] = Field(default_factory=list)
    from_table: Optional[TableRefNode] = None
    joins: List[JoinNode] = Field(default_factory=list)
    where_clause: Optional[Any] = None
    group_by: List[IdentifierNode] = Field(default_factory=list)
    having_clause: Optional[Any] = None
    order_by: List[Tuple[IdentifierNode, str]] = Field(default_factory=list)
    limit: Optional[int] = None
    offset: Optional[int] = None
    is_distinct: bool = False
