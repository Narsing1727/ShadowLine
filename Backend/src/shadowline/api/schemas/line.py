"""Line API schemas."""

from typing import Dict, List, Optional
from pydantic import BaseModel


class LineMetadataResponse(BaseModel):
    line_id: str
    name: str
    takt_time_seconds: float
    target_jph: float
    shifts_per_day: int
    hours_per_shift: float
    mode: str
    total_stations: int
    total_buffers: int


class BufferStateSchema(BaseModel):
    id: str
    upstream_station_id: str
    downstream_station_id: str
    capacity: int
    current_occupancy: int
    fill_ratio: float


class StationStateSummarySchema(BaseModel):
    id: str
    name: str
    zone: str
    confidence_tier: str
    current_state: str
    nominal_cycle_time: float
    last_cycle_time: Optional[float]
    current_unit_vin: Optional[str]


class LineStateResponse(BaseModel):
    timestamp: str
    horizon_hours: float
    stations: List[StationStateSummarySchema]
    buffers: List[BufferStateSchema]
    active_in_flight_units: int


class SimulationMetadataResponse(BaseModel):
    last_fork_timestamp: Optional[str]
    forecast_horizon_hours: float
    monte_carlo_runs: int
    cycles_completed: int
    last_cycle_duration_seconds: float
