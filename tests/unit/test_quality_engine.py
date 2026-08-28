"""
Unit Tests: Data Quality Engine, Rule Suite & Quarantine
"""

import pandas as pd
import pytest
from data_engine.quality.quarantine import QuarantineManager
from data_engine.quality.rules import (
    EmailRule,
    NotNullRule,
    RangeRule,
    RegexRule,
    UniqueRule,
)
from data_engine.quality.suite import QualitySuiteEvaluator


def test_individual_quality_rules():
    df = pd.DataFrame([
        {"id": "1", "email": "valid@domain.com", "age": 25, "score": 100},
        {"id": "2", "email": "not-an-email", "age": -5, "score": 80},
        {"id": None, "email": "user2@domain.com", "age": 45, "score": 90},
        {"id": "1", "email": "user3@domain.com", "age": 30, "score": 70},  # Duplicate ID
    ])

    # 1. NotNullRule
    not_null_res = NotNullRule("id").evaluate(df)
    assert not_null_res.passed_records == 3
    assert not_null_res.failed_records == 1
    assert 2 in not_null_res.failed_indices

    # 2. EmailRule
    email_res = EmailRule("email").evaluate(df)
    assert email_res.failed_records == 1
    assert 1 in email_res.failed_indices

    # 3. RangeRule (age >= 0)
    range_res = RangeRule("age", min_value=0, max_value=120).evaluate(df)
    assert range_res.failed_records == 1
    assert 1 in range_res.failed_indices

    # 4. UniqueRule
    unique_res = UniqueRule("id").evaluate(df)
    assert unique_res.failed_records == 2  # indices 0 and 3 are duplicates


def test_quality_suite_evaluator_and_quarantine():
    df = pd.DataFrame([
        {"customer_id": "C01", "email": "c1@test.com", "spend": 100},
        {"customer_id": "C02", "email": "c2@test.com", "spend": 250},
        {"customer_id": None, "email": "invalid-email", "spend": -20},  # Corrupted row
    ])

    evaluator = QualitySuiteEvaluator(
        rules=[
            NotNullRule("customer_id"),
            EmailRule("email"),
            RangeRule("spend", min_value=0),
        ]
    )

    summary, valid_df = evaluator.evaluate(
        df,
        dataset_id="raw_customers",
        execution_id="exec_test_1",
        failure_action="QUARANTINE_RECORDS"
    )
    assert summary.total_records == 3
    assert len(valid_df) == 2
    assert summary.overall_quality_score < 100.0

    # Test Quarantine persistence
    q_manager = QuarantineManager()
    q_uri = q_manager.quarantine_records(
        records=[{"bad": "data"}],
        dataset_id="raw_customers",
        execution_id="exec_test_1",
        rule_name="suite_validation",
        reason="Quality checks failed"
    )
    assert q_uri is not None
    assert "quarantine/" in q_uri
