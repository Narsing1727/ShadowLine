"""Lag estimator measuring transport time between causing and detecting stations."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np


@dataclass
class LagEstimate:
    causing_station_id: str
    detecting_station_id: str
    defect_code: str
    sample_count: int
    mean_lag_minutes: float
    std_lag_minutes: float


class DefectLagEstimator:
    """Calculates observed travel lag times between stations for specific defect signatures."""

    def __init__(self):
        # Key: (causing_station, detecting_station, defect_code) -> List[lag_minutes]
        self._samples: Dict[Tuple[str, str, str], List[float]] = {}

    def record_lag(self, causing_id: str, detecting_id: str, defect_code: str, lag_minutes: float) -> None:
        key = (causing_id, detecting_id, defect_code)
        if key not in self._samples:
            self._samples[key] = []
        self._samples[key].append(lag_minutes)

    def estimate(self, causing_id: str, detecting_id: str, defect_code: str) -> Optional[LagEstimate]:
        key = (causing_id, detecting_id, defect_code)
        samples = self._samples.get(key, [])
        if not samples:
            return None

        return LagEstimate(
            causing_station_id=causing_id,
            detecting_station_id=detecting_id,
            defect_code=defect_code,
            sample_count=len(samples),
            mean_lag_minutes=round(float(np.mean(samples)), 2),
            std_lag_minutes=round(float(np.std(samples)), 2) if len(samples) > 1 else 0.0,
        )
