"""
Unit Tests: Kahn's DAG Cycle Detector & Topological Sorter
"""

import pytest
from orchestration_engine.dag.dag_parser import DAGParser
from orchestration_engine.dag.models import DAGDefinition, DAGEdge, DAGNode


def test_valid_dag_topological_sort_and_layers():
    dag = DAGDefinition(
        nodes=[
            {"id": "A", "type": "extract", "name": "Extract A"},
            {"id": "B", "type": "extract", "name": "Extract B"},
            {"id": "C", "type": "transform", "name": "Transform C"},
            {"id": "D", "type": "aggregate", "name": "Aggregate D"},
            {"id": "E", "type": "warehouse_load", "name": "Load E"},
        ],
        edges=[
            {"source": "A", "target": "C"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "D"},
            {"source": "D", "target": "E"},
        ]
    )

    parser = DAGParser(dag)
    is_valid, errors, warnings = parser.validate_dag()
    assert is_valid is True
    assert len(errors) == 0

    top_order = parser.get_topological_sort()
    assert top_order.index("A") < top_order.index("C")
    assert top_order.index("B") < top_order.index("C")
    assert top_order.index("C") < top_order.index("D")
    assert top_order.index("D") < top_order.index("E")

    layers = parser.get_execution_layers()
    assert len(layers) == 4
    # Layer 0 can run A and B in parallel!
    assert set(layers[0]) == {"A", "B"}
    assert layers[1] == ["C"]
    assert layers[2] == ["D"]
    assert layers[3] == ["E"]


def test_cycle_detection_in_cyclic_dag():
    dag = DAGDefinition(
        nodes=[
            {"id": "N1", "type": "transform", "name": "Node 1"},
            {"id": "N2", "type": "transform", "name": "Node 2"},
            {"id": "N3", "type": "transform", "name": "Node 3"},
        ],
        edges=[
            {"source": "N1", "target": "N2"},
            {"source": "N2", "target": "N3"},
            {"source": "N3", "target": "N1"},  # Cycle!
        ]
    )

    parser = DAGParser(dag)
    is_valid, errors, warnings = parser.validate_dag()
    assert is_valid is False
    assert any("cycle" in e.lower() for e in errors)

    is_cyclic, cycle_nodes = parser.detect_cycles()
    assert is_cyclic is True
    assert set(cycle_nodes) == {"N1", "N2", "N3"}
