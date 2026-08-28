"""
DataFlowX PostgreSQL Dialect SQL Generator
Generates valid PostgreSQL SQL statements from AST nodes with JSONB operators (->>), array constructors, and ILIKE patterns.
"""

from typing import Any, List, Optional
from data_engine.sql_dialects.ast_nodes import (
    ColumnProjectionNode,
    FunctionCallNode,
    IdentifierNode,
    LiteralNode,
    SelectQueryAST,
    TableRefNode,
)


class PostgresDialectGenerator:
    """Generates PostgreSQL SQL statements from SelectQueryAST."""

    @classmethod
    def generate(cls, ast: SelectQueryAST) -> str:
        sql = "SELECT "
        if ast.is_distinct:
            sql += "DISTINCT "

        proj_strs = []
        for p in ast.projections:
            expr_str = cls._format_expr(p.expression)
            if p.alias:
                proj_strs.append(f'{expr_str} AS "{p.alias}"')
            else:
                proj_strs.append(expr_str)
        sql += ", ".join(proj_strs) if proj_strs else "*"

        if ast.from_table:
            sql += f" FROM {cls._format_table(ast.from_table)}"

        for j in ast.joins:
            sql += f" {j.join_type} {cls._format_table(j.table)}"
            if j.condition:
                sql += f" ON {cls._format_expr(j.condition)}"

        if ast.where_clause:
            sql += f" WHERE {cls._format_expr(ast.where_clause)}"

        if ast.group_by:
            sql += " GROUP BY " + ", ".join(cls._format_expr(g) for g in ast.group_by)

        if ast.order_by:
            sql += " ORDER BY " + ", ".join(f"{cls._format_expr(o[0])} {o[1]}" for o in ast.order_by)

        if ast.limit is not None:
            sql += f" LIMIT {ast.limit}"

        return sql + ";"

    @classmethod
    def _format_expr(cls, expr: Any) -> str:
        if isinstance(expr, IdentifierNode):
            return f'"{expr.name}"'
        elif isinstance(expr, LiteralNode):
            if expr.data_type == "STRING":
                return f"'{expr.value}'"
            return str(expr.value)
        elif isinstance(expr, FunctionCallNode):
            args = ", ".join(cls._format_expr(a) for a in expr.arguments)
            return f"{expr.name}({args})"
        return str(expr)

    @classmethod
    def _format_table(cls, tbl: TableRefNode) -> str:
        t = f'"{tbl.schema_name}"."{tbl.table_name}"' if tbl.schema_name else f'"{tbl.table_name}"'
        if tbl.alias:
            t += f' AS "{tbl.alias}"'
        return t
