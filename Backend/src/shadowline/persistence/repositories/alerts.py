"""Alert repository."""

from datetime import datetime, timezone
import json
from typing import List, Optional
from sqlalchemy.orm import Session
from shadowline.domain.alert import Alert
from shadowline.persistence.models import AlertModel


class AlertRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, alert: Alert) -> None:
        explanation_str = json.dumps(alert.explanation.__dict__) if alert.explanation else None
        model = AlertModel(
            id=alert.id,
            prediction_id=alert.prediction_id,
            station_id=alert.station_id,
            severity=alert.severity.value,
            status=alert.status.value,
            confidence=alert.confidence,
            confidence_tier=alert.confidence_tier.value,
            title=alert.title,
            message=alert.message,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
            acknowledged_at=alert.acknowledged_at,
            acknowledged_by=alert.acknowledged_by,
            snoozed_until=alert.snoozed_until,
            dismissed_at=alert.dismissed_at,
            false_alarm=alert.false_alarm,
            false_alarm_reason=alert.false_alarm_reason,
            explanation_json=explanation_str,
            recommendations_json=json.dumps(alert.recommended_actions),
            metadata_json=json.dumps(alert.metadata),
        )
        self.session.merge(model)
        self.session.commit()

    def get(self, alert_id: str) -> Optional[AlertModel]:
        return self.session.query(AlertModel).filter(AlertModel.id == alert_id).first()

    def list_active(self) -> List[AlertModel]:
        return (
            self.session.query(AlertModel)
            .filter(AlertModel.status == "ACTIVE")
            .order_by(AlertModel.created_at.desc())
            .all()
        )

    def list_all(self, limit: int = 100) -> List[AlertModel]:
        return self.session.query(AlertModel).order_by(AlertModel.created_at.desc()).limit(limit).all()
