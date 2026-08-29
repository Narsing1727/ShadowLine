"""Coverage API schemas."""

from typing import Dict, List
from pydantic import BaseModel


class StationCoverageItem(BaseModel):
    station_id: str
    station_name: str
    zone: str
    confidence_tier: str


class LineCoverageResponse(BaseModel):
    total_stations: int
    measured_count: int
    inferred_count: int
    dark_count: int
    coverage_percentage: float
    stations: List[StationCoverageItem]
