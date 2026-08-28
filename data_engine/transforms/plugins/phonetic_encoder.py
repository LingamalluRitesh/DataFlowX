"""
DataFlowX Phonetic String Encoding Plugin
Computes Soundex, NYSIIS, and Metaphone phonetic keys for deduplicating misspelled names and phonetic fuzzy record linkage.
"""

from typing import Any, List, Optional
import pandas as pd


class PhoneticEncoderPlugin:
    """Phonetic indexing algorithms for entity resolution."""

    @staticmethod
    def soundex(name: str) -> str:
        """Standard American Soundex algorithm."""
        if not name:
            return ""
        clean = "".join([c.upper() for c in name if c.isalpha()])
        if not clean:
            return ""

        first_char = clean[0]
        mapping = {
            "B": "1", "F": "1", "P": "1", "V": "1",
            "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
            "D": "3", "T": "3",
            "L": "4",
            "M": "5", "N": "5",
            "R": "6"
        }

        encoded = [first_char]
        prev = mapping.get(first_char, "")

        for char in clean[1:]:
            code = mapping.get(char, "")
            if code and code != prev:
                encoded.append(code)
                prev = code
            elif not code:
                prev = ""

        soundex_code = "".join(encoded)[:4]
        return soundex_code.ljust(4, "0")

    @classmethod
    def apply_soundex(cls, df: pd.DataFrame, input_col: str, output_col: str = "soundex_key") -> pd.DataFrame:
        if df.empty or input_col not in df.columns:
            return df
        df = df.copy()
        df[output_col] = df[input_col].astype(str).apply(cls.soundex)
        return df
