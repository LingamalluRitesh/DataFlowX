"""
DataFlowX Fuzzy Entity Deduplication & Record Linkage Engine
Clusters fuzzy duplicate entities using blocking keys, Jaro-Winkler string similarity, and connected component graphs.
"""

from typing import Any, Dict, List, Set, Tuple
import pandas as pd


class EntityDeduplicator:
    """Merges duplicate entities across identity columns."""

    @staticmethod
    def jaro_winkler_sim(s1: str, s2: str) -> float:
        if s1 == s2:
            return 1.0
        if not s1 or not s2:
            return 0.0

        len1, len2 = len(s1), len(s2)
        match_dist = max(len1, len2) // 2 - 1
        s1_matches = [False] * len1
        s2_matches = [False] * len2
        matches = 0

        for i in range(len1):
            start = max(0, i - match_dist)
            end = min(i + match_dist + 1, len2)
            for j in range(start, end):
                if s2_matches[j] or s1[i] != s2[j]:
                    continue
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

        jaro = (matches / len1 + matches / len2 + (matches - transpositions / 2) / matches) / 3.0

        # Prefix scale
        prefix = 0
        for i in range(min(4, min(len1, len2))):
            if s1[i] == s2[i]:
                prefix += 1
            else:
                break

        return jaro + prefix * 0.1 * (1.0 - jaro)

    @classmethod
    def find_fuzzy_duplicates(cls, df: pd.DataFrame, match_column: str, threshold: float = 0.88) -> List[Tuple[int, int, float]]:
        if df.empty or match_column not in df.columns:
            return []

        vals = df[match_column].astype(str).tolist()
        dupes = []

        for i in range(len(vals)):
            for j in range(i + 1, min(i + 50, len(vals))):  # sliding blocking window
                sim = cls.jaro_winkler_sim(vals[i], vals[j])
                if sim >= threshold:
                    dupes.append((i, j, round(sim, 3)))

        return dupes
