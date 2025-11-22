"""Simple in-memory dataset so Lambdas can run locally without AWS."""
from __future__ import annotations

from typing import Dict, List, Any

CLINICS: List[Dict[str, Any]] = [
    {
        "clinicaId": "CLIN-001",
        "nombreClinica": "Clínica Internacional Lima",
        "ubicacion": "Av. Javier Prado Este 123, San Isidro",
        "ubigeoId": "150101",
        "especialidadIds": ["CARD", "NEURO", "TRAUM"],
        "seguroIds": ["RIMAC", "PACIFICO"],
        "grupoClinicaId": "GRP-01",
        "url": "https://clinicainternacional.com.pe/",
        "urlStaffMedico": "https://clinicainternacional.com.pe/doctores"
    },
    {
        "clinicaId": "CLIN-002",
        "nombreClinica": "Clínica Ricardo Palma",
        "ubicacion": "Av. Javier Prado Este 1066, San Isidro",
        "ubigeoId": "150101",
        "especialidadIds": ["DERM", "CARD", "ONCO"],
        "seguroIds": ["RIMAC", "PACIFICO", "MAPFRE"],
        "grupoClinicaId": "GRP-02",
        "url": "https://www.ricardopalma.com.pe/",
        "urlStaffMedico": "https://www.ricardopalma.com.pe/medicos"
    },
    {
        "clinicaId": "CLIN-003",
        "nombreClinica": "Clínica San Felipe",
        "ubicacion": "Av. Gregorio Escobedo 650, Jesús María",
        "ubigeoId": "150108",
        "especialidadIds": ["GINEC", "PEDIA", "CARD"],
        "seguroIds": ["RIMAC"],
        "grupoClinicaId": "GRP-03",
        "url": "https://www.clinicasanfelipe.com/",
        "urlStaffMedico": "https://www.clinicasanfelipe.com/staff"
    },
    {
        "clinicaId": "CLIN-004",
        "nombreClinica": "Clínica Javier Prado",
        "ubicacion": "Av. Javier Prado Este 499, San Isidro",
        "ubigeoId": "150101",
        "especialidadIds": ["TRAUM", "NEURO", "CARD"],
        "seguroIds": ["PACIFICO", "MAPFRE"],
        "grupoClinicaId": "GRP-04",
        "url": "https://www.clinicajavierprado.com.pe/",
        "urlStaffMedico": "https://www.clinicajavierprado.com.pe/medicos"
    },
    {
        "clinicaId": "CLIN-005",
        "nombreClinica": "Clínica Anglo Americana",
        "ubicacion": "Av. Alfredo Salazar 350, San Isidro",
        "ubigeoId": "150132",
        "especialidadIds": ["CARD", "ONCO", "GINEC", "PEDIA"],
        "seguroIds": ["RIMAC", "PACIFICO"],
        "grupoClinicaId": "GRP-05",
        "url": "https://www.angloamericana.com.pe/",
        "urlStaffMedico": "https://www.angloamericana.com.pe/nuestros-medicos"
    },
]

DOCTORS: List[Dict[str, Any]] = [
    {
        "doctorId": "DOC-001",
        "nombreCompleto": "Dr. Juan Carlos Pérez Salazar",
        "especialidadPrincipalId": "CARD",
        "subEspecialidadIds": ["CARD_INT"],
        "clinicaId": "CLIN-001",
        "photoUrl": "https://images.example/doc1.png",
    },
    {
        "doctorId": "DOC-002",
        "nombreCompleto": "Dra. María Isabel López García",
        "especialidadPrincipalId": "DERM",
        "subEspecialidadIds": ["DERM_COSM"],
        "clinicaId": "CLIN-002",
        "photoUrl": "https://images.example/doc2.png",
    },
    {
        "doctorId": "DOC-003",
        "nombreCompleto": "Dr. Roberto Fernández Castro",
        "especialidadPrincipalId": "NEURO",
        "subEspecialidadIds": ["NEURO_PED"],
        "clinicaId": "CLIN-001",
        "photoUrl": "https://images.example/doc3.png",
    },
    {
        "doctorId": "DOC-004",
        "nombreCompleto": "Dra. Carmen Rosa Villanueva",
        "especialidadPrincipalId": "GINEC",
        "subEspecialidadIds": [],
        "clinicaId": "CLIN-003",
        "photoUrl": "https://images.example/doc4.png",
    },
    {
        "doctorId": "DOC-005",
        "nombreCompleto": "Dr. Luis Alberto Torres Mendoza",
        "especialidadPrincipalId": "TRAUM",
        "subEspecialidadIds": ["TRAUM_DEPORT"],
        "clinicaId": "CLIN-004",
        "photoUrl": "https://images.example/doc5.png",
    },
    {
        "doctorId": "DOC-006",
        "nombreCompleto": "Dra. Patricia Morales Suárez",
        "especialidadPrincipalId": "ONCO",
        "subEspecialidadIds": [],
        "clinicaId": "CLIN-005",
        "photoUrl": "https://images.example/doc6.png",
    },
    {
        "doctorId": "DOC-007",
        "nombreCompleto": "Dr. Fernando Vega Rojas",
        "especialidadPrincipalId": "PEDIA",
        "subEspecialidadIds": [],
        "clinicaId": "CLIN-003",
        "photoUrl": "https://images.example/doc7.png",
    },
    {
        "doctorId": "DOC-008",
        "nombreCompleto": "Dra. Ana María Campos Rivera",
        "especialidadPrincipalId": "CARD",
        "subEspecialidadIds": ["CARD_ELECT"],
        "clinicaId": "CLIN-002",
        "photoUrl": "https://images.example/doc8.png",
    },
]

