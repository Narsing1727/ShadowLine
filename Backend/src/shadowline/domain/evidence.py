"""Evidence and explanation domain models."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EvidenceItem:
    metric_name: str
    observed_value: Any
    threshold_value: Optional[Any] = None
    unit: Optional[str] = None
    description: str = ""
    supporting_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Explanation:
    summary: str
    key_factors: List[str] = field(default_factory=list)
    evidence_items: List[EvidenceItem] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
