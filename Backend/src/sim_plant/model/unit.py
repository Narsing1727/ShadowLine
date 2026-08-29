"""Physical unit moving down the simulated line."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
import uuid


@dataclass
class SimUnit:
    vin: str
    variant: str
    created_at_sim: float
    history: List[Dict[str, float]] = field(default_factory=list)
    defects: List[Dict[str, str]] = field(default_factory=list)

    @classmethod
    def create(cls, variant: str, now_sim: float, index: int) -> "SimUnit":
        vin = f"VIN-2026-{variant[:3]}-{index:06d}"
        return cls(vin=vin, variant=variant, created_at_sim=now_sim)

    def record_station_entry(self, station_id: str, entered_at_sim: float) -> None:
        self.history.append({"station_id": station_id, "entered_at": entered_at_sim, "exited_at": None})

    def record_station_exit(self, station_id: str, exited_at_sim: float) -> None:
        for entry in reversed(self.history):
            if entry["station_id"] == station_id and entry["exited_at"] is None:
                entry["exited_at"] = exited_at_sim
                entry["dwell"] = exited_at_sim - entry["entered_at"]
                break

    def inject_defect(self, defect_code: str, station_id: str) -> None:
        self.defects.append({"defect_code": defect_code, "causing_station_id": station_id})
