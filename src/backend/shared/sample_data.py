"""Simple in-memory dataset so Lambdas can run locally without AWS."""
from __future__ import annotations

from typing import Dict, List

CLINICS: List[Dict[str, str]] = [
    {
        "clinicaId": "CLIN-001",
        "nombreClinica": "Clínica Internacional Lima",
        "ubicacion": "Av. Javier Prado 123, Lima",
        "ubigeoId": "150101",
        "especialidadIds": ["CARD", "NEURO"],
        "seguroIds": ["RIMAC", "PACIFICO"],
        "grupoClinicaId": "GRP-01",
        "url": "https://clinica.example/",
    },
    {
        "clinicaId": "CLIN-002",
        "nombreClinica": "Clínica del Sur",
        "ubicacion": "Av. Benavides 456, Lima",
        "ubigeoId": "150132",
        "especialidadIds": ["DERM", "CARD"],
        "seguroIds": ["RIMAC"],
        "grupoClinicaId": "GRP-02",
        "url": "https://clinicasur.example/",
    },
]

DOCTORS: List[Dict[str, str]] = [
    {
        "doctorId": "DOC-001",
        "nombreCompleto": "Dr. Juan Pérez",
        "especialidadPrincipalId": "CARD",
        "subEspecialidadIds": ["CARD_INT"],
        "clinicaId": "CLIN-001",
        "photoUrl": "https://images.example/doc1.png",
    },
    {
        "doctorId": "DOC-002",
        "nombreCompleto": "Dra. María López",
        "especialidadPrincipalId": "DERM",
        "subEspecialidadIds": [],
        "clinicaId": "CLIN-002",
        "photoUrl": "https://images.example/doc2.png",
    },
]

SPECIALTIES: List[Dict[str, str]] = [
    {"especialidadId": "CARD", "nombre": "Cardiología"},
    {"especialidadId": "DERM", "nombre": "Dermatología"},
]

SUBSPECIALTIES: List[Dict[str, str]] = [
    {"subEspecialidadId": "CARD_INT", "especialidadId": "CARD", "nombre": "Cardiología Intervencionista"}
]

INSURERS: List[Dict[str, str]] = [
    {"seguroId": "RIMAC", "nombre": "RIMAC Seguros"},
    {"seguroId": "PACIFICO", "nombre": "Pacífico"},
]

UBIGEOS: List[Dict[str, str]] = [
    {"ubigeoId": "150101", "nombreDistrito": "Lima"},
    {"ubigeoId": "150132", "nombreDistrito": "Santiago de Surco"},
]
