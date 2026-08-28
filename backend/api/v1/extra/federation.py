from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.extra.federation_service import FederationService

router = APIRouter(prefix="/federation", tags=["Query Federation"])
_service = FederationService()


class MappingCreateRequest(BaseModel):
    virtual_name: str
    connector_type: str
    physical_table: str
    database_name: str = "default"


@router.get("/tables")
def list_virtual_tables() -> List[Dict[str, Any]]:
    mappings = _service.list_mappings()
    return [m.dict() for m in mappings]


@router.post("/tables")
def create_virtual_table(req: MappingCreateRequest) -> Dict[str, Any]:
    mapping = _service.register_mapping(
        req.virtual_name,
        req.connector_type,
        req.physical_table,
        req.database_name
    )
    return {"message": "Virtual table registered successfully", "mapping": mapping.dict()}
