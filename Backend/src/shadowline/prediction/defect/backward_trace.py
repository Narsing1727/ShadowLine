"""Backward tracing of defect root causes."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from shadowline.domain.genealogy import GenealogyRecord
from shadowline.prediction.defect.propagation_graph import DefectPropagationGraph


@dataclass
class BackwardTraceCandidate:
    station_id: str
    defect_code: str
    likelihood_score: float
    historical_cases: int
    mean_lag_minutes: float
    reason: str


class DefectBackwardTracer:
    """Traces from a detected defect backward to identify probable causing stations."""

    def __init__(self, propagation_graph: DefectPropagationGraph):
        self.graph = propagation_graph

    def trace(
        self,
        defect_code: str,
        detecting_station_id: str,
        unit_genealogy: Optional[GenealogyRecord] = None,
    ) -> List[BackwardTraceCandidate]:
        candidates = []
        known_causes = self.graph.get_candidate_causes(detecting_station_id)

        # 1. Match against known graph relationships
        total_cases = sum(c["observed_cases"] for c in known_causes) if known_causes else 1
        for cause in known_causes:
            likelihood = cause["observed_cases"] / total_cases
            candidates.append(
                BackwardTraceCandidate(
                    station_id=cause["causing_station_id"],
                    defect_code=cause["defect_code"],
                    likelihood_score=round(likelihood, 2),
                    historical_cases=cause["observed_cases"],
                    mean_lag_minutes=cause["mean_lag_minutes"],
                    reason=f"Historical defect graph indicates {cause['observed_cases']} past correlation(s).",
                )
            )

        # 2. If genealogy is present, cross-reference visited stations
        if unit_genealogy and not candidates:
            # Fallback heuristic: immediate upstream visited stations
            for step in reversed(unit_genealogy.steps):
                if step.station_id != detecting_station_id:
                    candidates.append(
                        BackwardTraceCandidate(
                            station_id=step.station_id,
                            defect_code=defect_code,
                            likelihood_score=0.40,
                            historical_cases=1,
                            mean_lag_minutes=15.0,
                            reason=f"Station visited by unit {unit_genealogy.vin} during assembly.",
                        )
                    )
                    if len(candidates) >= 3:
                        break

        # Sort by likelihood
        candidates.sort(key=lambda x: x.likelihood_score, reverse=True)
        return candidates
