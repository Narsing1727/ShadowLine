"""Unit tests for Active Period Method calculation."""

from shadowline.prediction.bottleneck.active_period import ActivePeriodCalculator
from shadowline.twin.snapshot import TwinSnapshot


def test_active_period_bottleneck_detection(sample_snapshot: TwinSnapshot):
    apm_results = ActivePeriodCalculator.calculate(sample_snapshot)

    assert "S-01" in apm_results
    assert "S-02" in apm_results
    assert "S-03" in apm_results
    assert "S-04" in apm_results

    # S-02 has 450s active out of 470s total (~95.7%), should be the identified bottleneck
    assert apm_results["S-02"].is_current_bottleneck is True
    assert apm_results["S-01"].is_current_bottleneck is False
    assert apm_results["S-02"].active_percentage > apm_results["S-01"].active_percentage
