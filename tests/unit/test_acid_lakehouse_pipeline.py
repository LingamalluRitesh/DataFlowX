"""
End-to-End ACID Lakehouse & Streaming Pipeline Test Suite.
Validates Streaming Watermarks, Columnar Flight Ingestion, Governance RBAC Masking, and DAG Scheduling.
"""

import pytest
from data_engine.streaming.watermark_engine import StreamingWatermarkEngine, StreamEvent
from connectors.arrow_flight.flight_stream_connector import (
    ArrowFlightStreamConnector,
    ColumnarField,
    ColumnarRecordBatch,
)
from data_engine.governance.column_masking_engine import ColumnMaskingEngine, MaskingStrategy
from orchestration_engine.dag.dag_parser import DAGParser
from orchestration_engine.dag.models import DAGDefinition


def test_e2e_dataflowx_streaming_and_masking():
    # 1. Ingest via Arrow Flight
    flight = ArrowFlightStreamConnector()
    schema = [
        ColumnarField("user_id", "string"),
        ColumnarField("email", "string"),
        ColumnarField("amount", "float"),
    ]
    flight.register_stream_descriptor("flight_stream_users", schema)
    flight.ingest_batch("flight_stream_users", ColumnarRecordBatch(
        schema=schema,
        row_count=2,
        columns={
            "user_id": ["U1", "U2"],
            "email": ["alice@company.com", "bob@company.com"],
            "amount": [150.0, 300.0],
        }
    ))
    telemetry = flight.get_stream_telemetry("flight_stream_users")
    assert telemetry["total_rows"] == 2

    # 2. Window Processing with Watermarking
    watermark_engine = StreamingWatermarkEngine(window_size_sec=60.0, max_out_of_orderness_sec=5.0)
    watermark_engine.process_event(StreamEvent("ev1", 10.0, {"value": 150.0}))
    watermark_engine.process_event(StreamEvent("ev2", 20.0, {"value": 300.0}))
    emitted = watermark_engine.process_event(StreamEvent("ev3", 75.0, {"value": 50.0}))

    assert emitted is not None
    assert emitted[0].aggregated_metrics["sum_value"] == 450.0

    # 3. Security Column Masking
    masker = ColumnMaskingEngine()
    masker.add_masking_rule("email", "AUDITOR", MaskingStrategy.EMAIL_OBFUSCATE)
    row = {"user_id": "U1", "email": "alice@company.com", "amount": 150.0}
    masked = masker.mask_row(row, user_role="AUDITOR")
    assert masked["email"] == "a***e@company.com"

    # 4. DAG Topology Verification
    dag = DAGDefinition(
        nodes=[
            {"id": "extract_flight", "type": "extract", "name": "Extract Flight"},
            {"id": "transform_watermark", "type": "transform", "name": "Transform Watermark"},
            {"id": "mask_pii", "type": "security", "name": "Mask PII"},
            {"id": "load_lakehouse", "type": "warehouse_load", "name": "Load Lakehouse"},
        ],
        edges=[
            {"source": "extract_flight", "target": "transform_watermark"},
            {"source": "transform_watermark", "target": "mask_pii"},
            {"source": "mask_pii", "target": "load_lakehouse"},
        ],
    )
    parser = DAGParser(dag)
    is_valid, errors, _ = parser.validate_dag()
    assert is_valid is True
    assert len(errors) == 0
