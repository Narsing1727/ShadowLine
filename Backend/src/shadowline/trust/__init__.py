"""Trust and governance layer package."""

from shadowline.trust.operator_feedback import FeedbackEntry, OperatorFeedbackTracker
from shadowline.trust.outcome_matcher import OutcomeMatcher
from shadowline.trust.promotion_gate import PromotionGate, PromotionGateResult
from shadowline.trust.scorecard import ScorecardCalculator, TrustScorecard
from shadowline.trust.shadow_log import ShadowLog

__all__ = [
    "FeedbackEntry",
    "OperatorFeedbackTracker",
    "OutcomeMatcher",
    "PromotionGate",
    "PromotionGateResult",
    "ScorecardCalculator",
    "ShadowLog",
    "TrustScorecard",
]
