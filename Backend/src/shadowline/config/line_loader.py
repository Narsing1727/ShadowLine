"""Line YAML configuration loader."""

from pathlib import Path
from typing import Any, Dict
import yaml

from shadowline.domain.buffer import Buffer
from shadowline.domain.enums import ConfidenceTier, Zone
from shadowline.domain.station import Station
from shadowline.domain.topology import Topology
from shadowline.domain.zone import ZoneInfo


class LineLoader:
    """Loads and validates a line's YAML configuration into a domain Topology entity."""

    @staticmethod
    def load_from_yaml(file_path: str) -> Topology:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Line config file not found: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f) or {}

        line_id = data.get("line_id", "default_line")
        name = data.get("name", "Assembly Line")
        takt = float(data.get("takt_time_seconds", 58.0))
        target_jph = float(data.get("target_jph", 62.0))
        shifts = int(data.get("shifts_per_day", 2))
        hours_shift = float(data.get("hours_per_shift", 8.0))

        # Zones
        zones = {}
        for z in data.get("zones", []):
            z_id_str = z["id"]
            z_enum = Zone(z_id_str) if z_id_str in Zone.__members__ else Zone.FINAL_ASSEMBLY
            zones[z_id_str] = ZoneInfo(
                id=z_enum,
                name=z.get("name", z_id_str),
                description=z.get("description", ""),
            )

        # Stations
        stations = {}
        station_sequence = []
        for s in data.get("stations", []):
            s_id = s["id"]
            station_sequence.append(s_id)
            z_str = s["zone"]
            z_enum = Zone(z_str) if z_str in Zone.__members__ else Zone.FINAL_ASSEMBLY

            tier_str = s.get("confidence_tier", "MEASURED")
            tier_enum = ConfidenceTier(tier_str) if tier_str in ConfidenceTier.__members__ else ConfidenceTier.MEASURED

            station = Station(
                id=s_id,
                name=s.get("name", s_id),
                zone=z_enum,
                confidence_tier=tier_enum,
                nominal_cycle_time=float(s.get("nominal_cycle_time", 55.0)),
            )
            stations[s_id] = station
            if z_str in zones:
                zones[z_str].station_ids.append(s_id)

        # Buffers
        buffers = {}
        for b in data.get("buffers", []):
            b_id = b["id"]
            buffers[b_id] = Buffer(
                id=b_id,
                upstream_station_id=b["upstream_station_id"],
                downstream_station_id=b["downstream_station_id"],
                capacity=int(b.get("capacity", 3)),
            )

        return Topology(
            line_id=line_id,
            name=name,
            takt_time_seconds=takt,
            target_jph=target_jph,
            shifts_per_day=shifts,
            hours_per_shift=hours_shift,
            zones=zones,
            stations=stations,
            buffers=buffers,
            station_sequence=station_sequence,
        )
