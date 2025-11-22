"""Simple in-memory dataset so Lambdas can run locally without AWS."""
from __future__ import annotations

from typing import Dict, List, Any

CLINICS: List[Dict[str, Any]] = [
    {
        "ClinicaId": "CLIN-001",
        "NombreClinica": "Clínica Internacional Lima",
        "Ubicacion": "Av. Javier Prado Este 123, San Isidro",
        "UbigeoId": "150101",
        "EspecialidadIds": ["CARD", "NEURO", "TRAUM"],
        "SeguroIds": ["RIMAC", "PACIFICO"],
        "GrupoClinicaId": "GRP-01",
        "URL": "https://clinicainternacional.com.pe/",
        "URLStaffMedico": "https://clinicainternacional.com.pe/doctores"
    },
    {
        "ClinicaId": "CLIN-002",
        "NombreClinica": "Clínica Ricardo Palma",
        "Ubicacion": "Av. Javier Prado Este 1066, San Isidro",
        "UbigeoId": "150101",
        "EspecialidadIds": ["DERM", "CARD", "ONCO"],
        "SeguroIds": ["RIMAC", "PACIFICO", "MAPFRE"],
        "GrupoClinicaId": "GRP-02",
        "URL": "https://www.ricardopalma.com.pe/",
        "URLStaffMedico": "https://www.ricardopalma.com.pe/medicos"
    },
    {
        "ClinicaId": "CLIN-003",
        "NombreClinica": "Clínica San Felipe",
        "Ubicacion": "Av. Gregorio Escobedo 650, Jesús María",
        "UbigeoId": "150108",
        "EspecialidadIds": ["GINEC", "PEDIA", "CARD"],
        "SeguroIds": ["RIMAC"],
        "GrupoClinicaId": "GRP-03",
        "URL": "https://www.clinicasanfelipe.com/",
        "URLStaffMedico": "https://www.clinicasanfelipe.com/staff"
    },
    {
        "ClinicaId": "CLIN-004",
        "NombreClinica": "Clínica Javier Prado",
        "Ubicacion": "Av. Javier Prado Este 499, San Isidro",
        "UbigeoId": "150101",
        "EspecialidadIds": ["TRAUM", "NEURO", "CARD"],
        "SeguroIds": ["PACIFICO", "MAPFRE"],
        "GrupoClinicaId": "GRP-04",
        "URL": "https://www.clinicajavierprado.com.pe/",
        "URLStaffMedico": "https://www.clinicajavierprado.com.pe/medicos"
    },
    {
        "ClinicaId": "CLIN-005",
        "NombreClinica": "Clínica Anglo Americana",
        "Ubicacion": "Av. Alfredo Salazar 350, San Isidro",
        "UbigeoId": "150132",
        "EspecialidadIds": ["CARD", "ONCO", "GINEC", "PEDIA"],
        "SeguroIds": ["RIMAC", "PACIFICO"],
        "GrupoClinicaId": "GRP-05",
        "URL": "https://www.angloamericana.com.pe/",
        "URLStaffMedico": "https://www.angloamericana.com.pe/nuestros-medicos"
    },
]

DOCTORS: List[Dict[str, Any]] = [
    {
        "DoctorId": "DOC-001",
        "NombreCompleto": "Dr. Juan Carlos Pérez Salazar",
        "EspecialidadPrincipalId": "CARD",
        "SubEspecialidadIds": ["CARD_INT"],
        "ClinicaId": "CLIN-001",
        "PhotoUrl": "https://images.example/doc1.png",
    },
    {
        "DoctorId": "DOC-002",
        "NombreCompleto": "Dra. María Isabel López García",
        "EspecialidadPrincipalId": "DERM",
        "SubEspecialidadIds": ["DERM_COSM"],
        "ClinicaId": "CLIN-002",
        "PhotoUrl": "https://images.example/doc2.png",
    },
    {
        "DoctorId": "DOC-003",
        "NombreCompleto": "Dr. Roberto Fernández Castro",
        "EspecialidadPrincipalId": "NEURO",
        "SubEspecialidadIds": ["NEURO_PED"],
        "ClinicaId": "CLIN-001",
        "PhotoUrl": "https://images.example/doc3.png",
    },
    {
        "DoctorId": "DOC-004",
        "NombreCompleto": "Dra. Carmen Rosa Villanueva",
        "EspecialidadPrincipalId": "GINEC",
        "SubEspecialidadIds": [],
        "ClinicaId": "CLIN-003",
        "PhotoUrl": "https://images.example/doc4.png",
    },
    {
        "DoctorId": "DOC-005",
        "NombreCompleto": "Dr. Luis Alberto Torres Mendoza",
        "EspecialidadPrincipalId": "TRAUM",
        "SubEspecialidadIds": ["TRAUM_DEPORT"],
        "ClinicaId": "CLIN-004",
        "PhotoUrl": "https://images.example/doc5.png",
    },
    {
        "DoctorId": "DOC-006",
        "NombreCompleto": "Dra. Patricia Morales Suárez",
        "EspecialidadPrincipalId": "ONCO",
        "SubEspecialidadIds": [],
        "ClinicaId": "CLIN-005",
        "PhotoUrl": "https://images.example/doc6.png",
    },
    {
        "DoctorId": "DOC-007",
        "NombreCompleto": "Dr. Fernando Vega Rojas",
        "EspecialidadPrincipalId": "PEDIA",
        "SubEspecialidadIds": [],
        "ClinicaId": "CLIN-003",
        "PhotoUrl": "https://images.example/doc7.png",
    },
    {
        "DoctorId": "DOC-008",
        "NombreCompleto": "Dra. Ana María Campos Rivera",
        "EspecialidadPrincipalId": "CARD",
        "SubEspecialidadIds": ["CARD_ELECT"],
        "ClinicaId": "CLIN-002",
        "PhotoUrl": "https://images.example/doc8.png",
    },
]

