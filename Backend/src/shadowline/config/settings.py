"""ShadowLine service configuration settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class ShadowLineSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SHADOWLINE_", env_file=".env", extra="ignore")

    mode: str = "SHADOW"  # SHADOW or LIVE
    line_config: str = "configs/lines/plant2_line_a.yaml"
    variants_config: str = "configs/variants.yaml"
    thresholds_config: str = "configs/thresholds.yaml"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:5173"

    db_url: str = "sqlite:///./data/shadowline.db"

    fork_interval_seconds: int = 60
    forecast_horizon_hours: float = 4.0
    monte_carlo_runs: int = 50

    alarm_budget_per_operator_per_hour: int = 6
    log_level: str = "INFO"
