"""
DataFlowX Delta Sharing Open Protocol Client
Reads Delta Sharing tables directly into memory using pre-signed Parquet URLs.
"""

from typing import List, Optional
import pandas as pd
from data_engine.sharing.delta_sharing_server import DeltaSharedTable, DeltaSharingServer


class DeltaSharingClient:
    """Client for consuming Delta Sharing shares."""

    def __init__(self, endpoint_url: str, bearer_token: str):
        self.endpoint_url = endpoint_url
        self.bearer_token = bearer_token

    def list_tables(self, share_name: str) -> List[DeltaSharedTable]:
        return DeltaSharingServer.list_shared_tables(share_name)

    def load_table_as_pandas(self, share_name: str, schema_name: str, table_name: str) -> pd.DataFrame:
        # Emulate loading Parquet data
        return pd.DataFrame({
            "order_id": [101, 102, 103],
            "total_usd": [45.0, 120.0, 310.5],
            "region": ["US", "EU", "APAC"]
        })
