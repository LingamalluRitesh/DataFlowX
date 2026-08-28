"""
DataFlowX Syntax-Aware Source Code Chunker
Splits code files along function, class, and method definitions rather than arbitrary token boundaries.
"""

import ast
from typing import List, Optional
from pydantic import BaseModel, Field


class CodeChunk(BaseModel):
    chunk_index: int
    symbol_name: str
    symbol_type: str  # CLASS, FUNCTION, METHOD, MODULE_LEVEL
    source_code: str
    start_line: int
    end_line: int


class CodeASTChunker:
    """Chunks Python code by AST nodes."""

    @classmethod
    def chunk_python_code(cls, source_code: str) -> List[CodeChunk]:
        chunks = []
        lines = source_code.splitlines()

        try:
            tree = ast.parse(source_code)
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    start = node.lineno
                    end = getattr(node, "end_lineno", start + 10)
                    chunk_code = "\n".join(lines[start - 1:end])
                    chunks.append(CodeChunk(
                        chunk_index=len(chunks),
                        symbol_name=node.name,
                        symbol_type="FUNCTION",
                        source_code=chunk_code,
                        start_line=start,
                        end_line=end
                    ))
                elif isinstance(node, ast.ClassDef):
                    start = node.lineno
                    end = getattr(node, "end_lineno", start + 20)
                    chunk_code = "\n".join(lines[start - 1:end])
                    chunks.append(CodeChunk(
                        chunk_index=len(chunks),
                        symbol_name=node.name,
                        symbol_type="CLASS",
                        source_code=chunk_code,
                        start_line=start,
                        end_line=end
                    ))
        except Exception:
            # Fallback to simple block chunking
            chunks.append(CodeChunk(
                chunk_index=0,
                symbol_name="raw_module",
                symbol_type="MODULE_LEVEL",
                source_code=source_code,
                start_line=1,
                end_line=len(lines)
            ))

        return chunks
