"""Feature extraction for soft-sensor virtual metrology."""

from typing import Dict, List, Optional
import numpy as np
from shadowline.twin.snapshot import TwinSnapshot


class SoftSensorFeatureExtractor:
    """Extracts features for an INFERRED station using neighbouring telemetry."""

    @staticmethod
    def extract_features(
        station_id: str,
        snapshot: TwinSnapshot,
        station_sequence: Optional[List[str]] = None,
    ) -> np.ndarray:
        seq = station_sequence or list(snapshot.stations.keys())
        features = []

        if station_id not in seq:
            return np.zeros(6)

        idx = seq.index(station_id)

        # 1. Upstream buffer fill ratio
        up_buf_fill = 0.5
        for b in snapshot.buffers.values():
            if b.downstream_station_id == station_id:
                up_buf_fill = b.current_occupancy / max(1, b.capacity)
                break
        features.append(up_buf_fill)

        # 2. Downstream buffer fill ratio
        down_buf_fill = 0.5
        for b in snapshot.buffers.values():
            if b.upstream_station_id == station_id:
                down_buf_fill = b.current_occupancy / max(1, b.capacity)
                break
        features.append(down_buf_fill)

        # 3. Upstream station cycle time
        up_s_ct = 55.0
        if idx > 0:
            up_s = snapshot.stations.get(seq[idx - 1])
            if up_s and up_s.last_cycle_time:
                up_s_ct = up_s.last_cycle_time
        features.append(up_s_ct)

        # 4. Downstream station cycle time
        down_s_ct = 55.0
        if idx < len(seq) - 1:
            down_s = snapshot.stations.get(seq[idx + 1])
            if down_s and down_s.last_cycle_time:
                down_s_ct = down_s.last_cycle_time
        features.append(down_s_ct)

        # 5. Station nominal cycle time
        s_snap = snapshot.stations.get(station_id)
        nominal_ct = s_snap.nominal_cycle_time if s_snap else 55.0
        features.append(nominal_ct)

        # 6. Total in-flight units
        features.append(len(snapshot.in_flight_units))

        return np.array(features, dtype=float)
