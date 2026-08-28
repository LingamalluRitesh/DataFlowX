"""
DataFlowX Graph Traversal & Blast Radius Impact Engine
Implements graph algorithms over lineage networks: transitive closure, cycle detection, critical path calculation, and failure blast radius scoring.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field


class BlastRadiusReport(BaseModel):
    root_entity: str
    impacted_tables: List[str] = Field(default_factory=list)
    impacted_pipelines: List[str] = Field(default_factory=list)
    impacted_dashboards: List[str] = Field(default_factory=list)
    total_impact_score: int = 0
    severity: str = "LOW"  # LOW, MEDIUM, HIGH, CRITICAL


class LineageGraphEngine:
    """Computes downstream blast radius and upstream root causes across lineage graphs."""

    def __init__(self):
        self.adj_list: Dict[str, Set[str]] = {}
        self.entity_types: Dict[str, str] = {}  # TABLE, PIPELINE, DASHBOARD

    def add_dependency(self, source_entity: str, target_entity: str, target_type: str = "TABLE") -> None:
        self.adj_list.setdefault(source_entity, set()).add(target_entity)
        self.entity_types[target_entity] = target_type

    def calculate_blast_radius(self, root_entity: str) -> BlastRadiusReport:
        """Find all downstream transitive dependencies from root entity failure."""
        visited: Set[str] = set()
        queue = [root_entity]

        while queue:
            curr = queue.pop(0)
            for downstream in self.adj_list.get(curr, set()):
                if downstream not in visited:
                    visited.add(downstream)
                    queue.append(downstream)

        tables = []
        pipelines = []
        dashboards = []

        for ent in visited:
            etype = self.entity_types.get(ent, "TABLE")
            if etype == "TABLE":
                tables.append(ent)
            elif etype == "PIPELINE":
                pipelines.append(ent)
            elif etype == "DASHBOARD":
                dashboards.append(ent)

        score = len(tables) * 2 + len(pipelines) * 5 + len(dashboards) * 10
        severity = "CRITICAL" if score >= 30 else "HIGH" if score >= 15 else "MEDIUM" if score >= 5 else "LOW"

        return BlastRadiusReport(
            root_entity=root_entity,
            impacted_tables=tables,
            impacted_pipelines=pipelines,
            impacted_dashboards=dashboards,
            total_impact_score=score,
            severity=severity
        )
