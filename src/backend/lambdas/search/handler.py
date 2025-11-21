"""Lambda handler for Search API doctor cards."""
from __future__ import annotations

from typing import Any, Dict

from shared.exceptions import ValidationError
from shared.http import json_response
from dto import SearchDoctorsQueryDTO
from services.search_service import SearchService

service = SearchService()


def handler(event: Dict[str, Any], _context: Any) -> Dict[str, Any]:
    try:
        dto = SearchDoctorsQueryDTO.from_event(event)
        result = service.search_doctors(dto)
        return json_response(200, result)
    except ValidationError as exc:
        return json_response(400, {"message": str(exc)})
    except Exception as exc:  # pragma: no cover - defensive logging placeholder
        print(f"[Search] Unexpected error: {exc}")
        return json_response(500, {"message": "Internal server error"})
