"""Discovery API router."""

from fastapi import APIRouter, Depends
from shadowline.api.errors import ResourceNotFoundError
from shadowline.api.schemas.discovery import (
    DiscoverySessionResponse,
    InferredBufferSchema,
    InferredTopologySchema,
    IngestDiscoveryEventsRequest,
    StartDiscoverySessionRequest,
)
from shadowline.discovery.onboarding_session import DiscoveryOnboardingManager, DiscoverySession

router = APIRouter(prefix="/api/discovery", tags=["Discovery"])

# Discovery session manager
_discovery_manager = DiscoveryOnboardingManager()


def _format_discovery_session(s: DiscoverySession) -> DiscoverySessionResponse:
    top_schema = None
    if s.inferred_topology:
        top_schema = InferredTopologySchema(
            station_sequence=s.inferred_topology.station_sequence,
            confidence_score=s.inferred_topology.confidence_score,
            pair_precedence_counts=s.inferred_topology.pair_precedence_counts,
        )

    buf_schemas = [
        InferredBufferSchema(
            upstream_station_id=b.upstream_station_id,
            downstream_station_id=b.downstream_station_id,
            estimated_capacity=b.estimated_capacity,
            median_dwell_seconds=b.median_dwell_seconds,
        )
        for b in s.inferred_buffers
    ]

    return DiscoverySessionResponse(
        session_id=s.session_id,
        line_name=s.line_name,
        status=s.status,
        created_at=s.created_at.isoformat(),
        updated_at=s.updated_at.isoformat(),
        events_ingested=s.events_ingested,
        estimated_takt_time=s.estimated_takt_time,
        inferred_topology=top_schema,
        inferred_buffers=buf_schemas,
    )


@router.post("/session", response_model=DiscoverySessionResponse)
async def start_discovery_session(req: StartDiscoverySessionRequest):
    session = _discovery_manager.create_session(line_name=req.line_name)
    return _format_discovery_session(session)


@router.post("/session/{session_id}/events", response_model=DiscoverySessionResponse)
async def ingest_discovery_events(session_id: str, req: IngestDiscoveryEventsRequest):
    s = _discovery_manager.get_session(session_id)
    if not s:
        raise ResourceNotFoundError("Discovery Session", session_id)
    _discovery_manager.add_events(session_id, req.events)
    return _format_discovery_session(s)


@router.post("/session/{session_id}/run", response_model=DiscoverySessionResponse)
async def run_discovery_inference(session_id: str):
    s = _discovery_manager.run_discovery(session_id)
    if not s:
        raise ResourceNotFoundError("Discovery Session", session_id)
    return _format_discovery_session(s)


@router.get("/session/{session_id}", response_model=DiscoverySessionResponse)
async def get_discovery_session(session_id: str):
    s = _discovery_manager.get_session(session_id)
    if not s:
        raise ResourceNotFoundError("Discovery Session", session_id)
    return _format_discovery_session(s)
