"""Alert API schemas."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class EvidenceItemSchema(BaseModel):
    metric_name: str
    observed_value: Any
    threshold_value: Optional[Any] = None
    unit: Optional[str] = None
    description: str


class ExplanationSchema(BaseModel):
    summary: str
    key_factors: List[str]
    evidence_items: List[EvidenceItemSchema]
    recommended_actions: List[str]


class AlertResponse(BaseModel):
    id: str
    prediction_id: Optional[str]
    station_id: str
    severity: str
    status: str
    confidence: float
    confidence_tier: str
    title: str
    message: str
    created_at: str
    updated_at: str
    acknowledged_at: Optional[str] = None
    acknowledged_by: Optional[str] = None
    snoozed_until: Optional[str] = None
    false_alarm: bool = False
    false_alarm_reason: Optional[str] = None
    explanation: Optional[ExplanationSchema] = None
    recommended_actions: List[str]


class AcknowledgeAlertRequest(BaseModel):
    operator_id: str = "operator_1"


class SnoozeAlertRequest(BaseModel):
    snooze_minutes: float = 30.0


class FalseAlarmAlertRequest(BaseModel):
    reason: str
    operator_id: str = "operator_1"
