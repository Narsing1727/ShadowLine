"""Station process drift detector."""

from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np


@dataclass
class DriftDetectionResult:
    station_id: str
    is_drifting: bool
    z_score: float
    baseline_mean: float
    current_mean: float
    drift_magnitude_pct: float


class ProcessDriftDetector:
    """Detects statistical process drift in station cycle times or defect rates."""

    def __init__(self, z_score_threshold: float = 2.0, min_samples: int = 10):
        self.z_score_threshold = z_score_threshold
        self.min_samples = min_samples

    def detect_cycle_time_drift(
        self,
        station_id: str,
        cycle_times: List[float],
        nominal_cycle_time: float,
    ) -> DriftDetectionResult:
        if len(cycle_times) < self.min_samples:
            return DriftDetectionResult(
                station_id=station_id,
                is_drifting=False,
                z_score=0.0,
                baseline_mean=nominal_cycle_time,
                current_mean=nominal_cycle_time,
                drift_magnitude_pct=0.0,
            )

        # Compare last 10 samples to nominal baseline
        recent = cycle_times[-10:]
        recent_mean = float(np.mean(recent))
        std = max(1.0, float(np.std(cycle_times)) if len(cycle_times) > 5 else 2.0)

        z = (recent_mean - nominal_cycle_time) / (std / np.sqrt(len(recent)))
        drift_pct = (recent_mean - nominal_cycle_time) / nominal_cycle_time

        is_drifting = z > self.z_score_threshold and drift_pct > 0.08

        return DriftDetectionResult(
            station_id=station_id,
            is_drifting=is_drifting,
            z_score=round(z, 2),
            baseline_mean=round(nominal_cycle_time, 2),
            current_mean=round(recent_mean, 2),
            drift_magnitude_pct=round(drift_pct * 100, 1),
        )
