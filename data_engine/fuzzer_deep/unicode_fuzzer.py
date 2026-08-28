"""
DataFlowX Unicode & String Attack Vector Fuzzer
Generates tricky Unicode payloads, zero-width joiners, emoji surrogates, RTL markers, and SQL injection strings to test pipeline sanitization.
"""

from typing import List


class UnicodeFuzzer:
    """Generates complex string edge cases."""

    SAMPLE_FUZZ_STRINGS: List[str] = [
        "🔥🚀✨🎉",
        "مرحبا بالعالم (Arabic RTL)",
        "Z̸̢͖͖̲̆̇Á̴̱L̸̨̗̎G̶̙̈́O̶̱̓",
        "Robert'); DROP TABLE Students;--",
        "NULL\x00BYTE_ATTACK",
        "<script>alert('xss')</script>",
        "¯\\_(ツ)_/¯",
        "\u200B\u200C\u200D (Zero Width Chars)"
    ]

    @classmethod
    def get_fuzz_sample(cls) -> List[str]:
        return list(cls.SAMPLE_FUZZ_STRINGS)
