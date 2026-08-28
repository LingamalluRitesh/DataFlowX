"""
DataFlowX Multi-Currency FX Rate Conversion Plugin
Converts transactional amounts between global fiat currencies (USD, EUR, GBP, JPY, CAD, AUD, CHF, INR) with static base rate mappings and caching.
"""

from typing import Any, Dict, Optional
import pandas as pd


class CurrencyConverterPlugin:
    """Vectorized FX Currency Conversion Transformation."""

    # Static FX rates against USD base (1.0 USD = X Currency)
    FX_RATES: Dict[str, float] = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "JPY": 155.20,
        "CAD": 1.36,
        "AUD": 1.52,
        "CHF": 0.90,
        "INR": 83.45,
        "SGD": 1.35,
    }

    @classmethod
    def convert_amount(cls, amount: float, from_curr: str, to_curr: str = "USD") -> float:
        f_rate = cls.FX_RATES.get(from_curr.upper(), 1.0)
        t_rate = cls.FX_RATES.get(to_curr.upper(), 1.0)
        # Convert to USD first, then to target currency
        usd_amt = amount / f_rate
        return round(usd_amt * t_rate, 2)

    @classmethod
    def apply_conversion(cls, df: pd.DataFrame, amount_col: str, curr_col: str, target_curr: str = "USD", output_col: str = "amount_usd") -> pd.DataFrame:
        if df.empty or amount_col not in df.columns or curr_col not in df.columns:
            return df
        df = df.copy()

        def row_convert(row):
            amt = row[amount_col]
            curr = str(row[curr_col]).upper()
            if pd.isna(amt):
                return None
            return cls.convert_amount(float(amt), curr, target_curr)

        df[output_col] = df.apply(row_convert, axis=1)
        return df
