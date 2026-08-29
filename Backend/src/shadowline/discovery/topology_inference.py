"""Topology and station order inference from exit timestamps."""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class InferredTopology:
    station_sequence: List[str]
    confidence_score: float
    pair_precedence_counts: Dict[str, int]


class TopologyInferenceEngine:
    """Infers the physical station order down the assembly line from unit exit events."""

    @staticmethod
    def infer_sequence(unit_exit_events: List[Dict[str, float]]) -> InferredTopology:
        """Takes a list of dicts with keys: {'vin': str, 'station_id': str, 'timestamp': float}."""
        # 1. Group by VIN
        vin_events: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        for ev in unit_exit_events:
            vin_events[ev["vin"]].append((ev["station_id"], ev["timestamp"]))

        # 2. Count pairwise precedence: how often did station A precede station B for the same VIN?
        pair_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        all_stations = set()

        for vin, events in vin_events.items():
            # Sort this VIN's events by timestamp
            sorted_ev = sorted(events, key=lambda x: x[1])
            for i in range(len(sorted_ev)):
                s_i = sorted_ev[i][0]
                all_stations.add(s_i)
                for j in range(i + 1, len(sorted_ev)):
                    s_j = sorted_ev[j][0]
                    if s_i != s_j:
                        pair_counts[(s_i, s_j)] += 1

        if not all_stations:
            return InferredTopology([], 0.0, {})

        # 3. Score each station by the net number of stations it systematically precedes
        precedence_score: Dict[str, int] = {s: 0 for s in all_stations}
        for (a, b), count in pair_counts.items():
            reverse_count = pair_counts.get((b, a), 0)
            if count > reverse_count:
                precedence_score[a] += 1
                precedence_score[b] -= 1

        # Sort stations descending by precedence score
        ordered = sorted(all_stations, key=lambda s: precedence_score[s], reverse=True)

        # Confidence: proportion of pairwise observations conforming to inferred order
        total_pairs = sum(pair_counts.values())
        consistent_pairs = 0
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                consistent_pairs += pair_counts.get((ordered[i], ordered[j]), 0)

        conf = (consistent_pairs / total_pairs) if total_pairs > 0 else 1.0

        pair_dict = {f"{k[0]}->{k[1]}": v for k, v in pair_counts.items()}

        return InferredTopology(
            station_sequence=ordered,
            confidence_score=round(conf, 3),
            pair_precedence_counts=pair_dict,
        )
