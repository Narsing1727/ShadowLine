"""Genealogy repository."""

import json
from typing import List, Optional
from sqlalchemy.orm import Session
from shadowline.domain.genealogy import GenealogyRecord
from shadowline.persistence.models import GenealogyModel


class GenealogyRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_step(
        self,
        vin: str,
        variant: str,
        station_id: str,
        station_name: str,
        entered_at,
        exited_at=None,
        dwell_seconds=None,
        defect_codes=None,
    ) -> GenealogyModel:
        model = GenealogyModel(
            vin=vin,
            variant=variant,
            station_id=station_id,
            station_name=station_name,
            entered_at=entered_at,
            exited_at=exited_at,
            dwell_seconds=dwell_seconds,
            defect_codes_json=json.dumps(defect_codes or []),
        )
        self.session.add(model)
        self.session.commit()
        return model

    def get_trail_for_vin(self, vin: str) -> List[GenealogyModel]:
        return (
            self.session.query(GenealogyModel)
            .filter(GenealogyModel.vin == vin)
            .order_by(GenealogyModel.entered_at.asc())
            .all()
        )
