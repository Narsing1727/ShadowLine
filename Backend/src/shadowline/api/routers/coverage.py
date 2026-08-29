"""Coverage tier API router."""

from fastapi import APIRouter, Depends
from shadowline.api.deps import get_service_container
from shadowline.api.schemas.coverage import LineCoverageResponse, StationCoverageItem
from shadowline.orchestration.lifecycle import ServiceContainer

router = APIRouter(prefix="/api/coverage", tags=["Coverage"])


@router.get("", response_model=LineCoverageResponse)
async def get_line_coverage(container: ServiceContainer = Depends(get_service_container)):
    top = container.topology
    stations = list(top.stations.values())

    measured = sum(1 for s in stations if s.confidence_tier.value == "MEASURED")
    inferred = sum(1 for s in stations if s.confidence_tier.value == "INFERRED")
    dark = sum(1 for s in stations if s.confidence_tier.value == "DARK")
    total = len(stations)

    cov_pct = ((measured + inferred) / total * 100.0) if total > 0 else 0.0

    items = [
        StationCoverageItem(
            station_id=s.id,
            station_name=s.name,
            zone=s.zone.value if hasattr(s.zone, "value") else str(s.zone),
            confidence_tier=s.confidence_tier.value,
        )
        for s in stations
    ]

    return LineCoverageResponse(
        total_stations=total,
        measured_count=measured,
        inferred_count=inferred,
        dark_count=dark,
        coverage_percentage=round(cov_pct, 1),
        stations=items,
    )
