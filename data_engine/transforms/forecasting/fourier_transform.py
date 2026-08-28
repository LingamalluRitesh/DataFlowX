"""
DataFlowX Fast Fourier Transform (FFT) Periodicity Extractor
Extracts dominant seasonal frequencies, hourly cycles, and weekly patterns from time-series metrics.
"""

from typing import List, Tuple
import numpy as np


class PeriodicityExtractor:
    """Extracts cyclic patterns using Fast Fourier Transform."""

    @classmethod
    def find_dominant_periods(cls, series: List[float], top_k: int = 3) -> List[Tuple[float, float]]:
        """Returns list of (period_length, spectral_power)."""
        if len(series) < 8:
            return []

        arr = np.array(series, dtype=float) - np.mean(series)
        fft_vals = np.fft.rfft(arr)
        power_spectrum = np.abs(fft_vals) ** 2
        freqs = np.fft.rfftfreq(len(series))

        # Exclude DC frequency at index 0
        valid_indices = np.argsort(power_spectrum[1:])[::-1][:top_k] + 1
        results = []

        for idx in valid_indices:
            f = freqs[idx]
            if f > 0:
                period = round(1.0 / f, 1)
                power = round(float(power_spectrum[idx]), 2)
                results.append((period, power))

        return results
