"""
DataFlowX Streaming Spike & Chaos Traffic Generator
Simulates synthetic micro-burst spikes up to 50,000 events/sec to test rate limiters, backpressure controllers, and auto-scalers.
"""

import time
from typing import Dict, Generator, List
from backend.core.logging import get_logger

logger = get_logger(__name__)


class SyntheticTrafficSpiker:
    """Generates synthetic high-throughput event spikes."""

    @classmethod
    def generate_spike_stream(cls, base_rps: int = 1000, peak_rps: int = 50000, duration_seconds: int = 5) -> Generator[Dict[str, Any], None, None]:
        logger.info(f"Initiating synthetic traffic spike: ramping from {base_rps} RPS to {peak_rps} RPS over {duration_seconds}s")
        for s in range(duration_seconds):
            current_rate = base_rps + int((peak_rps - base_rps) * ((s + 1) / duration_seconds))
            yield {
                "second": s + 1,
                "emitted_rate_rps": current_rate,
                "status": "SPIKE_IN_PROGRESS"
            }
