"""
DataFlowX In-Memory Property Graph Model
Represents labeled property graph nodes, directed multi-edges, and node/edge attributes for graph analytics.
"""

from collections import defaultdict
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    node_id: str
    labels: List[str] = Field(default_factory=list)
    properties: Dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    edge_id: str
    source_id: str
    target_id: str
    relationship_type: str
    properties: Dict[str, Any] = Field(default_factory=dict)


class PropertyGraph:
    """In-memory property graph."""

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: Dict[str, GraphEdge] = {}
        # Adjacency: source_id -> list of edge_ids
        self.out_edges: Dict[str, List[str]] = defaultdict(list)
        # In-edges: target_id -> list of edge_ids
        self.in_edges: Dict[str, List[str]] = defaultdict(list)

    def add_node(self, node_id: str, labels: Optional[List[str]] = None, properties: Optional[Dict[str, Any]] = None) -> GraphNode:
        node = GraphNode(node_id=node_id, labels=labels or [], properties=properties or {})
        self.nodes[node_id] = node
        return node

    def add_edge(self, edge_id: str, source_id: str, target_id: str, relationship_type: str, properties: Optional[Dict[str, Any]] = None) -> GraphEdge:
        edge = GraphEdge(
            edge_id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            properties=properties or {}
        )
        self.edges[edge_id] = edge
        self.out_edges[source_id].append(edge_id)
        self.in_edges[target_id].append(edge_id)
        return edge

    def get_neighbors(self, node_id: str, direction: str = "OUT") -> List[str]:
        if direction.upper() == "OUT":
            return [self.edges[eid].target_id for eid in self.out_edges.get(node_id, [])]
        elif direction.upper() == "IN":
            return [self.edges[eid].source_id for eid in self.in_edges.get(node_id, [])]
        else:
            out_n = [self.edges[eid].target_id for eid in self.out_edges.get(node_id, [])]
            in_n = [self.edges[eid].source_id for eid in self.in_edges.get(node_id, [])]
            return list(set(out_n + in_n))
