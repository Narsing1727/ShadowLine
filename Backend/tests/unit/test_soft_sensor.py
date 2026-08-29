"""Unit tests for soft-sensor virtual metrology."""

import numpy as np
from shadowline.domain.enums import ConfidenceTier
from shadowline.prediction.soft_sensor.coverage_classifier import CoverageClassifier
from shadowline.prediction.soft_sensor.estimator import SoftSensorEstimator
from shadowline.prediction.soft_sensor.features import SoftSensorFeatureExtractor
from shadowline.twin.snapshot import TwinSnapshot


def test_coverage_classifier(sample_snapshot: TwinSnapshot):
    assert CoverageClassifier.classify("S-01", sample_snapshot) == ConfidenceTier.MEASURED
    assert CoverageClassifier.classify("S-03", sample_snapshot) == ConfidenceTier.INFERRED
    assert CoverageClassifier.classify("S-04", sample_snapshot) == ConfidenceTier.DARK


def test_soft_sensor_estimation(sample_snapshot: TwinSnapshot):
    features = SoftSensorFeatureExtractor.extract_features("S-03", sample_snapshot)
    assert len(features) == 6

    estimator = SoftSensorEstimator()
    # Synthetic training with realistic feature baseline
    X = np.tile(features, (20, 1)) + np.random.randn(20, 6) * 0.5
    y = np.full(20, 54.0) + np.random.randn(20) * 1.0
    estimator.fit_station("S-03", X, y)

    est = estimator.estimate("S-03", sample_snapshot)
    assert 40.0 <= est.estimated_cycle_time <= 70.0
    assert est.confidence_interval_low < est.estimated_cycle_time < est.confidence_interval_high
