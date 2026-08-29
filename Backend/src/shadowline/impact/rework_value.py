"""Rework and scrap financial valuation."""

from dataclasses import dataclass
from shadowline.impact.assumptions import CostAssumptions


@dataclass
class ReworkImpact:
    total_defects_detected: int
    rework_cost_usd: float
    prevented_defects: int
    prevented_savings_usd: float


class ReworkValuator:
    """Calculates rework and scrap monetary metrics from defect counts."""

    @staticmethod
    def calculate(
        defects_detected: int,
        defects_prevented: int,
        assumptions: CostAssumptions | None = None,
    ) -> ReworkImpact:
        cost = assumptions or CostAssumptions()
        rework = defects_detected * cost.rework_cost_per_defect_usd
        savings = defects_prevented * cost.rework_cost_per_defect_usd

        return ReworkImpact(
            total_defects_detected=defects_detected,
            rework_cost_usd=round(rework, 2),
            prevented_defects=defects_prevented,
            prevented_savings_usd=round(savings, 2),
        )
