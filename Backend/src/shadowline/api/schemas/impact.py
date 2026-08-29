"""Impact API schemas."""

from typing import Optional
from pydantic import BaseModel


class ImpactAssumptionsSchema(BaseModel):
    downtime_cost_per_hour_usd: float = 24000.0
    rework_cost_per_defect_usd: float = 450.0
    scrap_cost_per_unit_usd: float = 8500.0
    field_recall_cost_per_unit_usd: float = 12000.0
    operator_hourly_rate_usd: float = 65.0
    planned_production_hours_per_day: float = 16.0


class OEESchema(BaseModel):
    availability: float
    performance: float
    quality: float
    oee: float
    target_jph: float
    actual_jph: float


class ImpactSummaryResponse(BaseModel):
    downtime_loss_usd: float
    avoided_downtime_savings_usd: float
    rework_expense_usd: float
    prevented_defect_savings_usd: float
    containment_recall_avoided_usd: float
    net_savings_usd: float
    oee: OEESchema
    assumptions: ImpactAssumptionsSchema
