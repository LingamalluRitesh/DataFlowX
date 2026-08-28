"""
DataFlowX Physical Units & Engineering Metrics Conversion Plugin
Standardizes physical measurements: Length (meters, km, miles, feet, inches), Weight (kg, lbs, grams, oz), Temperature (Celsius, Fahrenheit, Kelvin), and Pressure (Bar, PSI, Pascal).
"""

from typing import Any, Dict, Optional
import pandas as pd


class UnitConverterPlugin:
    """Vectorized conversion of engineering and physical units."""

    # Multipliers to standard base units (meter, kilogram, celsius)
    LENGTH_TO_METERS: Dict[str, float] = {
        "M": 1.0,
        "KM": 1000.0,
        "CM": 0.01,
        "MM": 0.001,
        "MILE": 1609.344,
        "FT": 0.3048,
        "INCH": 0.0254,
    }

    WEIGHT_TO_KG: Dict[str, float] = {
        "KG": 1.0,
        "G": 0.001,
        "MG": 0.000001,
        "LB": 0.45359237,
        "OZ": 0.028349523,
    }

    @classmethod
    def convert_length(cls, val: float, from_unit: str, to_unit: str = "M") -> float:
        f_m = cls.LENGTH_TO_METERS.get(from_unit.upper(), 1.0)
        t_m = cls.LENGTH_TO_METERS.get(to_unit.upper(), 1.0)
        return (val * f_m) / t_m

    @classmethod
    def convert_temperature(cls, val: float, from_unit: str, to_unit: str = "C") -> float:
        f = from_unit.upper()
        t = to_unit.upper()

        # Convert to Celsius first
        if f == "F":
            c = (val - 32.0) * (5.0 / 9.0)
        elif f == "K":
            c = val - 273.15
        else:
            c = val

        # Convert from Celsius to Target
        if t == "F":
            return round((c * 9.0 / 5.0) + 32.0, 2)
        elif t == "K":
            return round(c + 273.15, 2)
        return round(c, 2)
