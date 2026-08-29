"""Serializable twin state snapshot."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from shadowline.domain.enums import ConfidenceTier, StationState, Variant, Zone


@dataclass
class StationSnapshot:
    id: str
    name: str
    zone: str
    confidence_tier: str
    nominal_cycle_time: float
    current_state: str
    current_unit_vin: Optional[str]
    last_cycle_time: Optional[float]
    active_period_seconds: float
    blocked_period_seconds: float
    starved_period_seconds: float
    down_period_seconds: float
    total_units_processed: int


@dataclass
class BufferSnapshot:
    id: str
    upstream_station_id: str
    downstream_station_id: str
    capacity: int
    current_occupancy: int
    queued_vins: List[str]


@dataclass
class UnitSnapshot:
    vin: str
    variant: str
    entered_line_at: str
    current_station_id: Optional[str]
    defect_codes: List[str]


@dataclass
class TwinSnapshot:
    timestamp: datetime
    stations: Dict[str, StationSnapshot]
    buffers: Dict[str, BufferSnapshot]
    in_flight_units: Dict[str, UnitSnapshot]
    metadata: Dict[str, Any] = field(default_factory=dict)
