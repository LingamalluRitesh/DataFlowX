"""
DataFlowX BM25 Sparse Inverted Index Frequency Ranker
Implements classic Okapi BM25 ranking algorithm with term frequency saturation (k1=1.5) and document length normalization (b=0.75).
"""

import math
from typing import Dict, List, Tuple


class BM25SparseRanker:
    """Okapi BM25 sparse keyword ranker."""

    def __init__(self, corpus: List[str], k1: float = 1.5, b: float = 0.75):
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.doc_len = [len(doc.lower().split()) for doc in corpus]
        self.avg_doc_len = sum(self.doc_len) / max(1, len(corpus))
        self.doc_freqs: Dict[str, int] = {}
        self._build_index()

    def _build_index(self) -> None:
        for doc in self.corpus:
            words = set(doc.lower().split())
            for w in words:
                self.doc_freqs[w] = self.doc_freqs.get(w, 0) + 1

    def score_query(self, query: str) -> List[Tuple[int, float]]:
        q_terms = query.lower().split()
        scores = []
        n_docs = len(self.corpus)

        for idx, doc in enumerate(self.corpus):
            doc_words = doc.lower().split()
            score = 0.0
            for term in q_terms:
                tf = doc_words.count(term)
                df = self.doc_freqs.get(term, 0)
                if df == 0:
                    continue
                idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1.0)
                num = tf * (self.k1 + 1.0)
                denom = tf + self.k1 * (1.0 - self.b + self.b * (self.doc_len[idx] / self.avg_doc_len))
                score += idf * (num / denom)
            scores.append((idx, round(score, 4)))

        return sorted(scores, key=lambda s: s[1], reverse=True)
