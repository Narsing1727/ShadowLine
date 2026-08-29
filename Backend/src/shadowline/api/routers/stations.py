"""Station API router."""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from shadowline.api.deps import get_db, get_service_container
from shadowline.api.errors import ResourceNotFoundError
from shadowline.api.schemas.station import StationDetailResponse, StationHistoryItem, StationHistoryResponse
from shadowline.orchestration.lifecycle import ServiceContainer
from shadowline.persistence.repositories.stations import StationRepository

router = APIRouter(prefix="/api/stations", tags=["Stations"])


@router.get("", response_model=List[StationDetailResponse])
async def list_stations(container: ServiceContainer = Depends(get_service_container)):
    snapshot = container.state_store.snapshot()
    return [
        StationDetailResponse(
            id=s.id,
            name=s.name,
            zone=s.zone,
            confidence_tier=s.confidence_tier,
            nominal_cycle_time=s.nominal_cycle_time,
            current_state=s.current_state,
            current_unit_vin=s.current_unit_vin,
            last_cycle_time=s.last_cycle_time,
            active_period_seconds=s.active_period_seconds,
            blocked_period_seconds=s.blocked_period_seconds,
            starved_period_seconds=s.starved_period_seconds,
            down_period_seconds=s.down_period_seconds,
            total_units_processed=s.total_units_processed,
        )
        for s in snapshot.stations.values()
    ]


@router.get("/{station_id}", response_model=StationDetailResponse)
async def get_station(station_id: str, container: ServiceContainer = Depends(get_service_container)):
    snapshot = container.state_store.snapshot()
    s = snapshot.stations.get(station_id)
    if not s:
        raise ResourceNotFoundError("Station", station_id)

    return StationDetailResponse(
        id=s.id,
        name=s.name,
        zone=s.zone,
        confidence_tier=s.confidence_tier,
        nominal_cycle_time=s.nominal_cycle_time,
        current_state=s.current_state,
        current_unit_vin=s.current_unit_vin,
        last_cycle_time=s.last_cycle_time,
        active_period_seconds=s.active_period_seconds,
        blocked_period_seconds=s.blocked_period_seconds,
        starved_period_seconds=s.starved_period_seconds,
        down_period_seconds=s.down_period_seconds,
        total_units_processed=s.total_units_processed,
    )


@router.get("/{station_id}/history", response_model=StationHistoryResponse)
async def get_station_history(
    station_id: str,
    db: Session = Depends(get_db),
    container: ServiceContainer = Depends(get_service_container),
):
    if station_id not in container.topology.stations:
        raise ResourceNotFoundError("Station", station_id)

    repo = StationRepository(db)
    records = repo.get_station_history(station_id, limit=100)
    items = [
        StationHistoryItem(
            state=r.state,
            cycle_time_seconds=r.cycle_time_seconds,
            vin=r.vin,
            occurred_at=r.occurred_at.isoformat(),
        )
        for r in records
    ]

    return StationHistoryResponse(station_id=station_id, history=items)