SPECIALTIES: List[Dict[str, Any]] = [
    {
        "EspecialidadId": "CARD",
        "Nombre": "Cardiología",
        "Descripcion": "Especialidad médica que se encarga del estudio, diagnóstico y tratamiento de las enfermedades del corazón y del aparato circulatorio"
    },
    {
        "EspecialidadId": "DERM",
        "Nombre": "Dermatología",
        "Descripcion": "Especialidad médica que se encarga del diagnóstico y tratamiento de las enfermedades de la piel"
    },
    {
        "EspecialidadId": "NEURO",
        "Nombre": "Neurología",
        "Descripcion": "Especialidad médica que trata los trastornos del sistema nervioso"
    },
    {
        "EspecialidadId": "GINEC",
        "Nombre": "Ginecología",
        "Descripcion": "Especialidad médica que se ocupa de la salud del aparato reproductor femenino"
    },
    {
        "EspecialidadId": "TRAUM",
        "Nombre": "Traumatología",
        "Descripcion": "Especialidad médica que se dedica al estudio de las lesiones del aparato locomotor"
    },
    {
        "EspecialidadId": "ONCO",
        "Nombre": "Oncología",
        "Descripcion": "Especialidad médica que estudia y trata los tumores malignos"
    },
    {
        "EspecialidadId": "PEDIA",
        "Nombre": "Pediatría",
        "Descripcion": "Especialidad médica que estudia al niño y sus enfermedades"
    },
]

SUBSPECIALTIES: List[Dict[str, Any]] = [
    {
        "SubEspecialidadId": "CARD_INT",
        "EspecialidadId": "CARD",
        "Nombre": "Cardiología Intervencionista",
        "Descripcion": "Subespecialidad que realiza procedimientos diagnósticos y terapéuticos invasivos"
    },
    {
        "SubEspecialidadId": "CARD_ELECT",
        "EspecialidadId": "CARD",
        "Nombre": "Electrofisiología Cardíaca",
        "Descripcion": "Subespecialidad que estudia y trata los trastornos del ritmo cardíaco"
    },
    {
        "SubEspecialidadId": "DERM_COSM",
        "EspecialidadId": "DERM",
        "Nombre": "Dermatología Cosmética",
        "Descripcion": "Subespecialidad enfocada en tratamientos estéticos de la piel"
    },
    {
        "SubEspecialidadId": "NEURO_PED",
        "EspecialidadId": "NEURO",
        "Nombre": "Neuropediatría",
        "Descripcion": "Subespecialidad que trata enfermedades neurológicas en niños"
    },
    {
        "SubEspecialidadId": "TRAUM_DEPORT",
        "EspecialidadId": "TRAUM",
        "Nombre": "Traumatología Deportiva",
        "Descripcion": "Subespecialidad que trata lesiones relacionadas con el deporte"
    },
]

INSURERS: List[Dict[str, Any]] = [
    {
        "SeguroId": "RIMAC",
        "Nombre": "RIMAC Seguros",
        "Descripcion": "Compañía líder en seguros de salud en Perú"
    },
    {
        "SeguroId": "PACIFICO",
        "Nombre": "Pacífico Seguros",
        "Descripcion": "Empresa de seguros con amplia cobertura nacional"
    },
    {
        "SeguroId": "MAPFRE",
        "Nombre": "MAPFRE Perú",
        "Descripcion": "Aseguradora internacional con presencia en Perú"
    },
]

UBIGEOS: List[Dict[str, Any]] = [
    {
        "UbigeoId": "150101",
        "Departamento": "Lima",
        "Provincia": "Lima",
        "DistritoId": "150101",
        "NombreDistrito": "San Isidro"
    },
    {
        "UbigeoId": "150108",
        "Departamento": "Lima",
        "Provincia": "Lima",
        "DistritoId": "150108",
        "NombreDistrito": "Jesús María"
    },
    {
        "UbigeoId": "150132",
        "Departamento": "Lima",
        "Provincia": "Lima",
        "DistritoId": "150132",
        "NombreDistrito": "Santiago de Surco"
    },
    {
        "UbigeoId": "150140",
        "Departamento": "Lima",
        "Provincia": "Lima",
        "DistritoId": "150140",
        "NombreDistrito": "Miraflores"
    },
]
