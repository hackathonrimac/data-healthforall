"""DTOs for Doctors API."""
from __future__ import annotations

from dataclasses import dataclass

from shared import event_utils


@dataclass
class DoctorsQueryDTO:
    especialidad_id: str | None
    clinica_id: str | None
    doctor_id: str | None
    page: int
    page_size: int

    @classmethod
    def from_event(cls, event):
        params = event_utils.get_query_params(event)
        return cls(
            especialidad_id=event_utils.optional_param(params, "especialidadId"),
            clinica_id=event_utils.optional_param(params, "clinicaId"),
            doctor_id=event_utils.optional_param(params, "doctorId"),
            page=event_utils.get_int_param(params, "page", default=1, minimum=1),
            page_size=event_utils.get_int_param(params, "pageSize", default=10, minimum=1),
        )
