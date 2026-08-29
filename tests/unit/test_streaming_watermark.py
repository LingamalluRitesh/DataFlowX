import pytest
from data_engine.streaming.watermark_engine import StreamingWatermarkEngine, StreamEvent


def test_watermark_in_order_windowing():
    engine = StreamingWatermarkEngine(window_size_sec=60.0, max_out_of_orderness_sec=5.0)

    # Event 1 at t=10
    engine.process_event(StreamEvent("e1", 10.0, {"value": 100.0}))
    # Event 2 at t=40
    engine.process_event(StreamEvent("e2", 40.0, {"value": 200.0}))

    # Advance time to t=70 -> watermark becomes 70 - 5 = 65 -> window [0, 60) fires!
    emitted = engine.process_event(StreamEvent("e3", 70.0, {"value": 50.0}))

    assert emitted is not None
    assert len(emitted) == 1
    assert emitted[0].window_start == 0.0
    assert emitted[0].window_end == 60.0
    assert emitted[0].events_count == 2
    assert emitted[0].aggregated_metrics["sum_value"] == 300.0


def test_watermark_dropped_late_events():
    engine = StreamingWatermarkEngine(window_size_sec=60.0, allowed_lateness_sec=10.0, max_out_of_orderness_sec=5.0)

    # Fast forward to t=100 -> Watermark = 95
    engine.process_event(StreamEvent("e_now", 100.0, {"value": 1.0}))

    # Event with timestamp 50 is before (Watermark 95 - Lateness 10 = 85) -> Must be dropped
    res = engine.process_event(StreamEvent("e_late", 50.0, {"value": 999.0}))
    assert res is None
    assert len(engine.side_output_dropped_events) == 1
    assert engine.side_output_dropped_events[0].event_id == "e_late"
