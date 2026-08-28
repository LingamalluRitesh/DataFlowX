"""
DataFlowX Webhook Circuit Breaker & Dead-Letter Queue Dispatcher
Provides resilient HTTP webhook delivery with exponential backoff, dead-letter storage, and circuit breaker trip states (CLOSED, OPEN, HALF_OPEN).
"""

import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WebhookPayload(BaseModel):
    event_id: str
    target_url: str
    payload_body: Dict[str, Any]
    attempt_count: int = 0
    max_retries: int = 5
    last_error: Optional[str] = None


class CircuitBreakerStatus(BaseModel):
    endpoint_host: str
    state: str  # CLOSED, OPEN, HALF_OPEN
    failure_count: int = 0
    success_count: int = 0
    last_failure_timestamp: float = 0.0


class WebhookCircuitBreaker:
    """Manages circuit breaking and retry queues per target endpoint."""

    def __init__(self, failure_threshold: int = 5, recovery_timeout_seconds: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_seconds
        # host -> CircuitBreakerStatus
        self.circuits: Dict[str, CircuitBreakerStatus] = {}
        self.dead_letter_queue: List[WebhookPayload] = []

    def record_success(self, host: str) -> None:
        if host not in self.circuits:
            self.circuits[host] = CircuitBreakerStatus(endpoint_host=host, state="CLOSED")
        c = self.circuits[host]
        c.failure_count = 0
        c.success_count += 1
        c.state = "CLOSED"

    def record_failure(self, host: str, payload: WebhookPayload, error_msg: str) -> None:
        if host not in self.circuits:
            self.circuits[host] = CircuitBreakerStatus(endpoint_host=host, state="CLOSED")
        c = self.circuits[host]
        c.failure_count += 1
        c.last_failure_timestamp = time.time()
        payload.attempt_count += 1
        payload.last_error = error_msg

        if c.failure_count >= self.failure_threshold:
            c.state = "OPEN"

        if payload.attempt_count >= payload.max_retries:
            self.dead_letter_queue.append(payload)
