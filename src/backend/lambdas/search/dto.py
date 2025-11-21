"""DTOs for Search API."""
from __future__ import annotations

from dataclasses import dataclass

from shared import event_utils


@dataclass
class SearchDoctorsQueryDTO:
    ubigeo_id: str
    especialidad_id: str
    seguro_id: str | None
    page: int
    page_size: int

    @classmethod
    def from_event(cls, event):
        params = event_utils.get_query_params(event)
        ubigeo_id = event_utils.require_param(params, "ubigeoId")
        especialidad_id = event_utils.require_param(params, "especialidadId")
        seguro_id = event_utils.optional_param(params, "seguroId")
        page = event_utils.get_int_param(params, "page", default=1, minimum=1)
        page_size = event_utils.get_int_param(params, "pageSize", default=10, minimum=1)
        return cls(ubigeo_id, especialidad_id, seguro_id, page, page_size)
