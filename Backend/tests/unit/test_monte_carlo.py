"""Unit tests for Monte Carlo forward forecasting."""

from shadowline.prediction.bottleneck.monte_carlo import MonteCarloForecaster
from shadowline.twin.snapshot import TwinSnapshot


def test_monte_carlo_forecasting(sample_snapshot: TwinSnapshot):
    forecaster = MonteCarloForecaster(num_runs=10, takt_time=58.0)
    summary = forecaster.run_forecast(sample_snapshot, horizon_hours=0.5)

    assert summary.num_runs == 10
    assert summary.horizon_seconds == 1800.0
    assert len(summary.bottleneck_probabilities) > 0
    # Probabilities sum to 1.0
    total_p = sum(summary.bottleneck_probabilities.values())
    assert 0.99 <= total_p <= 1.01
