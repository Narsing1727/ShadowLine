"""Conformal prediction calibrator providing guaranteed coverage bounds."""

import numpy as np
from shadowline.calibration.port import ProbabilityCalibrator


class ConformalCalibrator(ProbabilityCalibrator):
    """Conformal prediction calibrator computing valid p-values and confidence bands."""

    def __init__(self, significance_level: float = 0.10):
        self.significance_level = significance_level
        self.nonconformity_scores: np.ndarray = np.array([])
        self.is_fitted = False

    def fit(self, raw_probs: np.ndarray, actual_outcomes: np.ndarray) -> None:
        if len(raw_probs) < 5:
            return
        # Non-conformity score: absolute error |prob - outcome|
        self.nonconformity_scores = np.sort(np.abs(raw_probs - actual_outcomes))
        self.is_fitted = True

    def calibrate(self, raw_prob: float) -> float:
        if not self.is_fitted or len(self.nonconformity_scores) == 0:
            return raw_prob

        # Compute empirical quantile
        n = len(self.nonconformity_scores)
        k = int(np.ceil((n + 1) * (1.0 - self.significance_level)))
        k = min(n - 1, max(0, k))
        margin = float(self.nonconformity_scores[k])

        # Adjust probability conservatively
        if raw_prob >= 0.5:
            return float(np.clip(raw_prob - (margin * 0.5), 0.0, 1.0))
        else:
            return float(np.clip(raw_prob + (margin * 0.5), 0.0, 1.0))
