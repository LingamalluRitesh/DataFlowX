"""
DataFlowX Pure-Python TDS (Tabular Data Stream 7.4) Protocol Decoder
Decodes Microsoft SQL Server TDS packet headers, Pre-Login, Login7, and SQLBatch tokens.
"""

import struct
from typing import Any, Dict, List, Optional, Tuple


class TDSProtocol74:
    """TDS 7.4 packet header and token stream parser."""

    PACKET_TYPES = {
        1: "SQL_BATCH",
        2: "PRE_TDS7_LOGIN",
        3: "RPC",
        4: "TABULAR_RESULT",
        16: "LOGIN7",
        17: "SSPI",
        18: "PRE_LOGIN",
    }

    @staticmethod
    def decode_packet_header(header_bytes: bytes) -> Dict[str, Any]:
        if len(header_bytes) < 8:
            return {}
        pkt_type, status, length, spid, packet_id, window = struct.unpack("!BBHHBB", header_bytes)
        return {
            "type_id": pkt_type,
            "type_name": TDSProtocol74.PACKET_TYPES.get(pkt_type, "UNKNOWN"),
            "is_last_packet": bool(status & 0x01),
            "packet_length": length,
            "spid": spid,
            "packet_id": packet_id
        }

    @staticmethod
    def encode_sql_batch(sql: str) -> bytes:
        """Encode TDS SQL Batch packet."""
        unicode_sql = sql.encode("utf-16le")
        length = 8 + len(unicode_sql)
        header = struct.pack("!BBHHBB", 1, 1, length, 0, 1, 0)
        return header + unicode_sql
