"""
DataFlowX Recursive Semantic Paragraph & Sentence Chunker
Splits natural language documents along semantic boundaries (paragraphs, sentences) with sliding token overlap for RAG indexing.
"""

import re
from typing import List, Optional
from pydantic import BaseModel, Field


class TextChunk(BaseModel):
    chunk_index: int
    text: str
    token_count: int
    start_char: int
    end_char: int


class SemanticSentenceChunker:
    """Chunks prose text along natural sentence boundaries."""

    SENTENCE_SPLIT_REGEX = re.compile(r"(?<=[.!?])\s+")

    @classmethod
    def chunk_text(cls, document_text: str, max_chunk_tokens: int = 256, overlap_sentences: int = 1) -> List[TextChunk]:
        if not document_text.strip():
            return []

        # Split into raw sentences
        sentences = [s.strip() for s in cls.SENTENCE_SPLIT_REGEX.split(document_text) if s.strip()]
        if not sentences:
            return []

        chunks = []
        current_sentences = []
        current_tokens = 0
        char_offset = 0

        for i, s in enumerate(sentences):
            # Approximate 1 token ~= 4 chars or 0.75 words
            s_tokens = max(1, len(s.split()))

            if current_tokens + s_tokens > max_chunk_tokens and current_sentences:
                chunk_str = " ".join(current_sentences)
                chunks.append(TextChunk(
                    chunk_index=len(chunks),
                    text=chunk_str,
                    token_count=current_tokens,
                    start_char=char_offset,
                    end_char=char_offset + len(chunk_str)
                ))
                char_offset += len(chunk_str) + 1

                # Keep overlap
                overlap = current_sentences[-overlap_sentences:] if overlap_sentences > 0 else []
                current_sentences = list(overlap)
                current_tokens = sum(max(1, len(w.split())) for w in current_sentences)

            current_sentences.append(s)
            current_tokens += s_tokens

        if current_sentences:
            chunk_str = " ".join(current_sentences)
            chunks.append(TextChunk(
                chunk_index=len(chunks),
                text=chunk_str,
                token_count=current_tokens,
                start_char=char_offset,
                end_char=char_offset + len(chunk_str)
            ))

        return chunks
