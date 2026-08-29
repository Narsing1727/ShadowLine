"""Financial and ROI impact API router."""

from fastapi import APIRouter, Depends
from shadowline.api.deps import get_service_container
from shadowline.api.schemas.impact import ImpactAssumptionsSchema, ImpactSummaryResponse, OEESchema
from shadowline.impact.assumptions import CostAssumptions
from shadowline.impact.containment_value import ContainmentValuator
from shadowline.impact.downtime_value import DowntimeValuator
from shadowline.impact.oee import OEECalculator
from shadowline.impact.rework_value import ReworkValuator
from shadowline.orchestration.lifecycle import ServiceContainer

router = APIRouter(prefix="/api/impact", tags=["Impact"])

# Editable instance of cost assumptions
_cost_assumptions = CostAssumptions()


@router.get("", response_model=ImpactSummaryResponse)
async def get_impact_summary(container: ServiceContainer = Depends(get_service_container)):
    snapshot = container.state_store.snapshot()
    oee_res = OEECalculator.calculate(
        snapshot,
        operating_hours=8.0,
        target_jph=container.topology.target_jph,
    )

    total_down_hours = sum(s.down_period_seconds for s in snapshot.stations.values()) / 3600.0
    avoided_hours = total_down_hours * 0.40  # Estimated 40% downtime reduction via proactive alerts

    dt_impact = DowntimeValuator.calculate(
        downtime_hours=total_down_hours,
        avoided_hours=avoided_hours,
        assumptions=_cost_assumptions,
    )

    defect_count = sum(len(u.defect_codes) for u in snapshot.in_flight_units.values())
    prevented_defects = int(defect_count * 0.50)
    rw_impact = ReworkValuator.calculate(
        defects_detected=defect_count,
        defects_prevented=prevented_defects,
        assumptions=_cost_assumptions,
    )

    containment_report = ContainmentValuator.calculate(
        units_quarantined=defect_count,
        assumptions=_cost_assumptions,
    )

    net_savings = dt_impact.avoided_savings_usd + rw_impact.prevented_savings_usd + containment_report.net_containment_benefit_usd

    return ImpactSummaryResponse(
        downtime_loss_usd=dt_impact.monetary_loss_usd,
        avoided_downtime_savings_usd=dt_impact.avoided_savings_usd,
        rework_expense_usd=rw_impact.rework_cost_usd,
        prevented_defect_savings_usd=rw_impact.prevented_savings_usd,
        containment_recall_avoided_usd=containment_report.recall_risk_avoided_usd,
        net_savings_usd=round(net_savings, 2),
        oee=OEESchema(
            availability=oee_res.availability,
            performance=oee_res.performance,
            quality=oee_res.quality,
            oee=oee_res.oee,
            target_jph=oee_res.target_jph,
            actual_jph=oee_res.actual_jph,
        ),
        assumptions=ImpactAssumptionsSchema(
            downtime_cost_per_hour_usd=_cost_assumptions.downtime_cost_per_hour_usd,
            rework_cost_per_defect_usd=_cost_assumptions.rework_cost_per_defect_usd,
            scrap_cost_per_unit_usd=_cost_assumptions.scrap_cost_per_unit_usd,
            field_recall_cost_per_unit_usd=_cost_assumptions.field_recall_cost_per_unit_usd,
            operator_hourly_rate_usd=_cost_assumptions.operator_hourly_rate_usd,
            planned_production_hours_per_day=_cost_assumptions.planned_production_hours_per_day,
        ),
    )


@router.put("/assumptions", response_model=ImpactAssumptionsSchema)
async def update_impact_assumptions(assumptions: ImpactAssumptionsSchema):
    global _cost_assumptions
    _cost_assumptions.downtime_cost_per_hour_usd = assumptions.downtime_cost_per_hour_usd
    _cost_assumptions.rework_cost_per_defect_usd = assumptions.rework_cost_per_defect_usd
    _cost_assumptions.scrap_cost_per_unit_usd = assumptions.scrap_cost_per_unit_usd
    _cost_assumptions.field_recall_cost_per_unit_usd = assumptions.field_recall_cost_per_unit_usd
    _cost_assumptions.operator_hourly_rate_usd = assumptions.operator_hourly_rate_usd
    _cost_assumptions.planned_production_hours_per_day = assumptions.planned_production_hours_per_day
    return assumptions
