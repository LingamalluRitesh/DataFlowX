"""
DataFlowX High-Throughput Token Bucket & Leaky Bucket Rate Limiter
Enforces precise rate limits on incoming API/Webhook streaming streams to protect downstream pipelines against burst overload.
"""

import threading
import time


class TokenBucketRateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, refill_rate_per_sec: float = 1000.0, max_burst_capacity: float = 2000.0):
        self.refill_rate = refill_rate_per_sec
        self.capacity = max_burst_capacity
        self.tokens = max_burst_capacity
        self.last_refill_unix = time.time()
        self._lock = threading.Lock()

    def allow_request(self, tokens_needed: float = 1.0) -> bool:
        with self._lock:
            now = time.time()
            elapsed = now - self.last_refill_unix
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill_unix = now

            if self.tokens >= tokens_needed:
                self.tokens -= tokens_needed
                return True
            return False
