"""State forking engine for creating isolated digital twin copies."""

import copy
from typing import Optional
from shadowline.twin.line_model import TwinLineModel
from shadowline.twin.snapshot import TwinSnapshot


class TwinForker:
    """Clones snapshot into an isolated SimPy digital twin simulation."""

    @staticmethod
    def fork(snapshot: TwinSnapshot, takt_time: float = 58.0) -> TwinLineModel:
        # Deepcopy snapshot so forward simulation cannot mutate source
        snap_copy = copy.deepcopy(snapshot)
        return TwinLineModel(snapshot=snap_copy, takt_time=takt_time)
