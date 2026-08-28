"""
DataFlowX Retry Policy & Exponential Backoff Engine
Calculates retry delays with jitter and classifies retryable vs non-retryable exceptions.
"""

import random
import time
from typing import Any, Callable, List, Optional, Set, Type
from pydantic import BaseModel, Field
from backend.core.exceptions import (
    AuthenticationError,
    DAGCycleError,
    DAGValidationError,
    PermissionDeniedError,
    ValidationError,
)
from backend.core.logging import get_logger

logger = get_logger(__name__)

# Non-retryable fatal exceptions
NON_RETRYABLE_EXCEPTIONS: Set[Type[Exception]] = {
    AuthenticationError,
    PermissionDeniedError,
    PermissionError,
    FileNotFoundError,
    DAGValidationError,
    DAGCycleError,
    SyntaxError,
    ValueError,
    KeyError,
}


class RetryPolicy(BaseModel):
    max_retries: int = Field(default=3, ge=0, le=10)
    base_delay_seconds: float = Field(default=2.0, ge=0.1)
    max_delay_seconds: float = Field(default=300.0, ge=1.0)
    backoff_multiplier: float = Field(default=2.0, ge=1.0)
    jitter: bool = True

    def is_retryable(self, exc: Exception) -> bool:
        """Determine if an exception should trigger a retry attempt."""
        for non_retryable in NON_RETRYABLE_EXCEPTIONS:
            if isinstance(exc, non_retryable):
                return False
        return True

    def calculate_delay(self, attempt_number: int) -> float:
        """Compute exponential backoff delay with jitter."""
        if attempt_number <= 0:
            return 0.0

        delay = self.base_delay_seconds * (self.backoff_multiplier ** (attempt_number - 1))
        delay = min(delay, self.max_delay_seconds)

        if self.jitter:
            delay = random.uniform(0.0, delay)

        return round(delay, 2)

    def calculate_backoff_delay(self, attempt: int) -> float:
        return self.calculate_delay(attempt)

    def should_retry(self, attempt: int, exc: Exception) -> bool:
        if attempt > self.max_retries:
            return False
        return self.is_retryable(exc)

    def execute_with_retry(
        self,
        func: Callable[..., Any],
        *args: Any,
        on_retry_callback: Optional[Callable[[int, Exception, float], None]] = None,
        **kwargs: Any
    ) -> Any:
        """Synchronously execute callable with automatic retry."""
        attempt = 1
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                if attempt > self.max_retries or not self.is_retryable(exc):
                    logger.error(f"Execution failed after {attempt} attempts: {exc}")
                    raise exc

                delay = self.calculate_delay(attempt)
                logger.warning(f"Attempt {attempt}/{self.max_retries} failed: {exc}. Retrying in {delay}s...")

                if on_retry_callback:
                    on_retry_callback(attempt, exc, delay)

                time.sleep(delay)
                attempt += 1


RetryEngine = RetryPolicy
