"""
DataFlowX Text Analytics & NLP Processing Toolkit
Provides N-gram extraction, stopword filtering, term frequency weighting, Levenshtein edit distance, and phonetic Soundex algorithms.
"""

import re
from typing import List, Set
import pandas as pd


class TextNLPToolkit:
    """NLP text transformations."""

    @staticmethod
    def extract_ngrams(text: str, n: int = 2) -> List[str]:
        words = re.findall(r"\b\w+\b", text.lower())
        if len(words) < n:
            return []
        return [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]

    @staticmethod
    def soundex_hash(name: str) -> str:
        """Computes Soundex phonetic representation."""
        if not name:
            return ""
        name = name.upper()
        soundex = [name[0]]
        mapping = {"BFPV": "1", "CGJKQSXZ": "2", "DT": "3", "L": "4", "MN": "5", "R": "6"}

        for char in name[1:]:
            for keys, code in mapping.items():
                if char in keys:
                    if code != soundex[-1]:
                        soundex.append(code)
                    break

        soundex_str = "".join(soundex)[:4]
        return soundex_str.ljust(4, "0")
