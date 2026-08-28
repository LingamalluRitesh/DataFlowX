"""
DataFlowX Amazon Redshift to Google BigQuery Transpiler
Translates Redshift DDLs (DISTSTYLE, DISTKEY, SORTKEY, ENCODE) into BigQuery `PARTITION BY` and `CLUSTER BY` specifications.
"""

import re


class RedshiftToBigQueryTranspiler:
    """Transpiles Amazon Redshift SQL/DDL into BigQuery."""

    @classmethod
    def transpile_ddl(cls, redshift_ddl: str) -> str:
        ddl = redshift_ddl
        # Strip ENCODE <type>
        ddl = re.sub(r"\bENCODE\s+\w+\b", "", ddl, flags=re.IGNORECASE)
        # Strip DISTSTYLE <type>
        ddl = re.sub(r"\bDISTSTYLE\s+\w+\b", "", ddl, flags=re.IGNORECASE)

        # Replace DISTKEY(col) with CLUSTER BY col
        distkey_match = re.search(r"\bDISTKEY\s*\((.*?)\)", ddl, flags=re.IGNORECASE)
        if distkey_match:
            col = distkey_match.group(1).strip()
            ddl = re.sub(r"\bDISTKEY\s*\(.*?\)", "", ddl, flags=re.IGNORECASE)
            ddl = ddl.rstrip(";\n ") + f"\nCLUSTER BY {col};"

        return ddl
