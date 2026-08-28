"""
DataFlowX VF2 Subgraph Isomorphism Algorithm
Finds isomorphic subgraph matches within larger property graphs for fraud rings and network topology queries.
"""

from typing import Dict, List, Optional, Set
from data_engine.graph_engine.property_graph import PropertyGraph


class SubgraphMatcher:
    """Finds matching subgraph structures."""

    @classmethod
    def find_all_matches(cls, target_graph: PropertyGraph, pattern_edges: List[tuple[str, str, str]]) -> List[Dict[str, str]]:
        """
        pattern_edges: list of (src_alias, target_alias, rel_type)
        Returns list of alias -> actual_node_id mappings.
        """
        if not pattern_edges:
            return []

        # Find candidate edges
        first_rel = pattern_edges[0]
        results = []

        for edge in target_graph.edges.values():
            if first_rel[2] == "*" or edge.relationship_type.upper() == first_rel[2].upper():
                mapping = {first_rel[0]: edge.source_id, first_rel[1]: edge.target_id}

                # Validate remaining edges if any
                valid = True
                for s_alias, t_alias, r_type in pattern_edges[1:]:
                    if s_alias in mapping and t_alias in mapping:
                        # Check if edge exists
                        s_id = mapping[s_alias]
                        t_id = mapping[t_alias]
                        edge_exists = any(
                            target_graph.edges[eid].target_id == t_id and (r_type == "*" or target_graph.edges[eid].relationship_type.upper() == r_type.upper())
                            for eid in target_graph.out_edges.get(s_id, [])
                        )
                        if not edge_exists:
                            valid = False
                            break

                if valid:
                    results.append(mapping)

        return results
