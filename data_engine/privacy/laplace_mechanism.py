"""
DataFlowX Differential Privacy (ε, δ) Laplace Mechanism
Injects calibrated zero-mean Laplace noise scaled to global sensitivity Δf / epsilon to guarantee provable privacy in statistical aggregation queries.
"""

import math
from typing import Any, List, Optional
import numpy as np
import pandas as pd


class DifferentialPrivacyLaplace:
    """Laplace Mechanism for ε-Differential Privacy."""

    @classmethod
    def sample_laplace_noise(cls, scale: float) -> float:
        """Sample from Laplace(0, scale) distribution."""
        u = np.random.uniform(-0.5, 0.5)
        # Inverse CDF of Laplace
        return -scale * np.sign(u) * np.log(1.0 - 2.0 * abs(u) + 1e-12)

    @classmethod
    def privatize_count(cls, true_count: int, epsilon: float = 1.0) -> int:
        """Global sensitivity Δf = 1 for counting queries."""
        scale = 1.0 / epsilon
        noise = cls.sample_laplace_noise(scale)
        return max(0, int(round(true_count + noise)))

    @classmethod
    def privatize_sum(cls, true_sum: float, upper_bound: float, lower_bound: float, epsilon: float = 1.0) -> float:
        """Global sensitivity Δf = upper_bound - lower_bound for bounded sums."""
        sensitivity = upper_bound - lower_bound
        scale = sensitivity / epsilon
        noise = cls.sample_laplace_noise(scale)
        return round(float(true_sum + noise), 2)
