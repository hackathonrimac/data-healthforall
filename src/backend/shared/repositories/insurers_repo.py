"""Shared insurers repository."""
from __future__ import annotations

from typing import Dict, List

from .. import sample_data


class InsurersRepository:
    def list_insurers(self, seguro_id: str | None = None) -> List[Dict[str, str]]:
        items = sample_data.INSURERS
        if seguro_id:
            return [item for item in items if item["seguroId"] == seguro_id]
        return list(items)

    def list_clinics_by_insurer(self, seguro_id: str) -> List[Dict[str, str]]:
        clinics = []
        for clinic in sample_data.CLINICS:
            if seguro_id in clinic["seguroIds"]:
                clinics.append(clinic)
        return clinics
