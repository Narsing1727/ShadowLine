"""Station domain entity."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from shadowline.domain.enums import ConfidenceTier, StationState, Zone


@dataclass
class Station:
    id: str
    name: str
    zone: Zone
    confidence_tier: ConfidenceTier
    nominal_cycle_time: float
    current_state: StationState = StationState.IDLE
    current_unit_vin: Optional[str] = None
    last_state_change: Optional[datetime] = None
    last_cycle_time: Optional[float] = None
    active_period_seconds: float = 0.0
    blocked_period_seconds: float = 0.0
    starved_period_seconds: float = 0.0
    down_period_seconds: float = 0.0
    total_units_processed: int = 0
    metadata: dict = field(default_factory=dict)
