"""DTOs for Search API."""
from __future__ import annotations

from dataclasses import dataclass

from shared import event_utils
from shared.exceptions import ValidationError


@dataclass
class SearchDoctorsQueryDTO:
    ubigeo_id: str | None
    especialidad_id: str | None
    seguro_id: str | None
    rimac_ensured: bool | None
    page: int
    page_size: int

    @classmethod
    def from_event(cls, event):
        params = event_utils.get_query_params(event)
        ubigeo_id = event_utils.optional_param(params, "ubigeoId")
        especialidad_id = event_utils.optional_param(params, "especialidadId")
        seguro_id = event_utils.optional_param(params, "seguroId")
        
        rimac_param = event_utils.optional_param(params, "rimacEnsured")
        rimac_ensured = None
        if rimac_param is not None:
            rimac_ensured = rimac_param.lower() in ("true", "1", "yes")
        
        # Require at least ONE search criterion
        if not ubigeo_id and not especialidad_id and not seguro_id and rimac_ensured is None:
            raise ValidationError("At least one search criterion required: ubigeoId, especialidadId, seguroId, or rimacEnsured")
        
        page = event_utils.get_int_param(params, "page", default=1, minimum=1)
        page_size = event_utils.get_int_param(params, "pageSize", default=10, minimum=1)
        return cls(ubigeo_id, especialidad_id, seguro_id, rimac_ensured, page, page_size)
