"""Integration test: Full 60s prediction cycle."""

from shadowline.config.settings import ShadowLineSettings
from shadowline.domain.enums import Mode
from shadowline.orchestration.lifecycle import ServiceContainer


def test_full_prediction_cycle():
    settings = ShadowLineSettings(mode="LIVE", db_url="sqlite:///:memory:", monte_carlo_runs=10)
    container = ServiceContainer(settings)

    # 1. Run cycle in LIVE mode
    preds, alerts, suppressed = container.cycle_runner.run_cycle()

    assert len(preds) > 0
    assert container.metrics_collector.get_metrics()["cycles_completed"] == 1

    # In LIVE mode, predictions are budgeted and produced as Alerts
    assert isinstance(alerts, list)

    # 2. Switch to SHADOW mode
    container.mode_manager.set_mode(Mode.SHADOW)
    preds2, alerts2, suppressed2 = container.cycle_runner.run_cycle()

    assert len(preds2) > 0
    # In SHADOW mode, alerts are suppressed (0 surfaced alerts)
    assert len(alerts2) == 0
    assert len(suppressed2) == len(preds2)
