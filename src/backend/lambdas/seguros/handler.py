"""Lambda handler for Seguros API."""
from __future__ import annotations

from typing import Any, Dict

from shared.exceptions import ValidationError
from shared.http import json_response
from dto import SegurosClinicasQueryDTO, SegurosQueryDTO
from services.seguros_service import SegurosService

service = SegurosService()


def handler(event: Dict[str, Any], _context: Any) -> Dict[str, Any]:
    resource = (event.get("resource") or event.get("path") or "").lower()
    try:
        if resource.endswith("seguros-clinicas"):
            dto = SegurosClinicasQueryDTO.from_event(event)
            result = service.list_clinicas(dto)
        else:
            dto = SegurosQueryDTO.from_event(event)
            result = service.list_seguros(dto)
        return json_response(200, result)
    except ValidationError as exc:
        return json_response(400, {"message": str(exc)})
