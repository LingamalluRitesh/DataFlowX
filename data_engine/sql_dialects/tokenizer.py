"""
DataFlowX SQL Lexer & Tokenizer
Scans raw SQL string and produces classified token stream for AST compilation.
"""

from enum import Enum, auto
import re
from typing import Any, List, Optional
from pydantic import BaseModel


class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    OPERATOR = auto()
    PUNCTUATION = auto()
    WHITESPACE = auto()
    EOF = auto()


class Token(BaseModel):
    type: TokenType
    value: str
    position: int


class SQLTokenizer:
    """Vectorized SQL Lexer."""

    KEYWORDS = {
        "SELECT", "FROM", "WHERE", "GROUP", "BY", "HAVING", "ORDER", "LIMIT", "OFFSET",
        "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "CROSS", "ON", "AS", "AND", "OR", "NOT",
        "IN", "IS", "NULL", "LIKE", "BETWEEN", "CASE", "WHEN", "THEN", "ELSE", "END",
        "OVER", "PARTITION", "DISTINCT", "UNION", "ALL", "CREATE", "TABLE", "VIEW", "DROP"
    }

    TOKEN_SPEC = [
        ("NUMBER", r"\b\d+(?:\.\d+)?\b"),
        ("STRING", r"'[^']*'"),
        ("OPERATOR", r"<=|>=|!=|<>|=|<|>|\+|-|\*|/|%"),
        ("PUNCTUATION", r"[(),;.]"),
        ("IDENTIFIER", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
        ("WHITESPACE", r"\s+"),
    ]

    MASTER_REGEX = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))

    @classmethod
    def tokenize(cls, sql: str) -> List[Token]:
        tokens = []
        for match in cls.MASTER_REGEX.finditer(sql):
            kind = match.lastgroup
            val = match.group()
            pos = match.start()

            if kind == "WHITESPACE":
                continue
            elif kind == "IDENTIFIER" and val.upper() in cls.KEYWORDS:
                tokens.append(Token(type=TokenType.KEYWORD, value=val.upper(), position=pos))
            elif kind == "IDENTIFIER":
                tokens.append(Token(type=TokenType.IDENTIFIER, value=val, position=pos))
            elif kind == "NUMBER":
                tokens.append(Token(type=TokenType.NUMBER, value=val, position=pos))
            elif kind == "STRING":
                tokens.append(Token(type=TokenType.STRING, value=val[1:-1], position=pos))
            elif kind == "OPERATOR":
                tokens.append(Token(type=TokenType.OPERATOR, value=val, position=pos))
            elif kind == "PUNCTUATION":
                tokens.append(Token(type=TokenType.PUNCTUATION, value=val, position=pos))

        tokens.append(Token(type=TokenType.EOF, value="", position=len(sql)))
        return tokens
