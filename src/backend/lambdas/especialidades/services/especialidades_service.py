"""Specialties service."""
from __future__ import annotations

from typing import Dict, List

from dto import EspecialidadesQueryDTO, SubEspecialidadesQueryDTO
from repositories.specialties_repo import SpecialtiesRepository, SubSpecialtiesRepository


class EspecialidadesService:
    def __init__(
        self,
        specialties_repo: SpecialtiesRepository | None = None,
        subs_repo: SubSpecialtiesRepository | None = None,
    ):
        self._specialties_repo = specialties_repo or SpecialtiesRepository()
        self._subs_repo = subs_repo or SubSpecialtiesRepository()

    def list_specialties(self, dto: EspecialidadesQueryDTO) -> Dict[str, object]:
        items = self._specialties_repo.list_specialties(dto.especialidad_id)
        return {"items": items, "count": len(items)}

    def list_subspecialties(self, dto: SubEspecialidadesQueryDTO) -> Dict[str, object]:
        items = self._subs_repo.list_subspecialties(dto.especialidad_id)
        return {"items": items, "count": len(items)}
