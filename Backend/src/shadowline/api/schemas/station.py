"""Station API schemas."""

from typing import List, Optional
from pydantic import BaseModel


class StationDetailResponse(BaseModel):
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


class StationHistoryItem(BaseModel):
    state: str
    cycle_time_seconds: Optional[float]
    vin: Optional[str]
    occurred_at: str


class StationHistoryResponse(BaseModel):
    station_id: str
    history: List[StationHistoryItem]
