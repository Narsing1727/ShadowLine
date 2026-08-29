"""Explanation builder for decision layer."""

from typing import List, Optional
from shadowline.domain.evidence import EvidenceItem, Explanation
from shadowline.domain.prediction import Prediction


class ExplanationBuilder:
    """Constructs structured evidence and operator explanations from Predictions."""

    @staticmethod
    def build_from_prediction(prediction: Prediction, additional_notes: Optional[List[str]] = None) -> Explanation:
        if prediction.explanation:
            exp = prediction.explanation
            if additional_notes:
                exp.key_factors.extend(additional_notes)
            return exp

        # Fallback default
        return Explanation(
            summary=f"Prediction on {prediction.subject_id} with calibrated confidence {prediction.calibrated_probability * 100:.1f}%.",
            key_factors=additional_notes or [f"Prediction Type: {prediction.prediction_type.value}"],
            evidence_items=[],
            recommended_actions=["Monitor station throughput and buffer queues."],
        )
