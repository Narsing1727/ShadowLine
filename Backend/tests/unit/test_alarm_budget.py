"""Unit tests for Alarm Budgeting and Chatter Suppression."""

from datetime import datetime, timedelta, timezone
from shadowline.decision.alarm_budget import AlarmBudgetManager
from shadowline.decision.suppression import AlertSuppressionEngine


def test_alarm_budget_manager():
    mgr = AlarmBudgetManager(max_alerts_per_hour=3, window_minutes=60.0)
    now = datetime.now(timezone.utc)

    assert mgr.can_surface_alert(now) is True
    assert mgr.remaining_budget(now) == 3

    mgr.record_surfaced_alert(now)
    mgr.record_surfaced_alert(now + timedelta(minutes=5))
    mgr.record_surfaced_alert(now + timedelta(minutes=10))

    assert mgr.current_usage(now + timedelta(minutes=11)) == 3
    assert mgr.can_surface_alert(now + timedelta(minutes=11)) is False
    assert mgr.remaining_budget(now + timedelta(minutes=11)) == 0

    # After 65 minutes, the first alert drops out of rolling window
    t_later = now + timedelta(minutes=65)
    assert mgr.can_surface_alert(t_later) is True
    assert mgr.current_usage(t_later) == 2


def test_chatter_suppression():
    suppression = AlertSuppressionEngine(cooldown_seconds=300.0)
    now = datetime.now(timezone.utc)

    assert suppression.is_suppressed("S-14", "BOTTLENECK", now=now) is False
    suppression.record_alert("S-14", "BOTTLENECK", now=now)

    # 1 minute later -> suppressed
    assert suppression.is_suppressed("S-14", "BOTTLENECK", now=now + timedelta(seconds=60)) is True

    # Different station -> not suppressed
    assert suppression.is_suppressed("S-20", "BOTTLENECK", now=now + timedelta(seconds=60)) is False

    # After cooldown (350s) -> not suppressed
    assert suppression.is_suppressed("S-14", "BOTTLENECK", now=now + timedelta(seconds=350)) is False
