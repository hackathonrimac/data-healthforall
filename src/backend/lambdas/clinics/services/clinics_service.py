"""Service logic for Clinics API."""
from __future__ import annotations

from typing import Dict, List

from shared.exceptions import ValidationError
from dto import ClinicsQueryDTO
from repositories.clinics_repo import ClinicsRepository
from repositories.ubigeo_repo import UbigeoRepository


class ClinicsService:
    def __init__(self, clinics_repo: ClinicsRepository | None = None, ubigeo_repo: UbigeoRepository | None = None):
        self._clinics_repo = clinics_repo or ClinicsRepository()
        self._ubigeo_repo = ubigeo_repo or UbigeoRepository()

    def list_clinics(self, dto: ClinicsQueryDTO) -> Dict[str, object]:
        if dto.ubigeo_id and not self._ubigeo_repo.exists(dto.ubigeo_id):
            raise ValidationError("Invalid ubigeoId")

        filters = {
            "ubigeoId": dto.ubigeo_id,
            "especialidadId": dto.especialidad_id,
            "seguroId": dto.seguro_id,
            "clinicaId": dto.clinica_id,
        }

        clinics = self._clinics_repo.list_clinics(filters)
        total = len(clinics)
        start = (dto.page - 1) * dto.page_size
        end = start + dto.page_size
        paged = clinics[start:end]
        items = [self._to_response_model(clinic) for clinic in paged]
        return {
            "items": items,
            "page": dto.page,
            "pageSize": dto.page_size,
            "total": total,
        }

    @staticmethod
    def _to_response_model(clinic: Dict[str, str]) -> Dict[str, object]:
        return {
            "clinicaId": clinic["clinicaId"],
            "nombreClinica": clinic["nombreClinica"],
            "ubicacion": clinic["ubicacion"],
            "ubigeoId": clinic["ubigeoId"],
            "especialidadIds": clinic["especialidadIds"],
            "seguroIds": clinic["seguroIds"],
            "url": clinic["url"],
        }
