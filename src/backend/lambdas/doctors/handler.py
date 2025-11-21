"""AWS Lambda handler for Doctors API."""
from __future__ import annotations

from typing import Any, Dict

from shared.exceptions import ValidationError
from shared.http import json_response
from dto import DoctorsQueryDTO
from services.doctors_service import DoctorsService

service = DoctorsService()


def handler(event: Dict[str, Any], _context: Any) -> Dict[str, Any]:
    try:
        dto = DoctorsQueryDTO.from_event(event)
        result = service.list_doctors(dto)
        return json_response(200, result)
    except ValidationError as exc:
        return json_response(400, {"message": str(exc)})
    except Exception as exc:  # pragma: no cover - defensive logging placeholder
        print(f"[Doctors] Unexpected error: {exc}")
        return json_response(500, {"message": "Internal server error"})
