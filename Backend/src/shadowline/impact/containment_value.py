"""Containment value and recall-risk avoidance calculation."""

from dataclasses import dataclass
from shadowline.impact.assumptions import CostAssumptions


@dataclass
class ContainmentValueReport:
    units_quarantined: int
    units_prevented_from_shipping: int
    recall_risk_avoided_usd: float
    net_containment_benefit_usd: float


class ContainmentValuator:
    """Calculates financial risk avoidance by quarantining units before vehicle dispatch."""

    @staticmethod
    def calculate(
        units_quarantined: int,
        assumptions: CostAssumptions | None = None,
    ) -> ContainmentValueReport:
        cost = assumptions or CostAssumptions()
        # Risk of recall if bad unit leaves factory
        recall_risk = units_quarantined * cost.field_recall_cost_per_unit_usd
        rework_expense = units_quarantined * cost.rework_cost_per_defect_usd
        net_benefit = max(0.0, recall_risk - rework_expense)

        return ContainmentValueReport(
            units_quarantined=units_quarantined,
            units_prevented_from_shipping=units_quarantined,
            recall_risk_avoided_usd=round(recall_risk, 2),
            net_containment_benefit_usd=round(net_benefit, 2),
        )
