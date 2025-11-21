"""DTOs for Especialidades API."""
from __future__ import annotations

from dataclasses import dataclass

from shared import event_utils


@dataclass
class EspecialidadesQueryDTO:
    especialidad_id: str | None

    @classmethod
    def from_event(cls, event):
        params = event_utils.get_query_params(event)
        return cls(event_utils.optional_param(params, "especialidadId"))


@dataclass
class SubEspecialidadesQueryDTO:
    especialidad_id: str | None

    @classmethod
    def from_event(cls, event):
        params = event_utils.get_query_params(event)
        return cls(event_utils.optional_param(params, "especialidadId"))
