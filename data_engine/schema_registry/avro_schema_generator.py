"""
DataFlowX DataFrame to Apache Avro JSON Schema Generator
Converts tabular schema structures into standard Apache Avro JSON schema specifications.
"""

import json
from typing import Dict, List


class AvroSchemaGenerator:
    """Generates Avro JSON schema strings."""

    @classmethod
    def generate_avro_schema(cls, record_name: str, namespace: str, columns: Dict[str, str]) -> str:
        type_mapping = {
            "INT": "int",
            "BIGINT": "long",
            "FLOAT": "float",
            "DOUBLE": "double",
            "STRING": "string",
            "BOOLEAN": "boolean"
        }
        fields = []
        for col_name, c_type in columns.items():
            avro_t = type_mapping.get(c_type.upper(), "string")
            fields.append({"name": col_name, "type": ["null", avro_t], "default": None})

        schema = {
            "type": "record",
            "name": record_name,
            "namespace": namespace,
            "fields": fields
        }
        return json.dumps(schema, indent=2)
