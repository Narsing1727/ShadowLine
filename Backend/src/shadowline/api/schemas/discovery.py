"""Discovery API schemas."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class StartDiscoverySessionRequest(BaseModel):
    line_name: str


class IngestDiscoveryEventsRequest(BaseModel):
    events: List[Dict[str, Any]]


class InferredBufferSchema(BaseModel):
    upstream_station_id: str
    downstream_station_id: str
    estimated_capacity: int
    median_dwell_seconds: float


class InferredTopologySchema(BaseModel):
    station_sequence: List[str]
    confidence_score: float
    pair_precedence_counts: Dict[str, int]


class DiscoverySessionResponse(BaseModel):
    session_id: str
    line_name: str
    status: str
    created_at: str
    updated_at: str
    events_ingested: int
    estimated_takt_time: float
    inferred_topology: Optional[InferredTopologySchema]
    inferred_buffers: List[InferredBufferSchema]
