"""Shared clinics repository used by multiple Lambdas."""
from __future__ import annotations

import os
from typing import Dict, List

import boto3


class ClinicsRepository:
    def __init__(self):
        env = os.environ.get("ENVIRONMENT", "dev")
        self.table_name = f"clinics-{env}"
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(self.table_name)
    
    def list_clinics(self, filters: Dict[str, str]) -> List[Dict[str, str]]:
        # If specific clinicaId requested, get item directly
        if filters.get("clinicaId"):
            response = self.table.get_item(Key={"clinicaId": filters["clinicaId"]})
            item = response.get("Item")
            if item and self._matches_filters(item, filters):
                return [item]
            return []
        
        # Otherwise scan the table
        response = self.table.scan()
        items = response.get("Items", [])
        
        # Apply filters
        results = []
        for clinic in items:
            if self._matches_filters(clinic, filters):
                results.append(clinic)
        
        return results

    def get_clinic(self, clinica_id: str) -> Dict[str, str] | None:
        response = self.table.get_item(Key={"clinicaId": clinica_id})
        return response.get("Item")
    
    def _matches_filters(self, clinic: Dict[str, str], filters: Dict[str, str]) -> bool:
        """Check if clinic matches all provided filters."""
        if filters.get("ubigeoId") and clinic.get("ubigeoId") != filters["ubigeoId"]:
            return False
        if filters.get("especialidadId") and filters["especialidadId"] not in clinic.get("especialidadIds", []):
            return False
        if filters.get("seguroId") and filters["seguroId"] not in clinic.get("seguroIds", []):
            return False
        return True
