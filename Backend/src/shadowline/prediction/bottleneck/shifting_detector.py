"""Shifting (wandering) bottleneck detector."""

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ShiftingBottleneckInfo:
    is_shifting: bool
    dominant_station_id: Optional[str]
    secondary_station_id: Optional[str]
    shift_frequency_per_hour: float


class ShiftingBottleneckDetector:
    """Detects when the bottleneck shifts dynamically between multiple stations."""

    def __init__(self, window_size: int = 60):
        self.history: deque[str] = deque(maxlen=window_size)

    def record_bottleneck(self, station_id: str) -> None:
        self.history.append(station_id)

    def detect(self) -> ShiftingBottleneckInfo:
        if len(self.history) < 5:
            return ShiftingBottleneckInfo(
                is_shifting=False,
                dominant_station_id=self.history[-1] if self.history else None,
                secondary_station_id=None,
                shift_frequency_per_hour=0.0,
            )

        counts: Dict[str, int] = {}
        for s in self.history:
            counts[s] = counts.get(s, 0) + 1

        sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        dominant = sorted_counts[0][0]
        secondary = sorted_counts[1][0] if len(sorted_counts) > 1 else None

        # Count state switches
        switches = 0
        prev = None
        for s in self.history:
            if prev is not None and s != prev:
                switches += 1
            prev = s

        # Estimate hourly frequency assuming 1 record per minute
        hourly_shifts = switches * (60.0 / max(1, len(self.history)))
        is_shifting = len(sorted_counts) > 1 and (sorted_counts[1][1] / len(self.history)) > 0.25

        return ShiftingBottleneckInfo(
            is_shifting=is_shifting,
            dominant_station_id=dominant,
            secondary_station_id=secondary,
            shift_frequency_per_hour=round(hourly_shifts, 2),
        )
