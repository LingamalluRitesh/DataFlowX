"""
DataFlowX Differential Privacy (DP) Noise Engine
Injects Laplace and Gaussian perturbation noise into statistical query aggregates (COUNT, SUM, AVG) satisfying epsilon-differential privacy.
"""

from typing import Union
import numpy as np
import pandas as pd


class DifferentialPrivacyEngine:
    """Injects calibrated noise for Differential Privacy."""

    @staticmethod
    def laplace_mechanism(true_value: float, sensitivity: float, epsilon: float = 1.0) -> float:
        """Adds Laplace noise with scale = sensitivity / epsilon."""
        scale = max(1e-9, sensitivity / max(1e-9, epsilon))
        noise = np.random.laplace(0, scale)
        return float(true_value + noise)

    @staticmethod
    def gaussian_mechanism(true_value: float, sensitivity: float, epsilon: float = 1.0, delta: float = 1e-5) -> float:
        """Adds Gaussian noise with scale = sqrt(2*ln(1.25/delta)) * sensitivity / epsilon."""
        sigma = (np.sqrt(2 * np.log(1.25 / delta)) * sensitivity) / max(1e-9, epsilon)
        noise = np.random.normal(0, sigma)
        return float(true_value + noise)

    @classmethod
    def dp_count(cls, count_val: int, epsilon: float = 1.0) -> int:
        """Sensitivity of COUNT is 1."""
        noisy = cls.laplace_mechanism(float(count_val), sensitivity=1.0, epsilon=epsilon)
        return max(0, int(round(noisy)))

    @classmethod
    def dp_sum(cls, sum_val: float, val_lower_bound: float, val_upper_bound: float, epsilon: float = 1.0) -> float:
        """Sensitivity of SUM is (upper - lower)."""
        sensitivity = max(1.0, val_upper_bound - val_lower_bound)
        return cls.laplace_mechanism(sum_val, sensitivity=sensitivity, epsilon=epsilon)
