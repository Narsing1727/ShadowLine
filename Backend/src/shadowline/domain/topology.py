"""Topology and line structure domain entity."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from shadowline.domain.buffer import Buffer
from shadowline.domain.station import Station
from shadowline.domain.zone import ZoneInfo


@dataclass
class Topology:
    line_id: str
    name: str
    takt_time_seconds: float
    target_jph: float
    shifts_per_day: int
    hours_per_shift: float
    zones: Dict[str, ZoneInfo] = field(default_factory=dict)
    stations: Dict[str, Station] = field(default_factory=dict)
    buffers: Dict[str, Buffer] = field(default_factory=dict)
    station_sequence: List[str] = field(default_factory=list)
    parallel_groups: Dict[str, List[str]] = field(default_factory=dict)

    def get_upstream_station_id(self, station_id: str) -> Optional[str]:
        if station_id not in self.station_sequence:
            return None
        idx = self.station_sequence.index(station_id)
        return self.station_sequence[idx - 1] if idx > 0 else None

    def get_downstream_station_id(self, station_id: str) -> Optional[str]:
        if station_id not in self.station_sequence:
            return None
        idx = self.station_sequence.index(station_id)
        return self.station_sequence[idx + 1] if idx < len(self.station_sequence) - 1 else None

    def get_buffer_between(self, upstream_id: str, downstream_id: str) -> Optional[Buffer]:
        for buf in self.buffers.values():
            if buf.upstream_station_id == upstream_id and buf.downstream_station_id == downstream_id:
                return buf
        return None
