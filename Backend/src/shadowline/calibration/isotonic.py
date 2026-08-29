"""Isotonic regression probability calibrator."""

import numpy as np
from sklearn.isotonic import IsotonicRegression
from shadowline.calibration.port import ProbabilityCalibrator


class IsotonicCalibrator(ProbabilityCalibrator):
    """Calibrates probabilities via non-parametric monotonic isotonic regression."""

    def __init__(self):
        self.regressor = IsotonicRegression(out_of_bounds="clip", y_min=0.0, y_max=1.0)
        self.is_fitted = False

    def fit(self, raw_probs: np.ndarray, actual_outcomes: np.ndarray) -> None:
        if len(raw_probs) < 5:
            return
        self.regressor.fit(raw_probs, actual_outcomes)
        self.is_fitted = True

    def calibrate(self, raw_prob: float) -> float:
        if not self.is_fitted:
            # Identity fallback with slight conservative shrinkage towards prior (0.5)
            return float(np.clip(raw_prob * 0.95 + 0.025, 0.0, 1.0))
        res = self.regressor.predict(np.array([raw_prob]))
        return float(np.clip(res[0], 0.0, 1.0))
