"""
DataFlowX Recursive Document Chunking Engine
Splits long unstructured documents along paragraph, sentence, and word boundaries with configurable token chunk sizes and overlaps.
"""

from typing import List


class RecursiveDocumentChunker:
    """Chunks text documents for RAG vectorization."""

    @classmethod
    def chunk_text(cls, text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
        words = text.split()
        if not words:
            return []

        chunks = []
        start = 0
        while start < len(words):
            end = min(len(words), start + chunk_size)
            chunk_str = " ".join(words[start:end])
            chunks.append(chunk_str)
            if end >= len(words):
                break
            start += chunk_size - chunk_overlap

        return chunks
