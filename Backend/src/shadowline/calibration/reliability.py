"""Reliability curve and calibration metric calculations."""

from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass
class ReliabilityCurveData:
    bin_centers: List[float]
    empirical_frequencies: List[float]
    bin_counts: List[int]
    brier_score: float
    expected_calibration_error: float


class ReliabilityCalculator:
    """Calculates binned calibration curves, Brier score, and Expected Calibration Error (ECE)."""

    @staticmethod
    def calculate(
        probabilities: List[float],
        outcomes: List[int],
        num_bins: int = 5,
    ) -> ReliabilityCurveData:
        if not probabilities or not outcomes or len(probabilities) != len(outcomes):
            return ReliabilityCurveData([], [], [], 0.0, 0.0)

        p = np.array(probabilities)
        y = np.array(outcomes)

        # Brier score = mean((p - y)^2)
        brier = float(np.mean((p - y) ** 2))

        bins = np.linspace(0.0, 1.0, num_bins + 1)
        bin_centers = []
        frequencies = []
        counts = []
        ece = 0.0
        n_total = len(p)

        for i in range(num_bins):
            low, high = bins[i], bins[i + 1]
            if i == num_bins - 1:
                mask = (p >= low) & (p <= high)
            else:
                mask = (p >= low) & (p < high)

            count = int(np.sum(mask))
            counts.append(count)
            center = float((low + high) / 2.0)
            bin_centers.append(round(center, 2))

            if count > 0:
                freq = float(np.mean(y[mask]))
                frequencies.append(round(freq, 3))
                mean_pred = float(np.mean(p[mask]))
                ece += (count / n_total) * abs(freq - mean_pred)
            else:
                frequencies.append(0.0)

        return ReliabilityCurveData(
            bin_centers=bin_centers,
            empirical_frequencies=frequencies,
            bin_counts=counts,
            brier_score=round(brier, 4),
            expected_calibration_error=round(float(ece), 4),
        )
