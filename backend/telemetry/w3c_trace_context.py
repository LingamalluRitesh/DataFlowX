"""
DataFlowX W3C Trace Context Standard Header Injector & Extractor
Formats and parses standard W3C `traceparent` headers (`00-{trace_id}-{span_id}-{trace_flags}`) for distributed trace propagation across async DAG workers.
"""

import os
import secrets
from typing import Dict, Optional
from pydantic import BaseModel


class W3CTraceContext(BaseModel):
    version: str = "00"
    trace_id: str
    parent_span_id: str
    trace_flags: str = "01"

    def to_header(self) -> str:
        return f"{self.version}-{self.trace_id}-{self.parent_span_id}-{self.trace_flags}"

    @classmethod
    def new_trace(cls) -> "W3CTraceContext":
        return cls(
            trace_id=secrets.token_hex(16),
            parent_span_id=secrets.token_hex(8),
            trace_flags="01"
        )

    @classmethod
    def from_header(cls, header_val: str) -> Optional["W3CTraceContext"]:
        parts = header_val.strip().split("-")
        if len(parts) == 4:
            return cls(version=parts[0], trace_id=parts[1], parent_span_id=parts[2], trace_flags=parts[3])
        return None
