"""
Integration Tests: End-to-End Medallion Pipeline Execution
"""

import os
import pandas as pd
import pytest
from orchestration_engine.dag.models import DAGDefinition
from orchestration_engine.executor.dag_executor import DAGExecutor
from storage import ParquetManager, storage_engine


def test_full_medallion_pipeline_integration(tmp_path):
    # 1. Create realistic source raw data file
    raw_csv = str(tmp_path / "raw_events.csv")
    with open(raw_csv, "w", encoding="utf-8") as f:
        f.write("user_id,event_name,revenue,timestamp\n")
        f.write("U1,click,0,2025-01-01T00:00:00\n")
        f.write("U1,purchase,150.0,2025-01-01T00:05:00\n")
        f.write("U2,purchase,300.0,2025-01-01T00:10:00\n")
        f.write("U3,refund,-50.0,2025-01-01T00:15:00\n")  # Bad/negative value for quality filter
        f.write("U2,purchase,300.0,2025-01-01T00:10:00\n")  # Duplicate

    # 2. Build DAG
    dag = DAGDefinition(
        nodes=[
            {
                "id": "step_extract",
                "type": "extract",
                "name": "Extract Raw Events",
                "config": {"connector_type": "csv", "file_path": raw_csv}
            },
            {
                "id": "step_quality",
                "type": "quality",
                "name": "Validate Revenue Non-Negative",
                "config": {
                    "failure_action": "QUARANTINE_RECORDS",
                    "rules": [
                        {"rule_type": "NOT_NULL", "target_column": "user_id"},
                        {"rule_type": "RANGE", "target_column": "revenue", "condition_params": {"min": 0}}
                    ]
                }
            },
            {
                "id": "step_silver",
                "type": "transform",
                "name": "Deduplicate Silver",
                "config": {
                    "steps": [
                        {"type": "deduplicate", "config": {"subset": ["user_id", "event_name", "timestamp"]}}
                    ]
                }
            },
            {
                "id": "step_gold",
                "type": "aggregate",
                "name": "Aggregate Revenue Mart",
                "config": {
                    "group_by": ["user_id"],
                    "aggregations": {"revenue": "sum"}
                }
            },
            {
                "id": "step_warehouse",
                "type": "warehouse_load",
                "name": "Load Warehouse Table",
                "config": {
                    "table_name": "mart_user_revenue_test",
                    "mode": "overwrite"
                }
            }
        ],
        edges=[
            {"source": "step_extract", "target": "step_quality"},
            {"source": "step_quality", "target": "step_silver"},
            {"source": "step_silver", "target": "step_gold"},
            {"source": "step_gold", "target": "step_warehouse"}
        ]
    )

    # 3. Execute Pipeline
    executor = DAGExecutor(
        dag_definition=dag,
        pipeline_id="pipe_test_medallion",
        execution_id="exec_test_medallion_1",
        max_workers=2
    )

    summary = executor.run()
    assert summary.status == "SUCCESS"
    assert summary.total_records_processed > 0

    # 4. Verify Final Warehouse Load Output
    warehouse_res = summary.task_results["step_warehouse"]
    assert warehouse_res.status == "SUCCESS"
    assert len(warehouse_res.output_data) == 2  # Users U1 and U2
