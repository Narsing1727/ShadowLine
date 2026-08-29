"""Prediction domain entity."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from shadowline.domain.enums import ConfidenceTier, PredictionType
from shadowline.domain.evidence import Explanation


@dataclass
class Prediction:
    id: str
    prediction_type: PredictionType
    subject_id: str
    predicted_at: datetime
    horizon_hours: float
    probability: float
    calibrated_probability: float
    confidence_tier: ConfidenceTier = ConfidenceTier.MEASURED
    expected_impact_time: Optional[datetime] = None
    predicted_state: Optional[str] = None
    predicted_metric_value: Optional[float] = None
    explanation: Optional[Explanation] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    is_scored: bool = False
    actual_outcome: Optional[bool] = None
    scored_at: Optional[datetime] = None

    @classmethod
    def create(
        cls,
        prediction_type: PredictionType,
        subject_id: str,
        horizon_hours: float,
        probability: float,
        calibrated_probability: float,
        confidence_tier: ConfidenceTier = ConfidenceTier.MEASURED,
        expected_impact_time: Optional[datetime] = None,
        predicted_state: Optional[str] = None,
        predicted_metric_value: Optional[float] = None,
        explanation: Optional[Explanation] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Prediction":
        return cls(
            id=str(uuid.uuid4()),
            prediction_type=prediction_type,
            subject_id=subject_id,
            predicted_at=datetime.now(timezone.utc),
            horizon_hours=horizon_hours,
            probability=probability,
            calibrated_probability=calibrated_probability,
            confidence_tier=confidence_tier,
            expected_impact_time=expected_impact_time,
            predicted_state=predicted_state,
            predicted_metric_value=predicted_metric_value,
            explanation=explanation,
            metadata=metadata or {},
        )
