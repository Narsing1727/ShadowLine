"""Sensor gaps and coverage enforcement for emitted events."""

import random
from typing import Any, Dict, Optional


class SensorGapFilter:
    """Enforces deliberate information withholding for DARK and INFERRED stations."""

    @staticmethod
    def filter_event(event_type: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        tier = payload.get("confidence_tier", "MEASURED")

        # 1. DARK stations:
        # Station state changes and internal cycle times are withheld entirely.
        # Only UNIT_EXITED_STATION timestamps are known (simulating optical sensor / RFID at boundary).
        if tier == "DARK":
            if event_type == "STATION_STATE_CHANGED":
                # Withhold internal state telemetry
                return None
            if event_type == "UNIT_EXITED_STATION":
                # Remove dwell time details, keep exit timestamp and VIN
                clean_payload = dict(payload)
                clean_payload.pop("dwell_seconds", None)
                return clean_payload

        # 2. INFERRED stations:
        # State transitions may occasionally be noisy / delayed
        if tier == "INFERRED":
            clean_payload = dict(payload)
            if "cycle_time_seconds" in clean_payload and clean_payload["cycle_time_seconds"] is not None:
                # Add minor sensor noise (+- 5%)
                clean_payload["cycle_time_seconds"] = round(
                    clean_payload["cycle_time_seconds"] * random.uniform(0.95, 1.05), 2
                )
            return clean_payload

        # 3. MEASURED stations pass through cleanly
        return dict(payload)
