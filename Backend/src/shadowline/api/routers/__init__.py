"""API routers package."""

from shadowline.api.routers.alerts import router as alerts_router
from shadowline.api.routers.bottleneck import router as bottleneck_router
from shadowline.api.routers.coverage import router as coverage_router
from shadowline.api.routers.defects import router as defects_router
from shadowline.api.routers.discovery import router as discovery_router
from shadowline.api.routers.genealogy import router as genealogy_router
from shadowline.api.routers.health import router as health_router
from shadowline.api.routers.impact import router as impact_router
from shadowline.api.routers.line import router as line_router
from shadowline.api.routers.predictions import router as predictions_router
from shadowline.api.routers.settings import router as settings_router
from shadowline.api.routers.stations import router as stations_router
from shadowline.api.routers.trust import router as trust_router

__all__ = [
    "alerts_router",
    "bottleneck_router",
    "coverage_router",
    "defects_router",
    "discovery_router",
    "genealogy_router",
    "health_router",
    "impact_router",
    "line_router",
    "predictions_router",
    "settings_router",
    "stations_router",
    "trust_router",
]
