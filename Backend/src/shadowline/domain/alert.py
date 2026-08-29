"""Alert domain entity."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from shadowline.domain.enums import AlertSeverity, AlertStatus, ConfidenceTier
from shadowline.domain.evidence import Explanation


@dataclass
class Alert:
    id: str
    prediction_id: Optional[str]
    station_id: str
    severity: AlertSeverity
    status: AlertStatus
    confidence: float
    confidence_tier: ConfidenceTier
    title: str
    message: str
    created_at: datetime
    updated_at: datetime
    acknowledged_at: Optional[datetime] = None
    acknowledged_by: Optional[str] = None
    snoozed_until: Optional[datetime] = None
    dismissed_at: Optional[datetime] = None
    false_alarm: bool = False
    false_alarm_reason: Optional[str] = None
    explanation: Optional[Explanation] = None
    recommended_actions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        station_id: str,
        severity: AlertSeverity,
        confidence: float,
        confidence_tier: ConfidenceTier,
        title: str,
        message: str,
        prediction_id: Optional[str] = None,
        explanation: Optional[Explanation] = None,
        recommended_actions: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Alert":
        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid.uuid4()),
            prediction_id=prediction_id,
            station_id=station_id,
            severity=severity,
            status=AlertStatus.ACTIVE,
            confidence=confidence,
            confidence_tier=confidence_tier,
            title=title,
            message=message,
            created_at=now,
            updated_at=now,
            explanation=explanation,
            recommended_actions=recommended_actions or [],
            metadata=metadata or {},
        )

    def acknowledge(self, operator_id: str) -> None:
        self.status = AlertStatus.ACKNOWLEDGED
        self.acknowledged_at = datetime.now(timezone.utc)
        self.acknowledged_by = operator_id
        self.updated_at = datetime.now(timezone.utc)

    def snooze(self, until: datetime) -> None:
        self.status = AlertStatus.SNOOZED
        self.snoozed_until = until
        self.updated_at = datetime.now(timezone.utc)

    def mark_false_alarm(self, reason: Optional[str] = None) -> None:
        self.status = AlertStatus.FALSE_ALARM
        self.false_alarm = True
        self.false_alarm_reason = reason
        self.updated_at = datetime.now(timezone.utc)
