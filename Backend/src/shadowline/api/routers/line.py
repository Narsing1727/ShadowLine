"""Line metadata and state API router."""

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from shadowline.api.deps import get_service_container
from shadowline.api.schemas.line import (
    BufferStateSchema,
    LineMetadataResponse,
    LineStateResponse,
    SimulationMetadataResponse,
    StationStateSummarySchema,
)
from shadowline.domain.enums import StationState
from shadowline.orchestration.lifecycle import ServiceContainer
from shadowline.twin.advance import AdvanceResult, TwinAdvancer
from shadowline.twin.fork import TwinForker

router = APIRouter(prefix="/api/line", tags=["Line"])


@router.get("", response_model=LineMetadataResponse)
async def get_line_metadata(container: ServiceContainer = Depends(get_service_container)):
    top = container.topology
    return LineMetadataResponse(
        line_id=top.line_id,
        name=top.name,
        takt_time_seconds=top.takt_time_seconds,
        target_jph=top.target_jph,
        shifts_per_day=top.shifts_per_day,
        hours_per_shift=top.hours_per_shift,
        mode=container.mode_manager.current_mode.value,
        total_stations=len(top.stations),
        total_buffers=len(top.buffers),
    )


@router.get("/state", response_model=LineStateResponse)
async def get_line_state(
    horizon: Optional[str] = Query(None, description="Optional forward horizon (e.g. 1h, 2h, 4h)"),
    container: ServiceContainer = Depends(get_service_container),
):
    snapshot = container.state_store.snapshot()
    horizon_hours = 0.0

    if horizon:
        try:
            horizon_hours = float(horizon.replace("h", ""))
        except Exception:
            horizon_hours = 1.0

        # Advance forked twin to horizon
        forked = TwinForker.fork(snapshot, takt_time=container.topology.takt_time_seconds)
        adv_res = TwinAdvancer.advance(forked, horizon_seconds=horizon_hours * 3600.0)

    station_schemas = [
        StationStateSummarySchema(
            id=s.id,
            name=s.name,
            zone=s.zone,
            confidence_tier=s.confidence_tier,
            current_state=s.current_state,
            nominal_cycle_time=s.nominal_cycle_time,
            last_cycle_time=s.last_cycle_time,
            current_unit_vin=s.current_unit_vin,
        )
        for s in snapshot.stations.values()
    ]

    buffer_schemas = [
        BufferStateSchema(
            id=b.id,
            upstream_station_id=b.upstream_station_id,
            downstream_station_id=b.downstream_station_id,
            capacity=b.capacity,
            current_occupancy=b.current_occupancy,
            fill_ratio=round(b.current_occupancy / max(1, b.capacity), 2),
        )
        for b in snapshot.buffers.values()
    ]

    return LineStateResponse(
        timestamp=snapshot.timestamp.isoformat(),
        horizon_hours=horizon_hours,
        stations=station_schemas,
        buffers=buffer_schemas,
        active_in_flight_units=len(snapshot.in_flight_units),
    )


@router.get("/simulation", response_model=SimulationMetadataResponse)
async def get_simulation_metadata(container: ServiceContainer = Depends(get_service_container)):
    metrics = container.metrics_collector.get_metrics()
    return SimulationMetadataResponse(
        last_fork_timestamp=container.state_store.last_updated_at.isoformat(),
        forecast_horizon_hours=container.settings.forecast_horizon_hours,
        monte_carlo_runs=container.settings.monte_carlo_runs,
        cycles_completed=int(metrics.get("cycles_completed", 0)),
        last_cycle_duration_seconds=metrics.get("last_cycle_duration_seconds", 0.0),
    )


class FaultInjectionRequest(BaseModel):
    station_id: str
    fault_type: str = "drift"  # "drift", "breakdown", "intermittent"
    severity: float = 0.5  # 0.0 to 1.0


@router.post("/inject-fault")
async def inject_fault_scenario(
    req: FaultInjectionRequest,
    container: ServiceContainer = Depends(get_service_container),
):
    """Interactive What-If fault injection endpoint for live twin demonstrations."""
    st = container.state_store.stations.get(req.station_id)
    if not st:
        return {"error": f"Station {req.station_id} not found"}

    now = datetime.now(timezone.utc)
    if req.fault_type == "breakdown":
        st.current_state = StationState.DOWN
        st.last_state_change = now
    elif req.fault_type == "drift":
        # Drift cycle time by +40%
        st.last_cycle_time = st.nominal_cycle_time * (1.0 + 0.40 * req.severity)
        st.current_state = StationState.ACTIVE
    elif req.fault_type == "intermittent":
        st.last_cycle_time = st.nominal_cycle_time * 1.25

    # Run immediate forecast cycle
    raw_preds, alerts, suppressed = container.cycle_runner.run_cycle()

    return {
        "status": "FAULT_INJECTED",
        "station_id": req.station_id,
        "fault_type": req.fault_type,
        "new_state": st.current_state.value,
        "last_cycle_time": st.last_cycle_time,
        "predictions_generated": len(raw_preds),
        "alerts_surfaced": len(alerts),
        "alerts": [
            {
                "id": a.id,
                "station_id": a.station_id,
                "title": a.title,
                "confidence": a.confidence,
                "severity": a.severity.value,
            }
            for a in alerts
        ],
    }


@router.post("/run-cycle")
async def trigger_prediction_cycle(container: ServiceContainer = Depends(get_service_container)):
    """Manually trigger a forward prediction cycle."""
    raw_preds, alerts, suppressed = container.cycle_runner.run_cycle()
    return {
        "predictions_count": len(raw_preds),
        "alerts_count": len(alerts),
        "suppressed_count": len(suppressed),
    }
