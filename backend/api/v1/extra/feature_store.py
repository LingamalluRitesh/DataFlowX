from typing import Any, Dict, List
from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.extra.feature_store_service import FeatureStoreService
from data_engine.feature_store.feature_view import FeatureDefinition, FeatureView

router = APIRouter(prefix="/feature-store", tags=["Feature Store"])
_service = FeatureStoreService()


class FeatureViewCreateRequest(BaseModel):
    name: str
    entity_id_column: str
    timestamp_column: str
    source_dataset: str
    features: List[Dict[str, str]]


@router.get("/views")
def list_views() -> List[Dict[str, Any]]:
    return [v.dict() for v in _service.list_feature_views()]


@router.post("/views")
def create_view(req: FeatureViewCreateRequest) -> Dict[str, Any]:
    feat_defs = [FeatureDefinition(name=f["name"], data_type=f.get("data_type", "FLOAT"), description=f.get("description", "")) for f in req.features]
    view = FeatureView(
        name=req.name,
        entity_id_column=req.entity_id_column,
        timestamp_column=req.timestamp_column,
        source_dataset=req.source_dataset,
        features=feat_defs
    )
    res = _service.register_feature_view(view)
    return {"message": "Feature view registered", "view": res.dict()}
