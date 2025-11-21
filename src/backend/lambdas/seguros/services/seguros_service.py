"""Seguros service."""
from __future__ import annotations

from typing import Dict

from dto import SegurosClinicasQueryDTO, SegurosQueryDTO
from repositories.insurers_repo import InsurersRepository


class SegurosService:
    def __init__(self, repo: InsurersRepository | None = None):
        self._repo = repo or InsurersRepository()

    def list_seguros(self, dto: SegurosQueryDTO) -> Dict[str, object]:
        items = self._repo.list_insurers(dto.seguro_id)
        return {"items": items, "count": len(items)}

    def list_clinicas(self, dto: SegurosClinicasQueryDTO) -> Dict[str, object]:
        clinics = self._repo.list_clinics_by_insurer(dto.seguro_id)
        return {"items": clinics, "count": len(clinics)}
