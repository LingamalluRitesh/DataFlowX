"""
DataFlowX ANSI SQL:2016 Grammar Lexicon & Standard Function Registry
Defines keywords, reserved symbols, operator precedence tables, data type mappings, and built-in function signatures across SQL dialects.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field


class SQLFunctionSignature(BaseModel):
    name: str
    return_type: str
    min_args: int
    max_args: int
    is_aggregate: bool = False
    is_window: bool = False
    description: str


class SQLDataTypeMapping(BaseModel):
    standard_name: str
    postgres: str
    snowflake: str
    bigquery: str
    spark: str
    duckdb: str
    oracle: str


class SQLGrammarRegistry:
    """Standard SQL Grammar rules and function mappings."""

    OPERATOR_PRECEDENCE: Dict[str, int] = {
        "OR": 1,
        "AND": 2,
        "NOT": 3,
        "IS": 4,
        "IN": 4,
        "LIKE": 4,
        "BETWEEN": 4,
        "=": 5,
        "!=": 5,
        "<>": 5,
        "<": 5,
        "<=": 5,
        ">": 5,
        ">=": 5,
        "+": 6,
        "-": 6,
        "*": 7,
        "/": 7,
        "%": 7,
    }

    BUILTIN_FUNCTIONS: Dict[str, SQLFunctionSignature] = {
        # Scalar Mathematical
        "ABS": SQLFunctionSignature(name="ABS", return_type="DOUBLE", min_args=1, max_args=1, description="Absolute numeric value"),
        "CEIL": SQLFunctionSignature(name="CEIL", return_type="BIGINT", min_args=1, max_args=1, description="Smallest integer greater than or equal to argument"),
        "FLOOR": SQLFunctionSignature(name="FLOOR", return_type="BIGINT", min_args=1, max_args=1, description="Largest integer less than or equal to argument"),
        "ROUND": SQLFunctionSignature(name="ROUND", return_type="DOUBLE", min_args=1, max_args=2, description="Rounds number to N decimal places"),
        "EXP": SQLFunctionSignature(name="EXP", return_type="DOUBLE", min_args=1, max_args=1, description="Euler exponential e^x"),
        "LN": SQLFunctionSignature(name="LN", return_type="DOUBLE", min_args=1, max_args=1, description="Natural logarithm base e"),
        "LOG10": SQLFunctionSignature(name="LOG10", return_type="DOUBLE", min_args=1, max_args=1, description="Base 10 logarithm"),
        "POWER": SQLFunctionSignature(name="POWER", return_type="DOUBLE", min_args=2, max_args=2, description="Exponentiation x^y"),
        "SQRT": SQLFunctionSignature(name="SQRT", return_type="DOUBLE", min_args=1, max_args=1, description="Square root"),
        # String Manipulation
        "CONCAT": SQLFunctionSignature(name="CONCAT", return_type="STRING", min_args=2, max_args=99, description="Concatenates strings"),
        "LOWER": SQLFunctionSignature(name="LOWER", return_type="STRING", min_args=1, max_args=1, description="Converts to lowercase"),
        "UPPER": SQLFunctionSignature(name="UPPER", return_type="STRING", min_args=1, max_args=1, description="Converts to uppercase"),
        "TRIM": SQLFunctionSignature(name="TRIM", return_type="STRING", min_args=1, max_args=1, description="Strips leading and trailing spaces"),
        "SUBSTRING": SQLFunctionSignature(name="SUBSTRING", return_type="STRING", min_args=2, max_args=3, description="Extracts substring by offset and length"),
        "LENGTH": SQLFunctionSignature(name="LENGTH", return_type="INTEGER", min_args=1, max_args=1, description="Character count length"),
        "REPLACE": SQLFunctionSignature(name="REPLACE", return_type="STRING", min_args=3, max_args=3, description="Replaces substring occurrences"),
        "LPAD": SQLFunctionSignature(name="LPAD", return_type="STRING", min_args=3, max_args=3, description="Left-pads string to target width"),
        "RPAD": SQLFunctionSignature(name="RPAD", return_type="STRING", min_args=3, max_args=3, description="Right-pads string to target width"),
        "REVERSE": SQLFunctionSignature(name="REVERSE", return_type="STRING", min_args=1, max_args=1, description="Reverses character order"),
        # Date & Temporal
        "CURRENT_DATE": SQLFunctionSignature(name="CURRENT_DATE", return_type="DATE", min_args=0, max_args=0, description="Current UTC calendar date"),
        "CURRENT_TIMESTAMP": SQLFunctionSignature(name="CURRENT_TIMESTAMP", return_type="TIMESTAMP", min_args=0, max_args=0, description="Current UTC timestamp with timezone"),
        "DATE_TRUNC": SQLFunctionSignature(name="DATE_TRUNC", return_type="TIMESTAMP", min_args=2, max_args=2, description="Truncates date/time to specified granularity"),
        "EXTRACT": SQLFunctionSignature(name="EXTRACT", return_type="INTEGER", min_args=2, max_args=2, description="Extracts temporal part (year, month, day, hour)"),
        "DATEDIFF": SQLFunctionSignature(name="DATEDIFF", return_type="INTEGER", min_args=3, max_args=3, description="Difference between two timestamps in units"),
        # Aggregations
        "COUNT": SQLFunctionSignature(name="COUNT", return_type="BIGINT", min_args=1, max_args=1, is_aggregate=True, description="Counts non-null records"),
        "SUM": SQLFunctionSignature(name="SUM", return_type="DOUBLE", min_args=1, max_args=1, is_aggregate=True, description="Sums numeric values"),
        "AVG": SQLFunctionSignature(name="AVG", return_type="DOUBLE", min_args=1, max_args=1, is_aggregate=True, description="Arithmetic mean average"),
        "MIN": SQLFunctionSignature(name="MIN", return_type="ANY", min_args=1, max_args=1, is_aggregate=True, description="Minimum value in set"),
        "MAX": SQLFunctionSignature(name="MAX", return_type="ANY", min_args=1, max_args=1, is_aggregate=True, description="Maximum value in set"),
        "STDDEV": SQLFunctionSignature(name="STDDEV", return_type="DOUBLE", min_args=1, max_args=1, is_aggregate=True, description="Sample standard deviation"),
        "VARIANCE": SQLFunctionSignature(name="VARIANCE", return_type="DOUBLE", min_args=1, max_args=1, is_aggregate=True, description="Sample statistical variance"),
        # Window Analytical
        "ROW_NUMBER": SQLFunctionSignature(name="ROW_NUMBER", return_type="BIGINT", min_args=0, max_args=0, is_window=True, description="Sequential row number per partition"),
        "RANK": SQLFunctionSignature(name="RANK", return_type="BIGINT", min_args=0, max_args=0, is_window=True, description="Rank with gaps for ties"),
        "DENSE_RANK": SQLFunctionSignature(name="DENSE_RANK", return_type="BIGINT", min_args=0, max_args=0, is_window=True, description="Dense rank without gaps"),
        "LEAD": SQLFunctionSignature(name="LEAD", return_type="ANY", min_args=1, max_args=3, is_window=True, description="Evaluates expression on subsequent row"),
        "LAG": SQLFunctionSignature(name="LAG", return_type="ANY", min_args=1, max_args=3, is_window=True, description="Evaluates expression on preceding row"),
        "FIRST_VALUE": SQLFunctionSignature(name="FIRST_VALUE", return_type="ANY", min_args=1, max_args=1, is_window=True, description="First value in window frame"),
        "LAST_VALUE": SQLFunctionSignature(name="LAST_VALUE", return_type="ANY", min_args=1, max_args=1, is_window=True, description="Last value in window frame"),
        "NTILE": SQLFunctionSignature(name="NTILE", return_type="INTEGER", min_args=1, max_args=1, is_window=True, description="Divides partition into N buckets"),
    }

    TYPE_MAPPINGS: Dict[str, SQLDataTypeMapping] = {
        "STRING": SQLDataTypeMapping(standard_name="STRING", postgres="VARCHAR", snowflake="VARCHAR", bigquery="STRING", spark="STRING", duckdb="VARCHAR", oracle="VARCHAR2(4000)"),
        "INTEGER": SQLDataTypeMapping(standard_name="INTEGER", postgres="INTEGER", snowflake="INTEGER", bigquery="INT64", spark="INT", duckdb="INTEGER", oracle="NUMBER(10)"),
        "BIGINT": SQLDataTypeMapping(standard_name="BIGINT", postgres="BIGINT", snowflake="NUMBER(38,0)", bigquery="INT64", spark="BIGINT", duckdb="BIGINT", oracle="NUMBER(19)"),
        "DOUBLE": SQLDataTypeMapping(standard_name="DOUBLE", postgres="DOUBLE PRECISION", snowflake="FLOAT", bigquery="FLOAT64", spark="DOUBLE", duckdb="DOUBLE", oracle="BINARY_DOUBLE"),
        "BOOLEAN": SQLDataTypeMapping(standard_name="BOOLEAN", postgres="BOOLEAN", snowflake="BOOLEAN", bigquery="BOOL", spark="BOOLEAN", duckdb="BOOLEAN", oracle="NUMBER(1)"),
        "TIMESTAMP": SQLDataTypeMapping(standard_name="TIMESTAMP", postgres="TIMESTAMP WITH TIME ZONE", snowflake="TIMESTAMP_NTZ", bigquery="TIMESTAMP", spark="TIMESTAMP", duckdb="TIMESTAMP", oracle="TIMESTAMP"),
        "DATE": SQLDataTypeMapping(standard_name="DATE", postgres="DATE", snowflake="DATE", bigquery="DATE", spark="DATE", duckdb="DATE", oracle="DATE"),
        "JSON": SQLDataTypeMapping(standard_name="JSON", postgres="JSONB", snowflake="VARIANT", bigquery="JSON", spark="STRING", duckdb="JSON", oracle="CLOB"),
    }
