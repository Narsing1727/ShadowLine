"""Zone domain entity and aggregates."""

from dataclasses import dataclass, field
from typing import List

from shadowline.domain.enums import Zone


@dataclass
class ZoneInfo:
    id: Zone
    name: str
    description: str = ""
    station_ids: List[str] = field(default_factory=list)
