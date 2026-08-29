"""Genealogy record and step domain entities."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from shadowline.domain.enums import Variant


@dataclass
class GenealogyStep:
    station_id: str
    station_name: str
    entered_at: datetime
    exited_at: Optional[datetime] = None
    dwell_seconds: Optional[float] = None
    operator_id: Optional[str] = None
    tool_id: Optional[str] = None
    defect_codes: List[str] = field(default_factory=list)
    measurements: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenealogyRecord:
    vin: str
    variant: Variant
    created_at: datetime
    steps: List[GenealogyStep] = field(default_factory=list)
    defects: List[Dict[str, Any]] = field(default_factory=list)

    def add_step(self, step: GenealogyStep) -> None:
        self.steps.append(step)

    def record_defect(
        self,
        defect_code: str,
        detecting_station_id: str,
        detected_at: datetime,
        suspected_causing_station_id: Optional[str] = None,
    ) -> None:
        self.defects.append(
            {
                "defect_code": defect_code,
                "detecting_station_id": detecting_station_id,
                "detected_at": detected_at.isoformat(),
                "suspected_causing_station_id": suspected_causing_station_id,
            }
        )
