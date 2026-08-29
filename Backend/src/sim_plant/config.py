"""Configuration loader for sim_plant."""

from pathlib import Path
from typing import Any, Dict
import yaml
from pydantic_settings import BaseSettings, SettingsConfigDict


class SimPlantSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SIM_PLANT_", env_file=".env", extra="ignore")

    line_config: str = "configs/lines/plant2_line_a.yaml"
    variants_config: str = "configs/variants.yaml"
    faults_config: str = "configs/faults.yaml"
    speed_factor: float = 1.0
    transport: str = "http"
    emit_host: str = "0.0.0.0"
    emit_port: int = 8100


def load_yaml(path_str: str) -> Dict[str, Any]:
    path = Path(path_str)
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
