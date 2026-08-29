"""Operating mode manager (SHADOW vs LIVE)."""

import threading
from shadowline.domain.enums import Mode


class ModeManager:
    """Thread-safe manager for current ShadowLine operating mode."""

    def __init__(self, initial_mode: Mode = Mode.SHADOW):
        self._lock = threading.Lock()
        self._mode = initial_mode

    @property
    def current_mode(self) -> Mode:
        with self._lock:
            return self._mode

    def set_mode(self, mode: Mode) -> None:
        with self._lock:
            self._mode = mode

    @property
    def is_live(self) -> bool:
        return self.current_mode == Mode.LIVE
