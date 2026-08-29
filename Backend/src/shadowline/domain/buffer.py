"""Buffer domain entity."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Buffer:
    id: str
    upstream_station_id: str
    downstream_station_id: str
    capacity: int
    current_occupancy: int = 0
    queued_vins: List[str] = field(default_factory=list)

    @property
    def is_full(self) -> bool:
        return self.current_occupancy >= self.capacity

    @property
    def is_empty(self) -> bool:
        return self.current_occupancy == 0

    @property
    def fill_ratio(self) -> float:
        if self.capacity <= 0:
            return 0.0
        return min(1.0, self.current_occupancy / float(self.capacity))
