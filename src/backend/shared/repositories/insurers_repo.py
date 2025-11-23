"""Shared insurers repository."""
from __future__ import annotations

import os
from typing import Dict, List

import boto3
from boto3.dynamodb.conditions import Attr


class InsurersRepository:
    def __init__(self):
        env = os.environ.get("ENVIRONMENT", "dev")
        self.seguros_table_name = f"seguros-{env}"
        self.clinics_table_name = f"clinics-{env}"
        dynamodb = boto3.resource("dynamodb")
        self.seguros_table = dynamodb.Table(self.seguros_table_name)
        self.clinics_table = dynamodb.Table(self.clinics_table_name)
    
    def list_insurers(self, seguro_id: str | None = None) -> List[Dict[str, str]]:
        if seguro_id:
            response = self.seguros_table.get_item(Key={"seguroId": seguro_id})
            item = response.get("Item")
            return [item] if item else []
        else:
            response = self.seguros_table.scan()
            return response.get("Items", [])

    def list_clinics_by_insurer(self, seguro_id: str) -> List[Dict[str, str]]:
        response = self.clinics_table.scan(
            FilterExpression=Attr("seguroIds").contains(seguro_id)
        )
        return response.get("Items", [])
