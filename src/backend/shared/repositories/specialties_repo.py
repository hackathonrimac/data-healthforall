"""Shared specialties repositories."""
from __future__ import annotations

import os
from typing import Dict, List

import boto3
from boto3.dynamodb.conditions import Attr


class SpecialtiesRepository:
    def __init__(self):
        env = os.environ.get("ENVIRONMENT", "dev")
        self.table_name = f"especialidades-{env}"
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(self.table_name)
    
    def list_specialties(self, especialidad_id: str | None = None) -> List[Dict[str, str]]:
        if especialidad_id:
            response = self.table.get_item(Key={"especialidadId": especialidad_id})
            item = response.get("Item")
            return [item] if item else []
        else:
            response = self.table.scan()
            return response.get("Items", [])


class SubSpecialtiesRepository:
    def __init__(self):
        env = os.environ.get("ENVIRONMENT", "dev")
        self.table_name = f"subespecialidades-{env}"
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(self.table_name)
    
    def list_subspecialties(self, especialidad_id: str | None = None) -> List[Dict[str, str]]:
        if especialidad_id:
            response = self.table.scan(
                FilterExpression=Attr("especialidadId").eq(especialidad_id)
            )
            return response.get("Items", [])
        else:
            response = self.table.scan()
            return response.get("Items", [])
