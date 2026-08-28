"""
Performance Benchmark Tests
Tests vectorization throughput and memory efficiency for 10,000, 100,000, and 1,000,000 record streams.
"""

import time
import numpy as np
import pandas as pd
import pytest
from data_engine.profiling.profiler import DataProfiler
from data_engine.quality.rules import NotNullRule, RangeRule
from data_engine.quality.suite import QualitySuiteEvaluator
from data_engine.transformation.operators import (
    AggregateOperator,
    CalculatedColumnOperator,
    DeduplicateOperator,
    FilterRowsOperator,
)
from storage import ParquetManager


def test_10k_records_benchmark():
    n = 10_000
    df = pd.DataFrame({
        "id": np.arange(n),
        "user_id": [f"U_{i % 500}" for i in range(n)],
        "category": np.random.choice(["Electronics", "Fashion", "Grocery", "Home"], size=n),
        "amount": np.random.uniform(10.0, 500.0, size=n),
        "quantity": np.random.randint(1, 10, size=n),
    })

    t0 = time.time()
    # 1. Operators
    df_calc = CalculatedColumnOperator("total_cost", "amount * quantity").transform(df)
    df_filt = FilterRowsOperator("total_cost > 100").transform(df_calc)
    df_agg = AggregateOperator(group_by=["category"], aggregations={"total_cost": "sum"}).transform(df_filt)
    duration = time.time() - t0

    assert len(df_agg) <= 4
    assert duration < 2.0, f"10K benchmark took {duration:.3f}s (expected < 2.0s)"


def test_100k_records_benchmark():
    n = 100_000
    df = pd.DataFrame({
        "id": np.arange(n),
        "customer_id": [f"CUST_{i % 5000}" for i in range(n)],
        "spend": np.random.uniform(5.0, 1000.0, size=n),
        "rating": np.random.randint(1, 6, size=n),
    })

    t0 = time.time()
    # Quality Suite Check
    suite = QualitySuiteEvaluator(
        rules=[
            NotNullRule("customer_id"),
            RangeRule("spend", min_value=0),
            RangeRule("rating", min_value=1, max_value=5),
        ]
    )
    summary, valid_df = suite.evaluate(df, failure_action="QUARANTINE_RECORDS")
    duration = time.time() - t0

    assert summary.total_records == 100_000
    assert summary.overall_quality_score == 100.0
    assert duration < 5.0, f"100K quality check took {duration:.3f}s (expected < 5.0s)"


def test_1m_records_throughput_benchmark():
    n = 1_000_000
    df = pd.DataFrame({
        "metric_id": np.arange(n),
        "sensor_id": [f"sensor_{i % 1000}" for i in range(n)],
        "value": np.random.normal(50.0, 15.0, size=n),
    })

    t0 = time.time()
    # Parquet columnar round-trip
    parquet_bytes = ParquetManager.dataframe_to_parquet_bytes(df, compression="SNAPPY")
    recs = ParquetManager.parquet_bytes_to_records(parquet_bytes, limit=1000)
    duration = time.time() - t0

    assert len(parquet_bytes) > 0
    assert len(recs) == 1000
    assert duration < 10.0, f"1M parquet serialization took {duration:.3f}s (expected < 10.0s)"
