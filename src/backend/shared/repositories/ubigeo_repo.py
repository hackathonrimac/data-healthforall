"""Shared ubigeo repository."""
from __future__ import annotations

import os
from typing import Optional

import boto3


class UbigeoRepository:
    def __init__(self):
        env = os.environ.get("ENVIRONMENT", "dev")
        self.table_name = f"ubigeo-{env}"
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(self.table_name)
    
    def exists(self, ubigeo_id: str) -> bool:
        response = self.table.get_item(Key={"ubigeoId": ubigeo_id})
        return "Item" in response

    def get_name(self, ubigeo_id: str) -> Optional[str]:
        response = self.table.get_item(Key={"ubigeoId": ubigeo_id})
        item = response.get("Item")
        return item.get("nombreDistrito") if item else None
