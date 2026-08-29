"""On-demand prediction scoring script."""

from shadowline.config.settings import ShadowLineSettings
from shadowline.orchestration.lifecycle import ServiceContainer
from shadowline.trust.scorecard import ScorecardCalculator


def score_predictions():
    container = ServiceContainer()
    all_preds = container.shadow_log.all_predictions()
    scorecard = ScorecardCalculator.calculate(all_preds)
    gate = container.promotion_gate.evaluate(scorecard, current_mode=container.mode_manager.current_mode.value)

    print("\n================== SHADOWLINE TRUST SCORECARD ==================")
    print(f"Total Predictions:    {scorecard.total_predictions}")
    print(f"Scored Predictions:   {scorecard.scored_predictions}")
    print(f"Precision:            {scorecard.precision * 100:.1f}%")
    print(f"Recall:               {scorecard.recall * 100:.1f}%")
    print(f"False Alarm Rate:     {scorecard.false_alarm_rate * 100:.1f}%")
    print(f"Mean Lead Time:       {scorecard.mean_lead_time_minutes:.1f} minutes")
    print(f"Brier Score:          {scorecard.reliability_data.brier_score:.4f}")
    print(f"ECE (Expected Error): {scorecard.reliability_data.expected_calibration_error:.4f}")
    print("----------------------------------------------------------------")
    print(f"Promotion Gate Status: {'CERTIFIED FOR LIVE' if gate.is_eligible_for_live else 'REMAINS IN SHADOW'}")
    for reason in gate.reasons:
        print(f" - {reason}")
    print("================================================================\n")


if __name__ == "__main__":
    score_predictions()
