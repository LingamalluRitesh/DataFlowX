"""
DataFlowX Lineage Graph Exporter
Renders column and table lineage graphs into Graphviz DOT syntax, Marquez standard lineage JSON, and OpenLineage events.
"""

from typing import List
from data_engine.lineage_deep.sql_lineage_parser import ColumnLineageEdge


class LineageGraphExporter:
    """Exports column lineage to various industry standard formats."""

    @classmethod
    def to_graphviz_dot(cls, edges: List[ColumnLineageEdge]) -> str:
        lines = ["digraph ColumnLineage {", '  rankdir="LR";', '  node [shape="box", fontname="Helvetica"];']
        for e in edges:
            src = f'"{e.source_table}.{e.source_column}"'
            dst = f'"{e.target_table}.{e.target_column}"'
            lines.append(f"  {src} -> {dst} [label=\"{e.transformation_type}\"];")
        lines.append("}")
        return "\n".join(lines)
