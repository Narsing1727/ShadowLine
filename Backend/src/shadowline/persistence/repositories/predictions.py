"""Prediction repository."""

import json
from typing import List, Optional
from sqlalchemy.orm import Session
from shadowline.domain.prediction import Prediction
from shadowline.persistence.models import PredictionModel


class PredictionRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, prediction: Prediction) -> None:
        explanation_str = json.dumps(prediction.explanation.__dict__) if prediction.explanation else None
        model = PredictionModel(
            id=prediction.id,
            prediction_type=prediction.prediction_type.value,
            subject_id=prediction.subject_id,
            predicted_at=prediction.predicted_at,
            horizon_hours=prediction.horizon_hours,
            probability=prediction.probability,
            calibrated_probability=prediction.calibrated_probability,
            confidence_tier=prediction.confidence_tier.value,
            expected_impact_time=prediction.expected_impact_time,
            predicted_state=prediction.predicted_state,
            predicted_metric_value=prediction.predicted_metric_value,
            explanation_json=explanation_str,
            metadata_json=json.dumps(prediction.metadata),
            is_scored=prediction.is_scored,
            actual_outcome=prediction.actual_outcome,
            scored_at=prediction.scored_at,
        )
        self.session.merge(model)
        self.session.commit()

    def save_batch(self, predictions: List[Prediction]) -> None:
        for p in predictions:
            explanation_str = json.dumps(p.explanation.__dict__) if p.explanation else None
            model = PredictionModel(
                id=p.id,
                prediction_type=p.prediction_type.value,
                subject_id=p.subject_id,
                predicted_at=p.predicted_at,
                horizon_hours=p.horizon_hours,
                probability=p.probability,
                calibrated_probability=p.calibrated_probability,
                confidence_tier=p.confidence_tier.value,
                expected_impact_time=p.expected_impact_time,
                predicted_state=p.predicted_state,
                predicted_metric_value=p.predicted_metric_value,
                explanation_json=explanation_str,
                metadata_json=json.dumps(p.metadata),
                is_scored=p.is_scored,
                actual_outcome=p.actual_outcome,
                scored_at=p.scored_at,
            )
            self.session.merge(model)
        self.session.commit()

    def list_recent(self, prediction_type: Optional[str] = None, limit: int = 100) -> List[PredictionModel]:
        q = self.session.query(PredictionModel)
        if prediction_type:
            q = q.filter(PredictionModel.prediction_type == prediction_type)
        return q.order_by(PredictionModel.predicted_at.desc()).limit(limit).all()
