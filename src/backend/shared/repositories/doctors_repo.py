"""Shared doctors repository."""
from __future__ import annotations

from typing import Dict, List

from .. import sample_data


class DoctorsRepository:
    def list_doctors(self, filters: Dict[str, str]) -> List[Dict[str, str]]:
        results: List[Dict[str, str]] = []
        for doctor in sample_data.DOCTORS:
            if filters.get("doctorId") and doctor["doctorId"] != filters["doctorId"]:
                continue
            if filters.get("clinicaId") and doctor["clinicaId"] != filters["clinicaId"]:
                continue
            if filters.get("especialidadId") and doctor["especialidadPrincipalId"] != filters["especialidadId"]:
                continue
            if filters.get("rimacEnsured") is not None and doctor.get("rimacEnsured") != filters["rimacEnsured"]:
                continue
            results.append(doctor)
        return results
