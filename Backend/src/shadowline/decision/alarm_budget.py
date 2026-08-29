"""EEMUA 191 Alarm Budget Manager."""

from collections import deque
from datetime import datetime, timedelta, timezone
from typing import List, Optional


class AlarmBudgetManager:
    """Enforces EEMUA 191 alarm limits (e.g. max 6 alerts/operator/hour)."""

    def __init__(self, max_alerts_per_hour: int = 6, window_minutes: float = 60.0):
        self.max_alerts_per_hour = max_alerts_per_hour
        self.window_minutes = window_minutes
        self._surfaced_timestamps: deque[datetime] = deque()

    def can_surface_alert(self, now: Optional[datetime] = None) -> bool:
        current_time = now or datetime.now(timezone.utc)
        self._prune_expired(current_time)
        return len(self._surfaced_timestamps) < self.max_alerts_per_hour

    def record_surfaced_alert(self, now: Optional[datetime] = None) -> None:
        current_time = now or datetime.now(timezone.utc)
        self._prune_expired(current_time)
        self._surfaced_timestamps.append(current_time)

    def current_usage(self, now: Optional[datetime] = None) -> int:
        current_time = now or datetime.now(timezone.utc)
        self._prune_expired(current_time)
        return len(self._surfaced_timestamps)

    def remaining_budget(self, now: Optional[datetime] = None) -> int:
        return max(0, self.max_alerts_per_hour - self.current_usage(now))

    def _prune_expired(self, current_time: datetime) -> None:
        cutoff = current_time - timedelta(minutes=self.window_minutes)
        while self._surfaced_timestamps and self._surfaced_timestamps[0] < cutoff:
            self._surfaced_timestamps.popleft()
