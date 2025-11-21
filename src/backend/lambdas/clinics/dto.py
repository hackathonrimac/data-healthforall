"""DTOs for Clinics API."""
from __future__ import annotations

from dataclasses import dataclass

from shared import event_utils
from shared.exceptions import ValidationError


@dataclass
class ClinicsQueryDTO:
    ubigeo_id: str | None
    especialidad_id: str | None
    seguro_id: str | None
    clinica_id: str | None
    page: int
    page_size: int

    @classmethod
    def from_event(cls, event):
        params = event_utils.get_query_params(event)
        ubigeo_id = event_utils.optional_param(params, "ubigeoId")
        especialidad_id = event_utils.optional_param(params, "especialidadId")
        seguro_id = event_utils.optional_param(params, "seguroId")
        clinica_id = event_utils.optional_param(params, "clinicaId")
        page = event_utils.get_int_param(params, "page", default=1, minimum=1)
        page_size = event_utils.get_int_param(params, "pageSize", default=10, minimum=1)
        if clinica_id and (ubigeo_id or especialidad_id or seguro_id):
            raise ValidationError("When clinicaId is provided, remove other filters")
        return cls(ubigeo_id, especialidad_id, seguro_id, clinica_id, page, page_size)