SPECIALTIES: List[Dict[str, Any]] = [
    {
        "especialidadId": "CARD",
        "nombre": "Cardiología",
        "descripcion": "Especialidad médica que se encarga del estudio, diagnóstico y tratamiento de las enfermedades del corazón y del aparato circulatorio"
    },
    {
        "especialidadId": "DERM",
        "nombre": "Dermatología",
        "descripcion": "Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades de la piel"
    },
    {
        "especialidadId": "NEURO",
        "nombre": "Neurología",
        "descripcion": "Especialidad médica que trata los trastornos del sistema nervioso"
    },
    {
        "especialidadId": "GINEC",
        "nombre": "Ginecología",
        "descripcion": "Especialidad médica que se ocupa de la salud del aparato reproductor femenino"
    },
    {
        "especialidadId": "TRAUM",
        "nombre": "Traumatología",
        "descripcion": "Especialidad médica que se dedica al estudio de las lesiones del aparato locomotor"
    },
    {
        "especialidadId": "ONCO",
        "nombre": "Oncología",
        "descripcion": "Especialidad médica que estudia y trata los tumores malignos"
    },
    {
        "especialidadId": "PEDIA",
        "nombre": "Pediatría",
        "descripcion": "Especialidad médica que estudia al niño y sus enfermedades"
    },
]

SUBSPECIALTIES: List[Dict[str, Any]] = [
    {
        "subEspecialidadId": "CARD_INT",
        "especialidadId": "CARD",
        "nombre": "Cardiología Intervencionista",
        "descripcion": "Subespecialidad que realiza procedimientos diagnósticos y terapéuticos invasivos"
    },
    {
        "subEspecialidadId": "CARD_ELECT",
        "especialidadId": "CARD",
        "nombre": "Electrofisiología Cardíaca",
        "descripcion": "Subespecialidad que estudia y trata los trastornos del ritmo cardíaco"
    },
    {
        "subEspecialidadId": "DERM_COSM",
        "especialidadId": "DERM",
        "nombre": "Dermatología Cosmética",
        "descripcion": "Subespecialidad enfocada en tratamientos estéticos de la piel"
    },
    {
        "subEspecialidadId": "NEURO_PED",
        "especialidadId": "NEURO",
        "nombre": "Neuropediatría",
        "descripcion": "Subespecialidad que trata enfermedades neurológicas en niños"
    },
    {
        "subEspecialidadId": "TRAUM_DEPORT",
        "especialidadId": "TRAUM",
        "nombre": "Traumatología Deportiva",
        "descripcion": "Subespecialidad que trata lesiones relacionadas con el deporte"
    },
]

INSURERS: List[Dict[str, Any]] = [
    {
        "seguroId": "RIMAC",
        "nombre": "RIMAC Seguros",
        "descripcion": "Compañía líder en seguros de salud en Perú"
    },
    {
        "seguroId": "PACIFICO",
        "nombre": "Pacífico Seguros",
        "descripcion": "Empresa de seguros con amplia cobertura nacional"
    },
    {
        "seguroId": "MAPFRE",
        "nombre": "MAPFRE Perú",
        "descripcion": "Aseguradora internacional con presencia en Perú"
    },
]

UBIGEOS: List[Dict[str, Any]] = [
    {
        "ubigeoId": "150101",
        "departamento": "Lima",
        "provincia": "Lima",
        "distritoId": "150101",
        "nombreDistrito": "San Isidro"
    },
    {
        "ubigeoId": "150108",
        "departamento": "Lima",
        "provincia": "Lima",
        "distritoId": "150108",
        "nombreDistrito": "Jesús María"
    },
    {
        "ubigeoId": "150132",
        "departamento": "Lima",
        "provincia": "Lima",
        "distritoId": "150132",
        "nombreDistrito": "Santiago de Surco"
    },
    {
        "ubigeoId": "150140",
        "departamento": "Lima",
        "provincia": "Lima",
        "distritoId": "150140",
        "nombreDistrito": "Miraflores"
    },
]
