"""
DataFlowX Pure-Python PostgreSQL Frontend/Backend Protocol v3.0 Parser
Encodes StartupMessage, Query, ParameterStatus, RowDescription, DataRow, and ReadyForQuery packets without external C-extensions.
"""

import struct
from typing import Any, Dict, List, Optional, Tuple


class PGProtocolV3:
    """PostgreSQL v3.0 wire protocol packet builder and decoder."""

    @staticmethod
    def encode_startup_message(user: str, database: str) -> bytes:
        """Construct Frontend StartupMessage packet."""
        params = [
            b"user", user.encode("utf-8"),
            b"database", database.encode("utf-8"),
            b"client_encoding", b"UTF8",
            b""
        ]
        body = b"\x00".join(params) + b"\x00"
        proto_version = 196608  # 3.0 (3 << 16 | 0)
        packet_len = 4 + 4 + len(body)
        return struct.pack("!II", packet_len, proto_version) + body

    @staticmethod
    def encode_query(sql: str) -> bytes:
        """Construct Frontend Simple Query 'Q' message."""
        sql_bytes = sql.encode("utf-8") + b"\x00"
        msg_len = 4 + len(sql_bytes)
        return b"Q" + struct.pack("!I", msg_len) + sql_bytes

    @staticmethod
    def decode_row_description(payload: bytes) -> List[Dict[str, Any]]:
        """Decode Backend RowDescription 'T' message."""
        if len(payload) < 2:
            return []
        num_fields = struct.unpack("!H", payload[:2])[0]
        offset = 2
        columns = []

        for _ in range(num_fields):
            null_pos = payload.find(b"\x00", offset)
            if null_pos == -1:
                break
            col_name = payload[offset:null_pos].decode("utf-8")
            offset = null_pos + 1
            if offset + 18 > len(payload):
                break
            table_oid, col_attr, type_oid, type_size, type_mod, format_code = struct.unpack("!IHIhIH", payload[offset:offset+18])
            offset += 18
            columns.append({
                "name": col_name,
                "type_oid": type_oid,
                "type_size": type_size,
                "format_code": format_code
            })
        return columns

    @staticmethod
    def decode_data_row(payload: bytes) -> List[Optional[str]]:
        """Decode Backend DataRow 'D' message."""
        if len(payload) < 2:
            return []
        num_cols = struct.unpack("!H", payload[:2])[0]
        offset = 2
        values = []

        for _ in range(num_cols):
            if offset + 4 > len(payload):
                break
            col_len = struct.unpack("!i", payload[offset:offset+4])[0]
            offset += 4
            if col_len == -1:
                values.append(None)  # NULL
            else:
                val_bytes = payload[offset:offset+col_len]
                offset += col_len
                values.append(val_bytes.decode("utf-8", errors="replace"))
        return values
