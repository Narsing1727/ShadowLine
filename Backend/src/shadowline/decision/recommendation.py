"""Operator recommendation generator."""

from typing import List
from shadowline.domain.enums import PredictionType
from shadowline.domain.prediction import Prediction


class RecommendationEngine:
    """Generates non-prescriptive, actionable recommendations for plant operators."""

    @staticmethod
    def generate_recommendations(prediction: Prediction) -> List[str]:
        station_id = prediction.subject_id
        recs = []

        if prediction.prediction_type == PredictionType.BOTTLENECK:
            if prediction.calibrated_probability > 0.70:
                recs.append(f"Prepare buffer upstream of {station_id} for potential accumulation.")
                recs.append(f"Check mechanical/pneumatic feed cycle on {station_id} for micro-stoppages.")
            else:
                recs.append(f"Monitor cycle time trend at {station_id} over the next shift.")

        elif prediction.prediction_type == PredictionType.DEFECT_PROPAGATION:
            recs.append(f"Inspect tooling alignment / calibration at causing station {station_id}.")
            recs.append(f"Perform visual quality check on next 5 units passing {station_id}.")

        elif prediction.prediction_type == PredictionType.SOFT_SENSOR:
            recs.append(f"Verify manual work cadence or sensor connectivity near {station_id}.")

        return recs
