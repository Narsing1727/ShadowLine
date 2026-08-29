"""Defects and propagation graph API router."""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query

from shadowline.api.deps import get_service_container
from shadowline.orchestration.lifecycle import ServiceContainer
from shadowline.prediction.defect.containment import DefectContainmentEngine
from shadowline.prediction.defect.propagation_graph import DefectPropagationGraph

router = APIRouter(prefix="/api/defects", tags=["Defects"])

# Shared graph instance
_propagation_graph = DefectPropagationGraph()
# Seed known baseline propagation paths
_propagation_graph.add_or_update_edge("S-03", "S-11", "D-WELD-01", lag_minutes=18.0)
_propagation_graph.add_or_update_edge("S-14", "S-23", "D-PAINT-02", lag_minutes=35.0)
_propagation_graph.add_or_update_edge("S-33", "S-42", "D-TORQ-03", lag_minutes=25.0)
_propagation_graph.add_or_update_edge("S-34", "S-42", "D-BAT-05", lag_minutes=22.0)


@router.get("/propagation")
async def get_defect_propagation_graph():
    return _propagation_graph.to_dict()


@router.get("/containment")
async def get_defect_containment(
    causing_station_id: str = Query(..., description="Station suspected of introducing defects"),
    defect_code: str = Query("D-GENERAL", description="Defect code"),
    container: ServiceContainer = Depends(get_service_container),
):
    snapshot = container.state_store.snapshot()
    report = DefectContainmentEngine.identify_containment(
        causing_station_id=causing_station_id,
        defect_code=defect_code,
        snapshot=snapshot,
        station_sequence=container.topology.station_sequence,
    )
    return {
        "suspected_causing_station_id": report.suspected_causing_station_id,
        "defect_code": report.defect_code,
        "total_units_at_risk": report.total_units_at_risk,
        "affected_vins": report.affected_vins,
        "current_locations": report.current_locations,
        "recommended_quarantine_station_id": report.recommended_quarantine_station_id,
    }
