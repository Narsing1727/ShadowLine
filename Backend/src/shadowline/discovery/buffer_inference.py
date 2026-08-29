"""Buffer location and capacity inference."""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np


@dataclass
class InferredBuffer:
    upstream_station_id: str
    downstream_station_id: str
    estimated_capacity: int
    median_dwell_seconds: float
    max_observed_queue: int


class BufferInferenceEngine:
    """Infers buffer locations and capacities between inferred stations."""

    @staticmethod
    def infer_buffers(
        station_sequence: List[str],
        unit_exit_events: List[Dict[str, float]],
        nominal_cycle_time: float = 55.0,
    ) -> List[InferredBuffer]:
        if len(station_sequence) < 2:
            return []

        # Map: VIN -> {station_id: exit_timestamp}
        vin_exits: Dict[str, Dict[str, float]] = defaultdict(dict)
        for ev in unit_exit_events:
            vin_exits[ev["vin"]][ev["station_id"]] = ev["timestamp"]

        inferred = []
        for i in range(len(station_sequence) - 1):
            s_up = station_sequence[i]
            s_down = station_sequence[i + 1]

            deltas = []
            for vin, exits in vin_exits.items():
                if s_up in exits and s_down in exits:
                    dt = exits[s_down] - exits[s_up]
                    if dt > 0:
                        deltas.append(dt)

            if deltas:
                median_dt = float(np.median(deltas))
                # Capacity is roughly median transport/queue time divided by nominal cycle time
                est_cap = max(1, int(round(median_dt / max(10.0, nominal_cycle_time))))
                est_cap = min(15, est_cap)  # Reasonable industrial bound
            else:
                median_dt = nominal_cycle_time
                est_cap = 3

            inferred.append(
                InferredBuffer(
                    upstream_station_id=s_up,
                    downstream_station_id=s_down,
                    estimated_capacity=est_cap,
                    median_dwell_seconds=round(median_dt, 1),
                    max_observed_queue=est_cap + 1,
                )
            )

        return inferred
