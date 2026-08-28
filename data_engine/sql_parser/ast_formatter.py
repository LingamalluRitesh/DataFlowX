"""
DataFlowX SQL AST Formatter & Pretty Printer
Emits formatted ANSI SQL strings from structured AST representations.
"""

from typing import Any
from data_engine.sql_parser.ast_nodes import (
    BinaryExpression, ColumnRef, FunctionCall, JoinClause, Literal,
    OrderByItem, SelectItem, SelectStatement, TableSource, UnaryExpression
)


class SQLFormatter:
    """Formats AST nodes into SQL strings."""

    @classmethod
    def format_node(cls, node: Any, indent_level: int = 0) -> str:
        if isinstance(node, SelectStatement):
            return cls.format_select(node, indent_level)
        elif isinstance(node, SelectItem):
            s = cls.format_node(node.expression, indent_level)
            if node.alias:
                s += f" AS {node.alias}"
            return s
        elif isinstance(node, ColumnRef):
            if node.table_name:
                return f"{node.table_name}.{node.column_name}"
            return node.column_name
        elif isinstance(node, Literal):
            if isinstance(node.value, str):
                return f"'{node.value}'"
            elif node.value is None:
                return "NULL"
            return str(node.value)
        elif isinstance(node, BinaryExpression):
            left_str = cls.format_node(node.left, indent_level)
            right_str = cls.format_node(node.right, indent_level)
            return f"({left_str} {node.op.value} {right_str})"
        elif isinstance(node, UnaryExpression):
            expr_str = cls.format_node(node.expr, indent_level)
            return f"{node.op.value} {expr_str}"
        elif isinstance(node, FunctionCall):
            args_str = ", ".join(cls.format_node(arg, indent_level) for arg in node.arguments)
            return f"{node.function_name.upper()}({args_str})"
        elif isinstance(node, TableSource):
            s = f"{node.schema_name}.{node.table_name}" if node.schema_name else node.table_name
            if node.alias:
                s += f" AS {node.alias}"
            return s
        elif isinstance(node, JoinClause):
            table_str = cls.format_node(node.right_table, indent_level)
            on_str = f" ON {cls.format_node(node.on_condition, indent_level)}" if node.on_condition else ""
            return f"{node.join_type.value} {table_str}{on_str}"
        elif isinstance(node, OrderByItem):
            expr_str = cls.format_node(node.expression, indent_level)
            direction = "ASC" if node.ascending else "DESC"
            return f"{expr_str} {direction}"
        return str(node)

    @classmethod
    def format_select(cls, stmt: SelectStatement, indent: int = 0) -> str:
        pad = "  " * indent
        lines = []

        distinct_kw = "DISTINCT " if stmt.is_distinct else ""
        proj_items = [cls.format_node(item, indent) for item in stmt.projection]
        lines.append(f"{pad}SELECT {distinct_kw}" + ", ".join(proj_items))

        if stmt.from_table:
            lines.append(f"{pad}FROM {cls.format_node(stmt.from_table, indent)}")

        for join in stmt.joins:
            lines.append(f"{pad}{cls.format_node(join, indent)}")

        if stmt.where_clause:
            lines.append(f"{pad}WHERE {cls.format_node(stmt.where_clause, indent)}")

        if stmt.group_by:
            gb_items = [cls.format_node(item, indent) for item in stmt.group_by]
            lines.append(f"{pad}GROUP BY " + ", ".join(gb_items))

        if stmt.having_clause:
            lines.append(f"{pad}HAVING {cls.format_node(stmt.having_clause, indent)}")

        if stmt.order_by:
            ob_items = [cls.format_node(item, indent) for item in stmt.order_by]
            lines.append(f"{pad}ORDER BY " + ", ".join(ob_items))

        if stmt.limit is not None:
            lines.append(f"{pad}LIMIT {stmt.limit}")

        return "\n".join(lines)
