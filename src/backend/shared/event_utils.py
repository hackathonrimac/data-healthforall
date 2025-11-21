"""Helpers to work with API Gateway proxy events."""
from __future__ import annotations

from typing import Any, Dict, Optional

from .exceptions import ValidationError


def get_query_params(event: Dict[str, Any]) -> Dict[str, str]:
    params = event.get("queryStringParameters") or {}
    # API Gateway can pass None, ensure str keys/values
    return {k: v for k, v in params.items() if v is not None}


def require_param(params: Dict[str, str], name: str) -> str:
    value = params.get(name)
    if not value:
        raise ValidationError(f"Missing required parameter: {name}")
    return value


def get_int_param(params: Dict[str, str], name: str, default: int, minimum: int) -> int:
    raw = params.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:  # pragma: no cover - defensive
        raise ValidationError(f"Parameter {name} must be an integer") from exc
    if value < minimum:
        raise ValidationError(f"Parameter {name} must be >= {minimum}")
    return value


def optional_param(params: Dict[str, str], name: str) -> Optional[str]:
    value = params.get(name)
    return value if value else None
