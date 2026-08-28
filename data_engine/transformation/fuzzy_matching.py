"""
DataFlowX Fuzzy Record Linkage & String Distance Matching Engine
Provides string similarity scoring: Levenshtein distance, Jaro-Winkler, Soundex phonetic hashing, and entity deduplication.
"""

from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd

from backend.core.logging import get_logger
from data_engine.transformation.operators import BaseOperator

logger = get_logger(__name__)


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate minimum single-character edits (insertions, deletions, substitutions)."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def jaro_similarity(s1: str, s2: str) -> float:
    """Compute Jaro distance score [0.0, 1.0]."""
    if not s1 or not s2:
        return 1.0 if s1 == s2 else 0.0
    if s1 == s2:
        return 1.0

    len1, len2 = len(s1), len(s2)
    max_dist = max(len1, len2) // 2 - 1
    if max_dist < 0:
        max_dist = 0

    s1_matches = [False] * len1
    s2_matches = [False] * len2
    matches = 0

    for i in range(len1):
        start = max(0, i - max_dist)
        end = min(i + max_dist + 1, len2)
        for j in range(start, end):
            if s2_matches[j]:
                continue
            if s1[i] == s2[j]:
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break

    if matches == 0:
        return 0.0

    transpositions = 0
    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    transpositions //= 2
    return ((matches / len1) + (matches / len2) + ((matches - transpositions) / matches)) / 3.0


def soundex_hash(name: str) -> str:
    """American Soundex phonetic string encoding (e.g. Robert & Rupert -> R163)."""
    if not name:
        return "0000"
    name = name.upper()
    soundex_mapping = {
        "B": "1", "F": "1", "P": "1", "V": "1",
        "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
        "D": "3", "T": "3",
        "L": "4",
        "M": "5", "N": "5",
        "R": "6"
    }

    first_letter = name[0]
    tail = name[1:]
    encoded_tail = ""
    last_code = soundex_mapping.get(first_letter, "")

    for char in tail:
        code = soundex_mapping.get(char, "")
        if code and code != last_code:
            encoded_tail += code
            last_code = code
        elif not code and char not in ("A", "E", "I", "O", "U", "Y"):
            last_code = ""

    soundex_code = first_letter + encoded_tail
    soundex_code = soundex_code.replace("0", "")
    return (soundex_code + "000")[:4]


class FuzzyStringMatchOperator(BaseOperator):
    """Calculates pairwise string similarity score between two column attributes."""

    def __init__(
        self,
        col_a: str,
        col_b: str,
        algorithm: str = "jaro",  # jaro, levenshtein, soundex
        output_col: str = "similarity_score"
    ):
        self.col_a = col_a
        self.col_b = col_b
        self.algorithm = algorithm.lower()
        self.output_col = output_col

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.col_a not in df.columns or self.col_b not in df.columns:
            return df
        df = df.copy()

        def compute_sim(row: pd.Series) -> float:
            val_a = str(row[self.col_a]) if pd.notnull(row[self.col_a]) else ""
            val_b = str(row[self.col_b]) if pd.notnull(row[self.col_b]) else ""

            if self.algorithm == "levenshtein":
                dist = levenshtein_distance(val_a, val_b)
                max_l = max(len(val_a), len(val_b))
                return round(1.0 - (dist / max_l), 4) if max_l > 0 else 1.0
            elif self.algorithm == "soundex":
                return 1.0 if soundex_hash(val_a) == soundex_hash(val_b) else 0.0
            else:
                return round(jaro_similarity(val_a, val_b), 4)

        df[self.output_col] = df.apply(compute_sim, axis=1)
        return df


class SoundexPhoneticOperator(BaseOperator):
    """Encodes names or text columns into Soundex phonetic codes for clustering."""

    def __init__(self, target_column: str, output_col: Optional[str] = None):
        self.target_column = target_column
        self.output_col = output_col or f"{self.target_column}_soundex"

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or self.target_column not in df.columns:
            return df
        df = df.copy()
        df[self.output_col] = df[self.target_column].astype(str).apply(soundex_hash)
        return df
