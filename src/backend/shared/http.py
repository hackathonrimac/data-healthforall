"""Utilities for building Lambda proxy integration responses."""
from __future__ import annotations

import json
from typing import Any, Dict

_DEFAULT_HEADERS = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}


def json_response(status_code: int, body: Any, headers: Dict[str, str] | None = None) -> Dict[str, Any]:
    """Return an API Gateway compatible JSON response."""
    final_headers = {**_DEFAULT_HEADERS, **(headers or {})}
    serialised = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
    return {
        "statusCode": status_code,
        "headers": final_headers,
        "body": serialised,
    }
