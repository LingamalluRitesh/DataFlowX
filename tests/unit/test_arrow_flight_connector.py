import pytest
from connectors.arrow_flight.flight_stream_connector import (
    ArrowFlightStreamConnector,
    ColumnarField,
    ColumnarRecordBatch,
)


def test_arrow_flight_stream_ingestion():
    connector = ArrowFlightStreamConnector()
    schema = [
        ColumnarField("order_id", "string"),
        ColumnarField("amount", "float"),
        ColumnarField("customer_id", "string"),
    ]
    connector.register_stream_descriptor("orders_flight_stream", schema)

    batch1 = ColumnarRecordBatch(
        schema=schema,
        row_count=3,
        columns={
            "order_id": ["ORD-1", "ORD-2", "ORD-3"],
            "amount": [120.50, 45.00, 890.25],
            "customer_id": ["C1", "C2", "C3"],
        },
    )

    res = connector.ingest_batch("orders_flight_stream", batch1)
    assert res["status"] == "BATCH_INGESTED_SUCCESSFULLY"
    assert res["cumulative_rows"] == 3

    telemetry = connector.get_stream_telemetry("orders_flight_stream")
    assert telemetry["batches_received"] == 1
    assert telemetry["total_rows"] == 3
