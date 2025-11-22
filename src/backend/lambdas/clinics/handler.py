"""AWS Lambda handler for Clinics API."""
from __future__ import annotations

from typing import Any, Dict

from shared.exceptions import ValidationError
from shared.http import json_response
from dto import ClinicsQueryDTO
from services.clinics_service import ClinicsService

service = ClinicsService()


def handler(event: Dict[str, Any], _context: Any) -> Dict[str, Any]:
    try:
        dto = ClinicsQueryDTO.from_event(event)
        result = service.list_clinics(dto)
        return json_response(200, result)
    except ValidationError as exc:
        return json_response(400, {"message": str(exc)})
    except Exception as exc:  # pragma: no cover - defensive logging placeholder
        print(f"[Clinics] Unexpected error: {exc}")
        return json_response(500, {"message": "Internal server error"})
