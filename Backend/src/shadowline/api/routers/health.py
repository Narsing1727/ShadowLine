"""Health check router."""

from fastapi import APIRouter, Depends
from shadowline.api.deps import get_service_container
from shadowline.orchestration.lifecycle import ServiceContainer

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(container: ServiceContainer = Depends(get_service_container)):
    ingest_health = await container.ingestion_adapter.get_health()
    return {
        "status": "UP",
        "mode": container.mode_manager.current_mode.value,
        "line_id": container.topology.line_id,
        "ingestion": ingest_health,
        "metrics": container.metrics_collector.get_metrics(),
    }
