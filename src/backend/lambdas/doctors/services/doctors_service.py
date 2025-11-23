"""Service logic for Doctors API."""
from __future__ import annotations

from typing import Dict, List

from shared.exceptions import ValidationError
from dto import DoctorsQueryDTO
from repositories.clinics_repo import ClinicsRepository
from repositories.doctors_repo import DoctorsRepository
from repositories.specialties_repo import SpecialtiesRepository, SubSpecialtiesRepository


class DoctorsService:
    def __init__(
        self,
        doctors_repo: DoctorsRepository | None = None,
        clinics_repo: ClinicsRepository | None = None,
        specialties_repo: SpecialtiesRepository | None = None,
        subs_repo: SubSpecialtiesRepository | None = None,
    ):
        self._doctors_repo = doctors_repo or DoctorsRepository()
        self._clinics_repo = clinics_repo or ClinicsRepository()
        self._specialties_repo = specialties_repo or SpecialtiesRepository()
        self._subs_repo = subs_repo or SubSpecialtiesRepository()

    def list_doctors(self, dto: DoctorsQueryDTO) -> Dict[str, object]:
        filters = {
            "especialidadId": dto.especialidad_id,
            "clinicaId": dto.clinica_id,
            "doctorId": dto.doctor_id,
            "rimacEnsured": dto.rimac_ensured,
        }
        doctors = self._doctors_repo.list_doctors(filters)
        total = len(doctors)
        start = (dto.page - 1) * dto.page_size
        end = start + dto.page_size
        paged = doctors[start:end]
        items = [self._to_response_model(doctor) for doctor in paged]
        if dto.doctor_id and not items:
            raise ValidationError("Doctor not found")
        return {
            "items": items,
            "page": dto.page,
            "pageSize": dto.page_size,
            "total": total,
        }

    def _to_response_model(self, doctor: Dict[str, object]) -> Dict[str, object]:
        clinic = self._clinics_repo.get_clinic(doctor["clinicaId"])
        specialty = self._specialties_repo.list_specialties(doctor["especialidadPrincipalId"])
        subs = self._subs_repo.list_subspecialties(doctor["especialidadPrincipalId"])
        return {
            "doctorId": doctor["doctorId"],
            "doctorName": doctor["nombreCompleto"],
            "clinicId": clinic["clinicaId"] if clinic else None,
            "clinicName": clinic["nombreClinica"] if clinic else None,
            "especialidad": specialty[0]["nombre"] if specialty else None,
            "subEspecialidades": [item["nombre"] for item in subs],
            "photoUrl": doctor.get("photoUrl"),
        }
