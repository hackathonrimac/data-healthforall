"""Search service for doctor cards."""
from __future__ import annotations

from typing import Dict, List

from shared.exceptions import ValidationError
from dto import SearchDoctorsQueryDTO
from repositories.clinics_repo import ClinicsRepository
from repositories.doctors_repo import DoctorsRepository
from repositories.insurers_repo import InsurersRepository
from repositories.specialties_repo import SpecialtiesRepository, SubSpecialtiesRepository
from repositories.ubigeo_repo import UbigeoRepository


class SearchService:
    def __init__(
        self,
        doctors_repo: DoctorsRepository | None = None,
        clinics_repo: ClinicsRepository | None = None,
        specialties_repo: SpecialtiesRepository | None = None,
        subs_repo: SubSpecialtiesRepository | None = None,
        insurers_repo: InsurersRepository | None = None,
        ubigeo_repo: UbigeoRepository | None = None,
    ):
        self._doctors_repo = doctors_repo or DoctorsRepository()
        self._clinics_repo = clinics_repo or ClinicsRepository()
        self._specialties_repo = specialties_repo or SpecialtiesRepository()
        self._subs_repo = subs_repo or SubSpecialtiesRepository()
        self._insurers_repo = insurers_repo or InsurersRepository()
        self._ubigeo_repo = ubigeo_repo or UbigeoRepository()

    def search_doctors(self, dto: SearchDoctorsQueryDTO) -> Dict[str, object]:
        if not self._ubigeo_repo.exists(dto.ubigeo_id):
            raise ValidationError("Invalid ubigeoId")

        clinics = self._clinics_repo.list_clinics(
            {
                "ubigeoId": dto.ubigeo_id,
                "especialidadId": dto.especialidad_id,
                "seguroId": dto.seguro_id,
            }
        )
        clinic_ids = {clinic["clinicaId"] for clinic in clinics}
        if not clinic_ids:
            return self._empty_payload(dto)

        doctors = self._doctors_repo.list_doctors({
            "especialidadId": dto.especialidad_id,
            "rimacEnsured": dto.rimac_ensured,
        })
        doctors = [doctor for doctor in doctors if doctor["clinicaId"] in clinic_ids]
        total = len(doctors)
        start = (dto.page - 1) * dto.page_size
        end = start + dto.page_size
        paged = doctors[start:end]

        specialty = self._specialties_repo.list_specialties(dto.especialidad_id)
        specialty_name = specialty[0]["nombre"] if specialty else None
        sub_map = {sub["subEspecialidadId"]: sub["nombre"] for sub in self._subs_repo.list_subspecialties(dto.especialidad_id)}
        insurer_names = {ins["seguroId"]: ins["nombre"] for ins in self._insurers_repo.list_insurers(None)}
        clinic_lookup = {clinic["clinicaId"]: clinic for clinic in clinics}

        cards = [
            self._to_doctor_card(doctor, clinic_lookup, specialty_name, sub_map, insurer_names)
            for doctor in paged
        ]

        return {
            "items": cards,
            "page": dto.page,
            "pageSize": dto.page_size,
            "total": total,
        }

    def _to_doctor_card(
        self,
        doctor: Dict[str, object],
        clinic_lookup: Dict[str, Dict[str, object]],
        specialty_name: str | None,
        sub_map: Dict[str, str],
        insurer_names: Dict[str, str],
    ) -> Dict[str, object]:
        clinic = clinic_lookup.get(doctor["clinicaId"])
        seguros = []
        if clinic:
            for seguro_id in clinic.get("seguroIds", []):
                seguros.append({
                    "seguroId": seguro_id,
                    "nombre": insurer_names.get(seguro_id, seguro_id),
                })
        return {
            "doctorId": doctor["doctorId"],
            "doctorName": doctor["nombreCompleto"],
            "photoUrl": doctor.get("photoUrl"),
            "mainSpecialty": specialty_name,
            "subSpecialties": [sub_map.get(sub_id) for sub_id in doctor.get("subEspecialidadIds", []) if sub_map.get(sub_id)],
            "clinicId": clinic["clinicaId"] if clinic else None,
            "clinicName": clinic["nombreClinica"] if clinic else None,
            "clinicAddress": clinic["ubicacion"] if clinic else None,
            "seguros": seguros,
        }

    @staticmethod
    def _empty_payload(dto: SearchDoctorsQueryDTO) -> Dict[str, object]:
        return {"items": [], "page": dto.page, "pageSize": dto.page_size, "total": 0}
