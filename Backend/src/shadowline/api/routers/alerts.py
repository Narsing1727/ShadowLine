"""Alert management API router."""

from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import APIRouter, Depends

from shadowline.api.deps import get_service_container
from shadowline.api.errors import ResourceNotFoundError
from shadowline.api.schemas.alert import (
    AcknowledgeAlertRequest,
    AlertResponse,
    EvidenceItemSchema,
    ExplanationSchema,
    FalseAlarmAlertRequest,
    SnoozeAlertRequest,
)
from shadowline.domain.alert import Alert
from shadowline.orchestration.lifecycle import ServiceContainer

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


def _format_alert(a: Alert) -> AlertResponse:
    exp_schema = None
    if a.explanation:
        ev_schemas = [
            EvidenceItemSchema(
                metric_name=e.metric_name,
                observed_value=e.observed_value,
                threshold_value=e.threshold_value,
                unit=e.unit,
                description=e.description,
            )
            for e in a.explanation.evidence_items
        ]
        exp_schema = ExplanationSchema(
            summary=a.explanation.summary,
            key_factors=a.explanation.key_factors,
            evidence_items=ev_schemas,
            recommended_actions=a.explanation.recommended_actions,
        )

    return AlertResponse(
        id=a.id,
        prediction_id=a.prediction_id,
        station_id=a.station_id,
        severity=a.severity.value,
        status=a.status.value,
        confidence=a.confidence,
        confidence_tier=a.confidence_tier.value,
        title=a.title,
        message=a.message,
        created_at=a.created_at.isoformat(),
        updated_at=a.updated_at.isoformat(),
        acknowledged_at=a.acknowledged_at.isoformat() if a.acknowledged_at else None,
        acknowledged_by=a.acknowledged_by,
        snoozed_until=a.snoozed_until.isoformat() if a.snoozed_until else None,
        false_alarm=a.false_alarm,
        false_alarm_reason=a.false_alarm_reason,
        explanation=exp_schema,
        recommended_actions=a.recommended_actions,
    )


@router.get("", response_model=List[AlertResponse])
async def list_active_alerts(container: ServiceContainer = Depends(get_service_container)):
    alerts = container.cycle_runner.active_alerts
    return [_format_alert(a) for a in alerts]


@router.get("/suppressed", response_model=List[dict])
async def list_suppressed_alerts(container: ServiceContainer = Depends(get_service_container)):
    suppressed = container.cycle_runner.suppressed_predictions
    return [
        {
            "id": p.id,
            "subject_id": p.subject_id,
            "prediction_type": p.prediction_type.value,
            "calibrated_probability": p.calibrated_probability,
            "horizon_hours": p.horizon_hours,
            "suppression_reason": "Alarm budget reached or chatter suppression active",
        }
        for p in suppressed
    ]


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: str, container: ServiceContainer = Depends(get_service_container)):
    alert = next((a for a in container.cycle_runner.active_alerts if a.id == alert_id), None)
    if not alert:
        raise ResourceNotFoundError("Alert", alert_id)
    return _format_alert(alert)


@router.post("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge_alert(
    alert_id: str,
    req: AcknowledgeAlertRequest,
    container: ServiceContainer = Depends(get_service_container),
):
    alert = next((a for a in container.cycle_runner.active_alerts if a.id == alert_id), None)
    if not alert:
        raise ResourceNotFoundError("Alert", alert_id)
    alert.acknowledge(operator_id=req.operator_id)
    return _format_alert(alert)


@router.post("/{alert_id}/snooze", response_model=AlertResponse)
async def snooze_alert(
    alert_id: str,
    req: SnoozeAlertRequest,
    container: ServiceContainer = Depends(get_service_container),
):
    alert = next((a for a in container.cycle_runner.active_alerts if a.id == alert_id), None)
    if not alert:
        raise ResourceNotFoundError("Alert", alert_id)
    until = datetime.now(timezone.utc) + timedelta(minutes=req.snooze_minutes)
    alert.snooze(until=until)
    return _format_alert(alert)


@router.post("/{alert_id}/false-alarm", response_model=AlertResponse)
async def mark_false_alarm(
    alert_id: str,
    req: FalseAlarmAlertRequest,
    container: ServiceContainer = Depends(get_service_container),
):
    alert = next((a for a in container.cycle_runner.active_alerts if a.id == alert_id), None)
    if not alert:
        raise ResourceNotFoundError("Alert", alert_id)
    alert.mark_false_alarm(reason=req.reason)
    return _format_alert(alert)
