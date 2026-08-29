"""Genealogy API schemas."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class GenealogyStepSchema(BaseModel):
    station_id: str
    station_name: str
    entered_at: str
    exited_at: Optional[str]
    dwell_seconds: Optional[float]
    defect_codes: List[str]


class GenealogyResponse(BaseModel):
    vin: str
    variant: str
    created_at: str
    steps: List[GenealogyStepSchema]
    defects: List[Dict[str, Any]]
