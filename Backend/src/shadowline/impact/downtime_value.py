"""Downtime monetary impact valuation."""

from dataclasses import dataclass
from shadowline.impact.assumptions import CostAssumptions


@dataclass
class DowntimeImpact:
    downtime_hours: float
    monetary_loss_usd: float
    avoided_downtime_hours: float
    avoided_savings_usd: float


class DowntimeValuator:
    """Calculates monetary impact of line downtime and bottleneck delays."""

    @staticmethod
    def calculate(
        downtime_hours: float,
        avoided_hours: float,
        assumptions: CostAssumptions | None = None,
    ) -> DowntimeImpact:
        cost = assumptions or CostAssumptions()
        loss = downtime_hours * cost.downtime_cost_per_hour_usd
        savings = avoided_hours * cost.downtime_cost_per_hour_usd

        return DowntimeImpact(
            downtime_hours=round(downtime_hours, 2),
            monetary_loss_usd=round(loss, 2),
            avoided_downtime_hours=round(avoided_hours, 2),
            avoided_savings_usd=round(savings, 2),
        )
