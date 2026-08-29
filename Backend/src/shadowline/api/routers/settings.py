"""Settings and mode transition API router."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from shadowline.api.deps import get_service_container
from shadowline.api.errors import InvalidModeTransitionError
from shadowline.domain.enums import Mode
from shadowline.orchestration.lifecycle import ServiceContainer
from shadowline.trust.scorecard import ScorecardCalculator

router = APIRouter(prefix="/api/settings", tags=["Settings"])


class SettingsResponse(BaseModel):
    mode: str
    alarm_budget_per_operator_per_hour: int
    fork_interval_seconds: int
    forecast_horizon_hours: float
    monte_carlo_runs: int
    is_promotion_gate_passed: bool


class UpdateSettingsRequest(BaseModel):
    mode: str | None = None
    alarm_budget_per_operator_per_hour: int | None = None
    fork_interval_seconds: int | None = None
    force_promote: bool = False


@router.get("", response_model=SettingsResponse)
async def get_settings(container: ServiceContainer = Depends(get_service_container)):
    all_preds = container.shadow_log.all_predictions()
    sc = ScorecardCalculator.calculate(all_preds)
    gate = container.promotion_gate.evaluate(sc, current_mode=container.mode_manager.current_mode.value)

    return SettingsResponse(
        mode=container.mode_manager.current_mode.value,
        alarm_budget_per_operator_per_hour=container.alarm_budget.max_alerts_per_hour,
        fork_interval_seconds=container.settings.fork_interval_seconds,
        forecast_horizon_hours=container.settings.forecast_horizon_hours,
        monte_carlo_runs=container.settings.monte_carlo_runs,
        is_promotion_gate_passed=gate.is_eligible_for_live,
    )


@router.put("", response_model=SettingsResponse)
async def update_settings(
    req: UpdateSettingsRequest,
    container: ServiceContainer = Depends(get_service_container),
):
    if req.mode is not None:
        target_mode_str = req.mode.upper()
        if target_mode_str == "LIVE":
            all_preds = container.shadow_log.all_predictions()
            sc = ScorecardCalculator.calculate(all_preds)
            gate = container.promotion_gate.evaluate(sc, current_mode=container.mode_manager.current_mode.value)
            if not gate.is_eligible_for_live and not req.force_promote:
                raise InvalidModeTransitionError("; ".join(gate.reasons))
            container.mode_manager.set_mode(Mode.LIVE)
        elif target_mode_str == "SHADOW":
            container.mode_manager.set_mode(Mode.SHADOW)

    if req.alarm_budget_per_operator_per_hour is not None:
        container.alarm_budget.max_alerts_per_hour = req.alarm_budget_per_operator_per_hour

    if req.fork_interval_seconds is not None:
        container.settings.fork_interval_seconds = req.fork_interval_seconds
        container.scheduler.interval_seconds = req.fork_interval_seconds

    return await get_settings(container)
