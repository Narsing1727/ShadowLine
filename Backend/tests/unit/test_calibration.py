"""Unit tests for calibration and reliability curves."""

import numpy as np
from shadowline.calibration.conformal import ConformalCalibrator
from shadowline.calibration.isotonic import IsotonicCalibrator
from shadowline.calibration.reliability import ReliabilityCalculator


def test_isotonic_calibration():
    calibrator = IsotonicCalibrator()
    # Uncalibrated probabilities and true outcomes
    raw_probs = np.array([0.1, 0.2, 0.35, 0.6, 0.8, 0.85, 0.9, 0.95])
    outcomes = np.array([0, 0, 0, 1, 1, 1, 1, 1])

    calibrator.fit(raw_probs, outcomes)
    calibrated = calibrator.calibrate(0.85)

    assert 0.0 <= calibrated <= 1.0
    assert calibrated >= 0.80


def test_conformal_calibration():
    conformal = ConformalCalibrator(significance_level=0.10)
    raw_probs = np.array([0.1, 0.2, 0.4, 0.7, 0.8, 0.9])
    outcomes = np.array([0, 0, 0, 1, 1, 1])

    conformal.fit(raw_probs, outcomes)
    calibrated = conformal.calibrate(0.75)
    assert 0.0 <= calibrated <= 1.0


def test_reliability_calculator():
    probs = [0.1, 0.2, 0.8, 0.9]
    outcomes = [0, 0, 1, 1]

    rel = ReliabilityCalculator.calculate(probs, outcomes, num_bins=2)
    assert rel.brier_score < 0.10
    assert len(rel.bin_centers) == 2
