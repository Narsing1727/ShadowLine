"""Parallel station and path detector."""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass
class ParallelGroup:
    group_name: str
    station_ids: List[str]
    split_ratio: Dict[str, float]


class ParallelPathDetector:
    """Detects stations that process disjoint subsets of VINs in parallel."""

    @staticmethod
    def detect_parallel_stations(unit_exit_events: List[Dict[str, float]]) -> List[ParallelGroup]:
        # Group stations visited by each VIN
        vin_stations: Dict[str, Set[str]] = defaultdict(set)
        station_vins: Dict[str, Set[str]] = defaultdict(set)

        for ev in unit_exit_events:
            vin = ev["vin"]
            st = ev["station_id"]
            vin_stations[vin].add(st)
            station_vins[st].add(vin)

        # Check pairs of stations that never or rarely process the same VIN
        stations = list(station_vins.keys())
        parallel_pairs = []

        for i in range(len(stations)):
            s1 = stations[i]
            vins1 = station_vins[s1]
            for j in range(i + 1, len(stations)):
                s2 = stations[j]
                vins2 = station_vins[s2]

                overlap = vins1.intersection(vins2)
                # If both have significant volume but almost zero overlap
                if len(vins1) >= 10 and len(vins2) >= 10 and len(overlap) / max(len(vins1), len(vins2)) < 0.05:
                    total = len(vins1) + len(vins2)
                    parallel_pairs.append(
                        ParallelGroup(
                            group_name=f"Parallel_{s1}_{s2}",
                            station_ids=[s1, s2],
                            split_ratio={
                                s1: round(len(vins1) / total, 2),
                                s2: round(len(vins2) / total, 2),
                            },
                        )
                    )

        return parallel_pairs
