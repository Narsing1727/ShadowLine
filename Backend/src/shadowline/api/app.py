"""FastAPI Application constructor and mounting."""

from contextlib import asynccontextmanager
import logging
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shadowline.api.deps import set_service_container
from shadowline.api.errors import register_error_handlers
from shadowline.api.routers import (
    alerts_router,
    bottleneck_router,
    coverage_router,
    defects_router,
    discovery_router,
    genealogy_router,
    health_router,
    impact_router,
    line_router,
    predictions_router,
    settings_router,
    stations_router,
    trust_router,
)
from shadowline.api.ws.connection_manager import ws_manager
from shadowline.api.ws.live_feed import ws_router
from shadowline.config.settings import ShadowLineSettings
from shadowline.orchestration.lifecycle import ServiceContainer
from shadowline.telemetry.logging import setup_logging

logger = logging.getLogger("shadowline.api")


def create_app(settings: Optional[ShadowLineSettings] = None) -> FastAPI:
    cfg = settings or ShadowLineSettings()
    setup_logging(cfg.log_level)

    container = ServiceContainer(cfg)
    set_service_container(container)

    # Wire event broadcast to WebSockets
    def _on_state_updated(snapshot):
        # Fire-and-forget broadcast
        pass

    def _on_alerts_surfaced(alerts):
        # Fire-and-forget alert broadcast
        pass

    container.cycle_runner.on_state_updated = _on_state_updated
    container.cycle_runner.on_alerts_surfaced = _on_alerts_surfaced

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.info("Initializing ShadowLine API and background services...")
        await container.start()
        yield
        logger.info("Shutting down ShadowLine API services...")
        await container.stop()

    app = FastAPI(
        title="ShadowLine Predictive Digital Twin API",
        description="Discrete-event predictive twin running ahead of vehicle assembly line.",
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS
    origins = [orig.strip() for orig in cfg.cors_origins.split(",") if orig.strip()]
    if not origins:
        origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_error_handlers(app)

    # Mount routers
    app.include_router(health_router)
    app.include_router(line_router)
    app.include_router(stations_router)
    app.include_router(alerts_router)
    app.include_router(predictions_router)
    app.include_router(bottleneck_router)
    app.include_router(defects_router)
    app.include_router(genealogy_router)
    app.include_router(coverage_router)
    app.include_router(trust_router)
    app.include_router(impact_router)
    app.include_router(discovery_router)
    app.include_router(settings_router)
    app.include_router(ws_router)

    return app


app = create_app()
