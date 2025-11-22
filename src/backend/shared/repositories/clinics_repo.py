"""Shared clinics repository used by multiple Lambdas."""
from __future__ import annotations

from typing import Dict, List

from .. import sample_data


class ClinicsRepository:
    def list_clinics(self, filters: Dict[str, str]) -> List[Dict[str, str]]:
        results: List[Dict[str, str]] = []
        for clinic in sample_data.CLINICS:
            if filters.get("clinicaId") and clinic["clinicaId"] != filters["clinicaId"]:
                continue
            if filters.get("ubigeoId") and clinic["ubigeoId"] != filters["ubigeoId"]:
                continue
            if filters.get("especialidadId") and filters["especialidadId"] not in clinic["especialidadIds"]:
                continue
            if filters.get("seguroId") and filters["seguroId"] not in clinic["seguroIds"]:
                continue
            results.append(clinic)
        return results

    def get_clinic(self, clinica_id: str) -> Dict[str, str] | None:
        for clinic in sample_data.CLINICS:
            if clinic["clinicaId"] == clinica_id:
                return clinic
        return None
