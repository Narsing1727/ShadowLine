"""Defect containment calculation for affected downstream units."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from shadowline.domain.unit import Unit
from shadowline.twin.snapshot import TwinSnapshot


@dataclass
class ContainmentReport:
    suspected_causing_station_id: str
    defect_code: str
    affected_vins: List[str]
    total_units_at_risk: int
    current_locations: Dict[str, str]
    recommended_quarantine_station_id: Optional[str]


class DefectContainmentEngine:
    """Calculates downstream quarantine list of VINs that passed a faulted station."""

    @staticmethod
    def identify_containment(
        causing_station_id: str,
        defect_code: str,
        snapshot: TwinSnapshot,
        fault_start_time: Optional[datetime] = None,
        station_sequence: Optional[List[str]] = None,
    ) -> ContainmentReport:
        affected_vins = []
        locations = {}

        seq = station_sequence or list(snapshot.stations.keys())
        if causing_station_id not in seq:
            return ContainmentReport(
                suspected_causing_station_id=causing_station_id,
                defect_code=defect_code,
                affected_vins=[],
                total_units_at_risk=0,
                current_locations={},
                recommended_quarantine_station_id=None,
            )

        cause_idx = seq.index(causing_station_id)
        downstream_stations = set(seq[cause_idx:])

        for vin, u_snap in snapshot.in_flight_units.items():
            # If unit is currently at or downstream of the causing station
            curr_loc = u_snap.current_station_id
            if curr_loc and curr_loc in downstream_stations:
                affected_vins.append(vin)
                locations[vin] = curr_loc

        # Recommend quarantine at end of current zone or final station
        quarantine_station = seq[-1]

        return ContainmentReport(
            suspected_causing_station_id=causing_station_id,
            defect_code=defect_code,
            affected_vins=affected_vins,
            total_units_at_risk=len(affected_vins),
            current_locations=locations,
            recommended_quarantine_station_id=quarantine_station,
        )
