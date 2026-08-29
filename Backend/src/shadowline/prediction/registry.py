"""Prediction head registry."""

import logging
from typing import Dict, List, Optional
from shadowline.prediction.base import PredictionHead

logger = logging.getLogger("shadowline.prediction.registry")


class PredictionRegistry:
    """Central registry of active prediction heads."""

    def __init__(self):
        self._heads: Dict[str, PredictionHead] = {}

    def register(self, head: PredictionHead) -> None:
        self._heads[head.name] = head
        logger.info("Registered prediction head: %s", head.name)

    def get(self, name: str) -> Optional[PredictionHead]:
        return self._heads.get(name)

    def all_heads(self) -> List[PredictionHead]:
        return list(self._heads.values())
