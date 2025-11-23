"""Shared doctors repository."""
from __future__ import annotations

import os
from typing import Dict, List

import boto3


class DoctorsRepository:
    def __init__(self):
        env = os.environ.get("ENVIRONMENT", "dev")
        self.table_name = f"doctors-{env}"
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(self.table_name)
    
    def list_doctors(self, filters: Dict[str, str]) -> List[Dict[str, str]]:
        # If specific doctorId requested, get item directly
        if filters.get("doctorId"):
            response = self.table.get_item(Key={"doctorId": filters["doctorId"]})
            item = response.get("Item")
            if item and self._matches_filters(item, filters):
                return [item]
            return []
        
        # Otherwise scan the table with filters
        response = self.table.scan()
        items = response.get("Items", [])
        
        # Apply filters
        results = []
        for doctor in items:
            if self._matches_filters(doctor, filters):
                results.append(doctor)
        
        return results
    
    def _matches_filters(self, doctor: Dict[str, str], filters: Dict[str, str]) -> bool:
        """Check if doctor matches all provided filters."""
        # Handle clinicaId filter with both old (clinicaId) and new (clinicaIds array) format
        if filters.get("clinicaId"):
            if "clinicaId" in doctor and doctor.get("clinicaId") != filters["clinicaId"]:
                return False
            elif "clinicaIds" in doctor:
                clinica_ids = doctor.get("clinicaIds", [])
                if isinstance(clinica_ids, list):
                    if filters["clinicaId"] not in clinica_ids:
                        return False
                elif clinica_ids != filters["clinicaId"]:
                    return False
        
        # Use especialidadId (the actual field in the data)
        if filters.get("especialidadId"):
            doctor_especialidad = doctor.get("especialidadId")
            if doctor_especialidad != filters["especialidadId"]:
                return False
        
        if filters.get("rimacEnsured") is not None and doctor.get("rimacEnsured") != filters["rimacEnsured"]:
            return False
        return True
