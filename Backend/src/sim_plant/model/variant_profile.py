"""Variant definitions and defect profiles."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np


@dataclass
class DefectBaseline:
    defect_code: str
    causing_station_id: str
    detecting_station_id: str
    base_probability: float
    lag_minutes_mean: float
    lag_minutes_std: float


@dataclass
class VariantProfile:
    id: str
    name: str
    production_share: float
    cycle_time_multiplier: float
    defect_baselines: List[DefectBaseline] = field(default_factory=list)


def parse_variant_profiles(variants_data: Dict) -> Dict[str, VariantProfile]:
    profiles = {}
    for var in variants_data.get("variants", []):
        baselines = [
            DefectBaseline(
                defect_code=db["defect_code"],
                causing_station_id=db["causing_station_id"],
                detecting_station_id=db["detecting_station_id"],
                base_probability=db["base_probability"],
                lag_minutes_mean=db["lag_minutes_mean"],
                lag_minutes_std=db["lag_minutes_std"],
            )
            for db in var.get("defect_baselines", [])
        ]
        profiles[var["id"]] = VariantProfile(
            id=var["id"],
            name=var["name"],
            production_share=var["production_share"],
            cycle_time_multiplier=var["cycle_time_multiplier"],
            defect_baselines=baselines,
        )
    return profiles
