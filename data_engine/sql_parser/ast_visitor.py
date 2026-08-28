"""
DataFlowX SQL AST Visitor & Column Lineage Extractor
Traverses SQL ASTs to extract referenced tables, source columns, and expression dependencies.
"""

from typing import Any, List, Set
from data_engine.sql_parser.ast_nodes import (
    ASTNode, BinaryExpression, ColumnRef, FunctionCall, JoinClause,
    SelectItem, SelectStatement, TableSource, UnaryExpression
)


class ASTVisitor:
    """Base AST visitor pattern."""

    def visit(self, node: Any) -> Any:
        if node is None:
            return None
        method_name = f"visit_{node.__class__.__name__}"
        visitor_fn = getattr(self, method_name, self.generic_visit)
        return visitor_fn(node)

    def generic_visit(self, node: Any) -> Any:
        if isinstance(node, ASTNode):
            for field, val in node.__dict__.items():
                if isinstance(val, list):
                    for item in val:
                        self.visit(item)
                else:
                    self.visit(val)
        return None


class TableAndColumnExtractor(ASTVisitor):
    """Extracts all table and column names referenced in an AST."""

    def __init__(self):
        self.tables: Set[str] = set()
        self.columns: Set[str] = set()

    def visit_TableSource(self, node: TableSource):
        t_name = f"{node.schema_name}.{node.table_name}" if node.schema_name else node.table_name
        self.tables.add(t_name)
        self.generic_visit(node)

    def visit_ColumnRef(self, node: ColumnRef):
        c_name = f"{node.table_name}.{node.column_name}" if node.table_name else node.column_name
        self.columns.add(c_name)
        self.generic_visit(node)

    @classmethod
    def extract_dependencies(cls, ast: ASTNode) -> tuple[Set[str], Set[str]]:
        extractor = cls()
        extractor.visit(ast)
        return extractor.tables, extractor.columns
