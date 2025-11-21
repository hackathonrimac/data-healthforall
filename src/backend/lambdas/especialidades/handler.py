"""Lambda handler for Especialidades API."""
from __future__ import annotations

from typing import Any, Dict

from shared.http import json_response
from dto import EspecialidadesQueryDTO, SubEspecialidadesQueryDTO
from services.especialidades_service import EspecialidadesService

service = EspecialidadesService()


def handler(event: Dict[str, Any], _context: Any) -> Dict[str, Any]:
    resource = (event.get("resource") or event.get("path") or "").lower()
    if resource.endswith("subespecialidades"):
        dto = SubEspecialidadesQueryDTO.from_event(event)
        result = service.list_subspecialties(dto)
    else:
        dto = EspecialidadesQueryDTO.from_event(event)
        result = service.list_specialties(dto)
    return json_response(200, result)
