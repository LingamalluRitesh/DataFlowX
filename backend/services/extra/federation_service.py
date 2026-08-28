"""
DataFlowX Query Federation Service Layer
Manages virtual table mappings, remote dialect pushdowns, and in-memory federated joins.
"""

from typing import Any, Dict, List, Optional
import pandas as pd
from pydantic import BaseModel, Field

from backend.core.logging import get_logger
from data_engine.federation.logical_federator import FederatedTableMapping, LogicalQueryFederator

logger = get_logger(__name__)


class FederationService:
    """Service layer managing query federation."""

    def __init__(self):
        self.federator = LogicalQueryFederator()

    def register_mapping(self, virtual_name: str, connector_type: str, physical_table: str, db_name: str = "default") -> FederatedTableMapping:
        mapping = FederatedTableMapping(
            virtual_table_name=virtual_name,
            connector_type=connector_type,
            physical_table_name=physical_table,
            database_name=db_name
        )
        self.federator.register_virtual_table(mapping)
        return mapping

    def list_mappings(self) -> List[FederatedTableMapping]:
        return list(self.federator.mappings.values())
