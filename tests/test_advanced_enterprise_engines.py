"""
Comprehensive Integration Tests for Advanced Enterprise Engines:
- Vector MPP SIMD & Physical Operators
- Auto-Healing & Missing Value Imputation
- Schema Evolution & Proto3/Avro Registry
- Holt-Winters & ARIMA Time-Series Forecasting
- Hybrid RAG Vector Search & BM25 Ranker
- PII Sanitization & Salted Pseudonymization
- Consistent Hashing & Shard Rebalance Coordinator
"""

import pandas as pd
import pytest

from data_engine.mpp_engine.vector_batch import VectorBatch
from data_engine.mpp_engine.expression_evaluator import VectorizedExpressionEvaluator
from data_engine.quality.healing.imputation import MissingValueImputer
from data_engine.schema_registry.avro_schema_generator import AvroSchemaGenerator
from data_engine.schema_registry.protobuf_schema_generator import ProtobufSchemaGenerator
from data_engine.transforms.forecasting.holt_winters import HoltWintersForecaster
from data_engine.transforms.forecasting.arima_baseline import ARIMABaseline
from data_engine.rag_engine.sparse_bm25 import BM25SparseRanker
from data_engine.rag_engine.hybrid_reranker import HybridRankFusion
from data_engine.sanitization.pii_scrubber import PIIScrubber
from data_engine.sanitization.sha256_hasher import SaltedPseudonymizer
from storage.sharding.consistent_hash_ring import ConsistentHashRing
from data_engine.transpiler_deep.teradata_transpiler import TeradataTranspiler
from data_engine.transpiler_deep.oracle_transpiler import OracleToPostgresTranspiler


def test_vector_mpp_engine():
    df = pd.DataFrame({"id": [1, 2, 3, 4], "amount": [50.0, 150.0, 200.0, 30.0]})
    batch = VectorBatch.from_dataframe(df)
    assert batch.num_rows == 4
    mask = VectorizedExpressionEvaluator.eval_comparison(batch.columns["amount"], 100.0, ">")
    assert mask == [False, True, True, False]


def test_auto_healing_imputer():
    df = pd.DataFrame({"age": [20, None, 40, 60], "name": ["Alice", "Bob", None, "David"]})
    healed = MissingValueImputer.impute_dataframe(df, numeric_strategy="mean", string_strategy="constant")
    assert healed["age"].isna().sum() == 0
    assert healed["age"].iloc[1] == 40.0


def test_schema_generators():
    cols = {"id": "BIGINT", "username": "STRING", "balance": "DOUBLE"}
    avro_json = AvroSchemaGenerator.generate_avro_schema("UserRecord", "com.dataflowx", cols)
    assert "UserRecord" in avro_json
    assert "balance" in avro_json

    proto = ProtobufSchemaGenerator.generate_proto3_schema("UserRecord", "dataflowx.v1", cols)
    assert 'syntax = "proto3";' in proto
    assert "int64 id = 1;" in proto


def test_time_series_forecasting():
    series = [10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0, 34.0, 36.0]
    hw_preds = HoltWintersForecaster.forecast_series(series, season_length=7, forecast_horizon=3)
    assert len(hw_preds) == 3
    assert hw_preds[0] > 0

    arima_preds = ARIMABaseline.fit_and_predict(series, steps_ahead=3)
    assert len(arima_preds) == 3


def test_rag_bm25_and_hybrid_fusion():
    docs = [
        "Apache Iceberg provides hidden partitioning and ACID transactions",
        "SIMD vector execution accelerates query pipelines",
        "Kafka stream deduplication uses sliding Bloom filters"
    ]
    bm25 = BM25SparseRanker(docs)
    scores = bm25.score_query("Iceberg partitioning")
    assert len(scores) == 3
    assert scores[0][0] == 0  # Doc 0 is highest score

    fused = HybridRankFusion.fuse_rankings([0, 1, 2], [0, 2, 1])
    assert fused[0][0] == 0


def test_pii_sanitization():
    raw_text = "Customer email is john.doe@example.com and SSN is 123-45-6789"
    scrubbed = PIIScrubber.scrub_text(raw_text)
    assert "[REDACTED_EMAIL]" in scrubbed
    assert "[REDACTED_SSN]" in scrubbed
    assert "john.doe@example.com" not in scrubbed

    hasher = SaltedPseudonymizer()
    p1 = hasher.pseudonymize("user_123")
    p2 = hasher.pseudonymize("user_123")
    assert p1 == p2
    assert len(p1) == 64


def test_consistent_hash_ring():
    ring = ConsistentHashRing(vnodes=64)
    ring.add_node("worker-1")
    ring.add_node("worker-2")
    node = ring.get_node("partition_key_orders_2026")
    assert node in ["worker-1", "worker-2"]


def test_sql_transpilers():
    teradata_sql = "SEL id, ZEROIFNULL(amount) FROM my_table;"
    snow_sql = TeradataTranspiler.transpile_sql(teradata_sql)
    assert "SELECT" in snow_sql
    assert "COALESCE(amount, 0)" in snow_sql

    oracle_sql = "SELECT NVL(name, 'Anonymous') FROM DUAL;"
    pg_sql = OracleToPostgresTranspiler.transpile_sql(oracle_sql)
    assert "COALESCE" in pg_sql
