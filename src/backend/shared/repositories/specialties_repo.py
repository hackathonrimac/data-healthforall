"""Shared specialties repositories."""
from __future__ import annotations

from typing import Dict, List

from .. import sample_data


class SpecialtiesRepository:
    def list_specialties(self, especialidad_id: str | None = None) -> List[Dict[str, str]]:
        items = sample_data.SPECIALTIES
        if especialidad_id:
            return [item for item in items if item["especialidadId"] == especialidad_id]
        return list(items)


class SubSpecialtiesRepository:
    def list_subspecialties(self, especialidad_id: str | None = None) -> List[Dict[str, str]]:
        items = sample_data.SUBSPECIALTIES
        if especialidad_id:
            return [item for item in items if item["especialidadId"] == especialidad_id]
        return list(items)
