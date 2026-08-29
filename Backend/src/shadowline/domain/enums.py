"""Domain enumerations for ShadowLine."""

from enum import Enum


class StationState(str, Enum):
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    STARVED = "STARVED"
    DOWN = "DOWN"


class ConfidenceTier(str, Enum):
    MEASURED = "MEASURED"
    INFERRED = "INFERRED"
    DARK = "DARK"


class Zone(str, Enum):
    BODY_SHOP = "BODY_SHOP"
    PAINT_SHOP = "PAINT_SHOP"
    FINAL_ASSEMBLY = "FINAL_ASSEMBLY"


class Mode(str, Enum):
    SHADOW = "SHADOW"
    LIVE = "LIVE"


class Variant(str, Enum):
    SUV_A = "SUV_A"
    SEDAN_B = "SEDAN_B"
    EV_C = "EV_C"


class EventType(str, Enum):
    STATION_STATE_CHANGED = "STATION_STATE_CHANGED"
    UNIT_EXITED_STATION = "UNIT_EXITED_STATION"
    DEFECT_DETECTED = "DEFECT_DETECTED"
    HEARTBEAT = "HEARTBEAT"


class AlertSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    SNOOZED = "SNOOZED"
    DISMISSED = "DISMISSED"
    FALSE_ALARM = "FALSE_ALARM"


class PredictionType(str, Enum):
    BOTTLENECK = "BOTTLENECK"
    DEFECT_PROPAGATION = "DEFECT_PROPAGATION"
    SOFT_SENSOR = "SOFT_SENSOR"
