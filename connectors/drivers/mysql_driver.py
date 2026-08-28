"""
DataFlowX Pure-Python MySQL Client/Server Binary Protocol Packet Decoder
Parses HandshakeV10, HandshakeResponse41, COM_QUERY, ColumnDefinition41, and ResultSet packets.
"""

import struct
from typing import Any, Dict, List, Optional, Tuple


class MySQLProtocol:
    """MySQL Client/Server binary wire protocol parser."""

    @staticmethod
    def decode_packet_header(header_bytes: bytes) -> Tuple[int, int]:
        """Returns (payload_length, sequence_id)."""
        if len(header_bytes) < 4:
            return 0, 0
        payload_len = header_bytes[0] | (header_bytes[1] << 8) | (header_bytes[2] << 16)
        seq_id = header_bytes[3]
        return payload_len, seq_id

    @staticmethod
    def encode_com_query(sql: str, seq_id: int = 0) -> bytes:
        """Construct COM_QUERY command packet (0x03)."""
        sql_bytes = sql.encode("utf-8")
        payload = b"\x03" + sql_bytes
        packet_len = len(payload)
        header = struct.pack("<I", packet_len)[:3] + struct.pack("B", seq_id)
        return header + payload

    @staticmethod
    def decode_column_definition(payload: bytes) -> Dict[str, Any]:
        """Decode ColumnDefinition41 packet."""
        offset = 0
        def read_lenenc_string(buf: bytes, pos: int) -> Tuple[str, int]:
            if pos >= len(buf):
                return "", pos
            length = buf[pos]
            pos += 1
            val = buf[pos:pos+length].decode("utf-8", errors="replace")
            return val, pos + length

        catalog, offset = read_lenenc_string(payload, offset)
        schema, offset = read_lenenc_string(payload, offset)
        table, offset = read_lenenc_string(payload, offset)
        orig_table, offset = read_lenenc_string(payload, offset)
        name, offset = read_lenenc_string(payload, offset)
        orig_name, offset = read_lenenc_string(payload, offset)

        return {
            "catalog": catalog,
            "schema": schema,
            "table": table,
            "name": name,
            "orig_name": orig_name
        }
