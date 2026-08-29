"""Unit domain entity."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from shadowline.domain.enums import Variant


@dataclass
class Unit:
    vin: str
    variant: Variant
    entered_line_at: datetime
    current_station_id: Optional[str] = None
    exited_line_at: Optional[datetime] = None
    is_completed: bool = False
    defect_codes: List[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
