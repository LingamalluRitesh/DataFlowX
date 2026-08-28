from backend.api.v1.extra.catalogs import router as catalogs_router
from backend.api.v1.extra.federation import router as federation_router
from backend.api.v1.extra.feature_store import router as feature_store_router
from backend.api.v1.extra.healing import router as healing_router
from backend.api.v1.extra.mpp import router as mpp_router
from backend.api.v1.extra.optimizer import router as optimizer_router
from backend.api.v1.extra.privacy_adv import router as privacy_adv_router

__all__ = [
    "federation_router",
    "optimizer_router",
    "feature_store_router",
    "privacy_adv_router",
    "mpp_router",
    "healing_router",
    "catalogs_router",
]
