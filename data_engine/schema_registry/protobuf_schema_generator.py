"""
DataFlowX DataFrame to Google Protocol Buffers proto3 Generator
Converts tabular schema definitions into standard Google Protocol Buffers `syntax = "proto3";` message definitions.
"""

from typing import Dict


class ProtobufSchemaGenerator:
    """Generates proto3 message definitions."""

    @classmethod
    def generate_proto3_schema(cls, message_name: str, package_name: str, columns: Dict[str, str]) -> str:
        type_mapping = {
            "INT": "int32",
            "BIGINT": "int64",
            "FLOAT": "float",
            "DOUBLE": "double",
            "STRING": "string",
            "BOOLEAN": "bool"
        }
        lines = [
            'syntax = "proto3";',
            f"package {package_name};",
            "",
            f"message {message_name} {{"
        ]

        field_num = 1
        for col_name, c_type in columns.items():
            proto_t = type_mapping.get(c_type.upper(), "string")
            lines.append(f"  {proto_t} {col_name} = {field_num};")
            field_num += 1

        lines.append("}")
        return "\n".join(lines) + "\n"
