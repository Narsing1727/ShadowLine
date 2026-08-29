"""Chatter and duplicate alert suppression."""

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional


class AlertSuppressionEngine:
    """Suppresses chattering and duplicate alerts for the same condition."""

    def __init__(self, cooldown_seconds: float = 300.0):
        self.cooldown_seconds = cooldown_seconds
        # Key: (station_id, alert_type) -> last_alert_time
        self._last_alert_times: Dict[str, datetime] = {}

    def is_suppressed(self, station_id: str, alert_type: str, now: Optional[datetime] = None) -> bool:
        current_time = now or datetime.now(timezone.utc)
        key = f"{station_id}:{alert_type}"

        if key in self._last_alert_times:
            elapsed = (current_time - self._last_alert_times[key]).total_seconds()
            if elapsed < self.cooldown_seconds:
                return True

        return False

    def record_alert(self, station_id: str, alert_type: str, now: Optional[datetime] = None) -> None:
        key = f"{station_id}:{alert_type}"
        self._last_alert_times[key] = now or datetime.now(timezone.utc)
