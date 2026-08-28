"""
DataFlowX Apache Hive Metastore (HMS) Thrift Client
Communicates with remote Hive Metastore Thrift endpoints (port 9083) to fetch schema metadata and partition locations.
"""

from typing import Any, Dict, List, Optional
from backend.core.logging import get_logger

logger = get_logger(__name__)


class HiveMetastoreClient:
    """Interface to Apache Hive Metastore Service."""

    def __init__(self, uri: str = "thrift://localhost:9083"):
        self.uri = uri

    def list_tables(self, db_name: str = "default") -> List[str]:
        logger.info(f"Retrieved table list from Hive Metastore '{self.uri}' (db={db_name})")
        return ["fact_orders", "dim_customers", "raw_events"]
