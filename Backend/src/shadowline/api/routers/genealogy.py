"""Genealogy API router."""

from fastapi import APIRouter, Depends
from shadowline.api.deps import get_service_container
from shadowline.api.errors import ResourceNotFoundError
from shadowline.api.schemas.genealogy import GenealogyResponse, GenealogyStepSchema
from shadowline.orchestration.lifecycle import ServiceContainer

router = APIRouter(prefix="/api/genealogy", tags=["Genealogy"])


@router.get("/{vin}", response_model=GenealogyResponse)
async def get_unit_genealogy(vin: str, container: ServiceContainer = Depends(get_service_container)):
    rec = container.state_store.genealogy_tracker.get_genealogy(vin)
    if not rec:
        raise ResourceNotFoundError("Genealogy for VIN", vin)

    steps = [
        GenealogyStepSchema(
            station_id=st.station_id,
            station_name=st.station_name,
            entered_at=st.entered_at.isoformat(),
            exited_at=st.exited_at.isoformat() if st.exited_at else None,
            dwell_seconds=st.dwell_seconds,
            defect_codes=st.defect_codes,
        )
        for st in rec.steps
    ]

    return GenealogyResponse(
        vin=rec.vin,
        variant=rec.variant.value if hasattr(rec.variant, "value") else str(rec.variant),
        created_at=rec.created_at.isoformat(),
        steps=steps,
        defects=rec.defects,
    )
