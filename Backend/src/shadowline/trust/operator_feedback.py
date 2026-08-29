"""Operator feedback tracking for trust calibration."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass
class FeedbackEntry:
    alert_id: str
    action: str  # ACKNOWLEDGE, SNOOZE, FALSE_ALARM
    operator_id: str
    timestamp: datetime
    reason: Optional[str] = None


class OperatorFeedbackTracker:
    """Records operator actions and false-alarm marks to feed back into model scoring."""

    def __init__(self):
        self._entries: List[FeedbackEntry] = []

    def record_feedback(
        self,
        alert_id: str,
        action: str,
        operator_id: str = "operator_1",
        reason: Optional[str] = None,
        now: Optional[datetime] = None,
    ) -> FeedbackEntry:
        entry = FeedbackEntry(
            alert_id=alert_id,
            action=action,
            operator_id=operator_id,
            timestamp=now or datetime.now(timezone.utc),
            reason=reason,
        )
        self._entries.append(entry)
        return entry

    def get_false_alarm_count(self) -> int:
        return sum(1 for e in self._entries if e.action == "FALSE_ALARM")

    def all_entries(self) -> List[FeedbackEntry]:
        return list(self._entries)
