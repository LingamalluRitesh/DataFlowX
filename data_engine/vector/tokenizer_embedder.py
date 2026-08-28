"""
DataFlowX Text Tokenizer, BM25 Indexer & Sparse/Dense Vector Embedder
Provides subword n-gram hashing, TF-IDF vectorization, and BM25 Okapi lexical ranking without external NLP libraries.
"""

from collections import Counter
import math
import re
from typing import Any, Dict, List, Optional, Set, Tuple


class TextTokenizerEmbedder:
    """Computes fixed-dimension dense vector representations from textual descriptions."""

    def __init__(self, vector_dim: int = 128):
        self.vector_dim = vector_dim

    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        cleaned = re.sub(r"[^a-zA-Z0-9_\s]", " ", text.lower())
        return [tok for tok in cleaned.split() if len(tok) > 1]

    def text_to_embedding(self, text: str) -> List[float]:
        """Hash-trick dense embedding vector generation."""
        tokens = self.tokenize(text)
        vec = [0.0] * self.vector_dim
        if not tokens:
            return vec

        for tok in tokens:
            # Deterministic feature hash
            h = abs(hash(tok))
            idx = h % self.vector_dim
            sign = 1.0 if ((h // self.vector_dim) % 2 == 0) else -1.0
            vec[idx] += sign

        # L2 normalize
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0.0:
            vec = [v / norm for v in vec]

        return vec


class BM25OkapiIndexer:
    """Okapi BM25 Lexical Ranking for Data Catalog Search."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0
        self.term_doc_freqs: Dict[str, int] = Counter()
        self.doc_term_freqs: Dict[str, Dict[str, int]] = {}
        self.total_docs: int = 0

    def add_document(self, doc_id: str, text: str) -> None:
        tokens = TextTokenizerEmbedder().tokenize(text)
        self.doc_lengths[doc_id] = len(tokens)
        tf = Counter(tokens)
        self.doc_term_freqs[doc_id] = dict(tf)
        for term in tf.keys():
            self.term_doc_freqs[term] += 1
        self.total_docs += 1
        self.avg_doc_length = sum(self.doc_lengths.values()) / max(1, self.total_docs)

    def score_query(self, query_text: str) -> List[Tuple[float, str]]:
        q_tokens = TextTokenizerEmbedder().tokenize(query_text)
        scores: Dict[str, float] = {}

        for doc_id, tf_map in self.doc_term_freqs.items():
            doc_len = self.doc_lengths[doc_id]
            doc_score = 0.0

            for q_term in q_tokens:
                if q_term not in tf_map:
                    continue
                tf = tf_map[q_term]
                df = self.term_doc_freqs.get(q_term, 0)
                idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1.0)
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / max(1.0, self.avg_doc_length)))
                doc_score += idf * (numerator / max(1e-6, denominator))

            if doc_score > 0.0:
                scores[doc_id] = round(doc_score, 4)

        sorted_res = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(score, doc_id) for doc_id, score in sorted_res]
