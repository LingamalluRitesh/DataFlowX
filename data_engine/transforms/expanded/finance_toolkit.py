"""
DataFlowX Financial Analytics & Valuation Toolkit
Calculates Compound Annual Growth Rate (CAGR), Net Present Value (NPV), and currency exchange rate normalizations.
"""

from typing import List, Optional
import pandas as pd


class FinanceToolkit:
    """Financial calculations."""

    @staticmethod
    def calculate_cagr(beginning_value: float, ending_value: float, num_years: float) -> float:
        if beginning_value <= 0 or num_years <= 0:
            return 0.0
        return round(((ending_value / beginning_value) ** (1.0 / num_years) - 1.0) * 100.0, 2)

    @staticmethod
    def calculate_npv(rate: float, cash_flows: List[float]) -> float:
        npv = 0.0
        for t, cf in enumerate(cash_flows):
            npv += cf / ((1.0 + rate) ** t)
        return round(npv, 2)
