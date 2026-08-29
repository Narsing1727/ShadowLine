"""NetworkX-based Defect Propagation Graph."""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import networkx as nx


@dataclass
class PropagationEdge:
    source_station_id: str
    target_station_id: str
    defect_code: str
    mean_lag_minutes: float
    std_lag_minutes: float
    observed_case_count: int
    confidence_score: float


class DefectPropagationGraph:
    """Maintains a directed graph of defect propagation relationships across stations."""

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_or_update_edge(
        self,
        source_id: str,
        target_id: str,
        defect_code: str,
        lag_minutes: float,
    ) -> None:
        if self.graph.has_edge(source_id, target_id):
            edge_data = self.graph[source_id][target_id]
            edge_data["case_count"] += 1
            lags = edge_data.get("lags", [])
            lags.append(lag_minutes)
            edge_data["lags"] = lags
            edge_data["defect_code"] = defect_code
        else:
            self.graph.add_edge(
                source_id,
                target_id,
                defect_code=defect_code,
                case_count=1,
                lags=[lag_minutes],
            )

    def get_candidate_causes(self, detecting_station_id: str) -> List[Dict[str, Any]]:
        """Returns all upstream stations that have known edges to the detecting station."""
        candidates = []
        if not self.graph.has_node(detecting_station_id):
            return candidates

        for predecessor in self.graph.predecessors(detecting_station_id):
            edge_data = self.graph[predecessor][detecting_station_id]
            lags = edge_data.get("lags", [10.0])
            mean_lag = sum(lags) / len(lags)
            candidates.append(
                {
                    "causing_station_id": predecessor,
                    "defect_code": edge_data.get("defect_code", "UNKNOWN"),
                    "observed_cases": edge_data.get("case_count", 1),
                    "mean_lag_minutes": round(mean_lag, 2),
                }
            )
        return candidates

    def to_dict(self) -> Dict[str, Any]:
        nodes = list(self.graph.nodes)
        edges = []
        for u, v, data in self.graph.edges(data=True):
            lags = data.get("lags", [])
            mean_lag = (sum(lags) / len(lags)) if lags else 0.0
            edges.append(
                {
                    "source": u,
                    "target": v,
                    "defect_code": data.get("defect_code", ""),
                    "case_count": data.get("case_count", 0),
                    "mean_lag_minutes": round(mean_lag, 2),
                }
            )
        return {"nodes": nodes, "edges": edges}
