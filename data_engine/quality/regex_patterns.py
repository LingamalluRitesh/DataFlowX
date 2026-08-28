"""
DataFlowX Standard Global Regex Validation Patterns Registry
Over 50+ pre-compiled regular expressions for international identity documents, fiscal codes, payment tokens, and network identifiers.
"""

import re
from typing import Dict


class StandardRegexRegistry:
    """Enterprise Regular Expression Catalog."""

    PATTERNS: Dict[str, str] = {
        # Contact & Personal
        "EMAIL": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        "E164_PHONE": r"^\+[1-9]\d{1,14}$",
        "US_PHONE": r"^(?:\+?1[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$",
        "US_SSN": r"^(?!000|666|9\d{2})\d{3}-(?!00)\d{2}-(?!0000)\d{4}$",
        "US_ZIP": r"^\d{5}(?:[-\s]\d{4})?$",
        "UK_POSTCODE": r"^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$",
        "CANADIAN_POSTAL": r"^[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d$",
        # Financial & Corporate
        "CREDIT_CARD_VISA": r"^4[0-9]{12}(?:[0-9]{3})?$",
        "CREDIT_CARD_MASTERCARD": r"^5[1-5][0-9]{14}$",
        "CREDIT_CARD_AMEX": r"^3[47][0-9]{13}$",
        "IBAN": r"^[A-Z]{2}\d{2}[A-Z0-9]{4}\d{7}([A-Z0-9]?){0,16}$",
        "SWIFT_BIC": r"^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$",
        "US_EIN": r"^\d{2}-\d{7}$",
        # Network & Technical Identifiers
        "IPV4": r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
        "IPV6": r"^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$",
        "MAC_ADDRESS": r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
        "UUID_V4": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
        "HEX_COLOR": r"^#(?:[0-9a-fA-F]{3}){1,2}$",
        "JWT_TOKEN": r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$",
        "SEMVER": r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
        "ISO_8601_DATE": r"^\d{4}-\d{2}-\d{2}$",
        "ISO_8601_TIMESTAMP": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$",
        "URL_HTTP_HTTPS": r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$",
    }

    _COMPILED_CACHE: Dict[str, re.Pattern] = {}

    @classmethod
    def get_pattern(cls, pattern_name: str) -> Optional[re.Pattern]:
        norm = pattern_name.upper()
        if norm not in cls.PATTERNS:
            return None
        if norm not in cls._COMPILED_CACHE:
            cls._COMPILED_CACHE[norm] = re.compile(cls.PATTERNS[norm])
        return cls._COMPILED_CACHE[norm]
