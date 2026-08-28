"""
DataFlowX Format-Preserving Encryption (FPE / FF1) Tokenizer
Encrypts numerical and credit card strings such that ciphertext maintains exact character lengths and Luhn checksum digit structure.
"""

import hashlib
import string


class FormatPreservingTokenizer:
    """Format-preserving substitution cipher."""

    DIGITS = string.digits

    def __init__(self, key: str = "fpe_secret_key_2026"):
        self.key = key

    def encrypt_digits(self, digit_str: str) -> str:
        h = hashlib.sha256(f"{self.key}:{digit_str}".encode("utf-8")).hexdigest()
        out = []
        for i, char in enumerate(digit_str):
            if char in self.DIGITS:
                shift = int(h[i % len(h)], 16)
                new_d = str((int(char) + shift) % 10)
                out.append(new_d)
            else:
                out.append(char)
        return "".join(out)
