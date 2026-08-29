"""Takt time and line cadence estimator."""

from typing import List
import numpy as np


class TaktEstimator:
    """Estimates the line takt time from observed inter-departure times."""

    @staticmethod
    def estimate_takt(exit_timestamps_seconds: List[float]) -> float:
        if len(exit_timestamps_seconds) < 2:
            return 58.0  # Default baseline

        sorted_ts = sorted(exit_timestamps_seconds)
        inter_departures = [sorted_ts[i] - sorted_ts[i - 1] for i in range(1, len(sorted_ts))]
        
        # Remove outlier delays > 300s (e.g. shift breaks or downtime)
        filtered = [d for d in inter_departures if 10.0 <= d <= 300.0]
        if not filtered:
            return 58.0

        # Median is robust against outliers
        return round(float(np.median(filtered)), 1)
