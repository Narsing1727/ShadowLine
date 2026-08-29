"""Active Period Method (APM) bottleneck detection."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from shadowline.twin.snapshot import TwinSnapshot


@dataclass
class ActivePeriodResult:
    station_id: str
    active_percentage: float
    blocked_percentage: float
    starved_percentage: float
    is_current_bottleneck: bool


class ActivePeriodCalculator:
    """Calculates active period ratios and identifies the empirical bottleneck."""

    @staticmethod
    def calculate(snapshot: TwinSnapshot) -> Dict[str, ActivePeriodResult]:
        results = {}
        max_active_pct = -1.0
        bottleneck_id = None

        for s_id, s_snap in snapshot.stations.items():
            total = (
                s_snap.active_period_seconds
                + s_snap.blocked_period_seconds
                + s_snap.starved_period_seconds
                + s_snap.down_period_seconds
            )
            if total <= 0:
                # Default to nominal cycle time heuristic if brand new
                act_pct = 0.33
                blk_pct = 0.33
                stv_pct = 0.33
            else:
                act_pct = s_snap.active_period_seconds / total
                blk_pct = s_snap.blocked_period_seconds / total
                stv_pct = s_snap.starved_period_seconds / total

            if act_pct > max_active_pct:
                max_active_pct = act_pct
                bottleneck_id = s_id

            results[s_id] = ActivePeriodResult(
                station_id=s_id,
                active_percentage=act_pct,
                blocked_percentage=blk_pct,
                starved_percentage=stv_pct,
                is_current_bottleneck=False,
            )

        if bottleneck_id and bottleneck_id in results:
            results[bottleneck_id].is_current_bottleneck = True

        return results
