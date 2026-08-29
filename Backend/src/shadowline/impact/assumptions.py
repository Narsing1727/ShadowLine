"""Financial and operational cost assumptions for impact calculation."""

from dataclasses import dataclass


@dataclass
class CostAssumptions:
    downtime_cost_per_hour_usd: float = 24000.0  # Industry standard ~$400/min for auto assembly
    rework_cost_per_defect_usd: float = 450.0
    scrap_cost_per_unit_usd: float = 8500.0
    field_recall_cost_per_unit_usd: float = 12000.0
    operator_hourly_rate_usd: float = 65.0
    planned_production_hours_per_day: float = 16.0
