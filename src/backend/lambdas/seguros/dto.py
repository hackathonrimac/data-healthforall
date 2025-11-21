"""DTOs for Seguros API."""
from __future__ import annotations

from dataclasses import dataclass

from shared import event_utils
from shared.exceptions import ValidationError


@dataclass
class SegurosQueryDTO:
    seguro_id: str | None

    @classmethod
    def from_event(cls, event):
        params = event_utils.get_query_params(event)
        return cls(event_utils.optional_param(params, "seguroId"))


@dataclass
class SegurosClinicasQueryDTO:
    seguro_id: str

    @classmethod
    def from_event(cls, event):
        params = event_utils.get_query_params(event)
        seguro_id = event_utils.optional_param(params, "seguroId")
        if not seguro_id:
            raise ValidationError("seguroId is required")
        return cls(seguro_id)
