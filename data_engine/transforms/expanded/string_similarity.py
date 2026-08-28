"""
DataFlowX Fuzzy String Matching & Phonetic Record Linkage
Implements Levenshtein edit distance, Jaro-Winkler string similarity, and Soundex phonetic encoding for entity resolution and deduplication.
"""

from typing import List, Tuple
import pandas as pd


class StringSimilarityToolkit:
    """Calculates fuzzy string metrics."""

    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        if len(s1) < len(s2):
            return StringSimilarityToolkit.levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    @classmethod
    def similarity_ratio(cls, s1: str, s2: str) -> float:
        dist = cls.levenshtein_distance(s1.lower(), s2.lower())
        max_len = max(len(s1), len(s2))
        if max_len == 0:
            return 1.0
        return round(1.0 - (dist / max_len), 3)

    @staticmethod
    def soundex(name: str) -> str:
        if not name:
            return ""
        name = name.upper()
        soundex_map = {
            "B": "1", "F": "1", "P": "1", "V": "1",
            "C": "2", "G": "2", "J": "2", "K": "2", "Q": "2", "S": "2", "X": "2", "Z": "2",
            "D": "3", "T": "3",
            "L": "4",
            "M": "5", "N": "5",
            "R": "6"
        }
        first_letter = name[0]
        digits = []
        last_digit = soundex_map.get(first_letter, "0")

        for char in name[1:]:
            digit = soundex_map.get(char, "0")
            if digit != "0" and digit != last_digit:
                digits.append(digit)
            last_digit = digit

        code = first_letter + "".join(digits)
        return (code + "000")[:4]
