"""
DataFlowX Dynamic DAG Graph Compiler & Validator
Compiles declarative JSON/YAML workflow configurations into executable DAG graphs, computing topological sorts and detecting cycle conditions.
"""

from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from backend.core.exceptions import ValidationError
from backend.core.logging import get_logger

logger = get_logger(__name__)


class DynamicDAGSpec(BaseModel):
    pipeline_name: str
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)


class DynamicDAGCompiler:
    """Compiles and validates dynamic DAG definitions."""

    @staticmethod
    def compile_and_validate(spec: DynamicDAGSpec) -> List[str]:
        """Validate topological acyclic order and return execution sequence."""
        adj: Dict[str, List[str]] = {n["id"]: [] for n in spec.nodes}
        in_degree: Dict[str, int] = {n["id"]: 0 for n in spec.nodes}

        for e in spec.edges:
            src = e["source"]
            tgt = e["target"]
            if src in adj and tgt in in_degree:
                adj[src].append(tgt)
                in_degree[tgt] += 1

        # Kahn's algorithm
        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        topo_order = []

        while queue:
            curr = queue.pop(0)
            topo_order.append(curr)
            for neighbor in adj.get(curr, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(topo_order) != len(spec.nodes):
            raise ValidationError("Cycle detected in DAG definition. Graph must be a Directed Acyclic Graph.")

        logger.info(f"Successfully compiled DAG '{spec.pipeline_name}' with execution order: {topo_order}")
        return topo_order
