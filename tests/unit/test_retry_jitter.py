"""
Unit Tests: Exponential Backoff & Jitter Retry Engine
"""

import pytest
from orchestration_engine.retry.policy import RetryPolicy


def test_exponential_backoff_delay_calculation():
    policy = RetryPolicy(
        max_retries=5,
        base_delay_seconds=2.0,
        max_delay_seconds=60.0,
        backoff_multiplier=2.0,
        jitter=False  # Deterministic test
    )

    assert policy.calculate_backoff_delay(1) == 2.0
    assert policy.calculate_backoff_delay(2) == 4.0
    assert policy.calculate_backoff_delay(3) == 8.0
    assert policy.calculate_backoff_delay(4) == 16.0
    assert policy.calculate_backoff_delay(5) == 32.0


def test_retry_jitter_bounds():
    policy = RetryPolicy(
        max_retries=3,
        base_delay_seconds=10.0,
        max_delay_seconds=60.0,
        backoff_multiplier=2.0,
        jitter=True
    )

    for _ in range(10):
        delay = policy.calculate_backoff_delay(attempt=2)  # max expected is 20.0
        assert 0.0 <= delay <= 20.0


def test_retryable_vs_non_retryable_classification():
    policy = RetryPolicy(
        max_retries=3
    )

    assert policy.should_retry(1, ConnectionError("Network dropped")) is True
    assert policy.should_retry(1, TimeoutError("Connection timed out")) is True
    assert policy.should_retry(1, ValueError("Invalid syntax")) is False
    assert policy.should_retry(1, PermissionError("Access denied")) is False
    assert policy.should_retry(4, ConnectionError("Max retries exceeded")) is False
