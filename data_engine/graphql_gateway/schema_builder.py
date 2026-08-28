"""
DataFlowX Dynamic GraphQL Schema Generator
Generates GraphQL SDL (Schema Definition Language) types and root queries dynamically from Lakehouse table schemas.
"""

from typing import Dict, List


class GraphQLSchemaBuilder:
    """Generates GraphQL schema definitions from tabular metadata."""

    @classmethod
    def generate_sdl(cls, type_name: str, fields: Dict[str, str]) -> str:
        type_map = {
            "INT": "Int",
            "BIGINT": "Int",
            "FLOAT": "Float",
            "DOUBLE": "Float",
            "STRING": "String",
            "BOOLEAN": "Boolean"
        }
        sdl_lines = [f"type {type_name} {{"]
        for f_name, f_type in fields.items():
            gql_t = type_map.get(f_type.upper(), "String")
            sdl_lines.append(f"  {f_name}: {gql_t}")
        sdl_lines.append("}")
        sdl_lines.append("")
        sdl_lines.append("type Query {")
        sdl_lines.append(f"  {type_name.lower()}s(limit: Int = 100, offset: Int = 0): [{type_name}]")
        sdl_lines.append(f"  {type_name.lower()}ById(id: String!): {type_name}")
        sdl_lines.append("}")
        return "\n".join(sdl_lines)
