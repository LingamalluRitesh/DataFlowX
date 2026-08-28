"""
DataFlowX SQL Lexer & Tokenizer
Transforms raw SQL string queries into streams of categorized tokens for parsing.
"""

from enum import Enum
import re
from typing import Generator, List, Optional
from pydantic import BaseModel


class TokenType(str, Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    STRING_LITERAL = "STRING_LITERAL"
    NUMERIC_LITERAL = "NUMERIC_LITERAL"
    OPERATOR = "OPERATOR"
    PUNCTUATION = "PUNCTUATION"
    PARAMETER = "PARAMETER"
    EOF = "EOF"


class Token(BaseModel):
    token_type: TokenType
    value: str
    line: int
    column: int


class SQLLexer:
    """Lexer splitting SQL text into token stream."""

    KEYWORDS = {
        "SELECT", "FROM", "WHERE", "JOIN", "INNER", "LEFT", "RIGHT", "FULL", "CROSS",
        "ON", "GROUP", "BY", "HAVING", "ORDER", "ASC", "DESC", "LIMIT", "OFFSET",
        "AS", "AND", "OR", "NOT", "IN", "IS", "NULL", "LIKE", "ILIKE", "BETWEEN",
        "CASE", "WHEN", "THEN", "ELSE", "END", "DISTINCT", "UNION", "ALL", "EXCEPT",
        "INTERSECT", "WITH", "RECURSIVE", "CREATE", "TABLE", "INSERT", "INTO", "VALUES",
        "UPDATE", "SET", "DELETE", "DROP", "ALTER", "PARTITION", "CLUSTER"
    }

    OPERATORS = {"=", "!=", "<>", ">", ">=", "<", "<=", "+", "-", "*", "/", "%", "||"}
    PUNCTUATIONS = {"(", ")", ",", ";", "."}

    def __init__(self, sql: str):
        self.sql = sql
        self.pos = 0
        self.line = 1
        self.column = 1
        self.length = len(sql)

    def _peek(self) -> Optional[str]:
        if self.pos < self.length:
            return self.sql[self.pos]
        return None

    def _advance(self) -> Optional[str]:
        ch = self._peek()
        if ch is not None:
            self.pos += 1
            if ch == "\n":
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        return ch

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while self.pos < self.length:
            ch = self._peek()
            if ch is None:
                break

            # Whitespace
            if ch.isspace():
                self._advance()
                continue

            # Line comments --
            if ch == "-" and self.pos + 1 < self.length and self.sql[self.pos + 1] == "-":
                while self._peek() is not None and self._peek() != "\n":
                    self._advance()
                continue

            # String literal '...'
            if ch in ("'", '"', "`"):
                quote_char = ch
                start_col = self.column
                start_line = self.line
                self._advance()
                chars = []
                while self._peek() is not None and self._peek() != quote_char:
                    chars.append(self._advance())
                if self._peek() == quote_char:
                    self._advance()
                val = "".join(chars)
                if quote_char in ('"', "`"):
                    tokens.append(Token(token_type=TokenType.IDENTIFIER, value=val, line=start_line, column=start_col))
                else:
                    tokens.append(Token(token_type=TokenType.STRING_LITERAL, value=val, line=start_line, column=start_col))
                continue

            # Numbers
            if ch.isdigit():
                start_col = self.column
                start_line = self.line
                chars = []
                has_dot = False
                while self._peek() is not None and (self._peek().isdigit() or (self._peek() == "." and not has_dot)):
                    if self._peek() == ".":
                        has_dot = True
                    chars.append(self._advance())
                tokens.append(Token(token_type=TokenType.NUMERIC_LITERAL, value="".join(chars), line=start_line, column=start_col))
                continue

            # Identifiers and keywords
            if ch.isalpha() or ch == "_":
                start_col = self.column
                start_line = self.line
                chars = []
                while self._peek() is not None and (self._peek().isalnum() or self._peek() == "_"):
                    chars.append(self._advance())
                word = "".join(chars)
                if word.upper() in self.KEYWORDS:
                    tokens.append(Token(token_type=TokenType.KEYWORD, value=word.upper(), line=start_line, column=start_col))
                else:
                    tokens.append(Token(token_type=TokenType.IDENTIFIER, value=word, line=start_line, column=start_col))
                continue

            # Operators
            if ch in "+-*/%=<>!|":
                start_col = self.column
                start_line = self.line
                op = self._advance()
                next_ch = self._peek()
                if next_ch and (op + next_ch) in self.OPERATORS:
                    op += self._advance()
                tokens.append(Token(token_type=TokenType.OPERATOR, value=op, line=start_line, column=start_col))
                continue

            # Punctuations
            if ch in self.PUNCTUATIONS:
                start_col = self.column
                start_line = self.line
                punc = self._advance()
                tokens.append(Token(token_type=TokenType.PUNCTUATION, value=punc, line=start_line, column=start_col))
                continue

            # Skip unknown character
            self._advance()

        tokens.append(Token(token_type=TokenType.EOF, value="", line=self.line, column=self.column))
        return tokens
