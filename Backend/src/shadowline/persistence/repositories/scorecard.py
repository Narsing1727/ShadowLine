"""Scorecard repository."""

from sqlalchemy.orm import Session
from shadowline.persistence.models import ScorecardModel
from shadowline.trust.scorecard import TrustScorecard


class ScorecardRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_scorecard(self, scorecard: TrustScorecard, is_live_promoted: bool = False) -> ScorecardModel:
        model = ScorecardModel(
            total_predictions=scorecard.total_predictions,
            scored_predictions=scorecard.scored_predictions,
            true_positives=scorecard.true_positives,
            false_positives=scorecard.false_positives,
            true_negatives=scorecard.true_negatives,
            false_negatives=scorecard.false_negatives,
            precision=scorecard.precision,
            recall=scorecard.recall,
            false_alarm_rate=scorecard.false_alarm_rate,
            mean_lead_time_minutes=scorecard.mean_lead_time_minutes,
            brier_score=scorecard.reliability_data.brier_score,
            is_live_promoted=is_live_promoted,
        )
        self.session.add(model)
        self.session.commit()
        return model

    def get_latest(self) -> ScorecardModel | None:
        return self.session.query(ScorecardModel).order_by(ScorecardModel.recorded_at.desc()).first()
