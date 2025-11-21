"""Shared ubigeo repository."""
from __future__ import annotations

from typing import Optional

from .. import sample_data


class UbigeoRepository:
    def exists(self, ubigeo_id: str) -> bool:
        return any(item["ubigeoId"] == ubigeo_id for item in sample_data.UBIGEOS)

    def get_name(self, ubigeo_id: str) -> Optional[str]:
        for item in sample_data.UBIGEOS:
            if item["ubigeoId"] == ubigeo_id:
                return item["nombreDistrito"]
        return None
