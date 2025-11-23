"""Search service for doctor cards."""
from __future__ import annotations

from typing import Dict, List

from shared.exceptions import ValidationError
from dto import SearchDoctorsQueryDTO
from repositories.clinics_repo import ClinicsRepository
from repositories.doctors_repo import DoctorsRepository
from repositories.insurers_repo import InsurersRepository
from repositories.specialties_repo import SpecialtiesRepository
from repositories.ubigeo_repo import UbigeoRepository


class SearchService:
    def __init__(
        self,
        doctors_repo: DoctorsRepository | None = None,
        clinics_repo: ClinicsRepository | None = None,
        specialties_repo: SpecialtiesRepository | None = None,
        insurers_repo: InsurersRepository | None = None,
        ubigeo_repo: UbigeoRepository | None = None,
    ):
        self._doctors_repo = doctors_repo or DoctorsRepository()
        self._clinics_repo = clinics_repo or ClinicsRepository()
        self._specialties_repo = specialties_repo or SpecialtiesRepository()
        self._insurers_repo = insurers_repo or InsurersRepository()
        self._ubigeo_repo = ubigeo_repo or UbigeoRepository()

    def search_doctors(self, dto: SearchDoctorsQueryDTO) -> Dict[str, object]:
        # Validate ubigeo if provided
        if dto.ubigeo_id and not self._ubigeo_repo.exists(dto.ubigeo_id):
            raise ValidationError("Invalid ubigeoId")

        # Step 1: Get clinics (filter by ubigeo and/or seguro if provided)
        clinic_filters = {}
        if dto.ubigeo_id:
            clinic_filters["ubigeoId"] = dto.ubigeo_id
        if dto.seguro_id:
            clinic_filters["seguroId"] = dto.seguro_id
        
        # If we have clinic filters, apply them; otherwise get all clinics
        if clinic_filters:
            clinics = self._clinics_repo.list_clinics(clinic_filters)
            clinic_ids = {clinic["clinicaId"] for clinic in clinics}
        else:
            # No clinic filters - we'll filter by doctors only
            clinics = self._clinics_repo.list_clinics({})
            clinic_ids = None  # Will skip clinic filtering

        # Step 2: Get doctors (filter by especialidad and/or rimacEnsured if provided)
        doctor_filters = {}
        if dto.especialidad_id:
            doctor_filters["especialidadId"] = dto.especialidad_id
        if dto.rimac_ensured is not None:
            doctor_filters["rimacEnsured"] = dto.rimac_ensured
        
        doctors = self._doctors_repo.list_doctors(doctor_filters)
        
        # Step 3: Filter doctors whose clinicaIds intersect with clinic_ids (if clinic filters were applied)
        if clinic_ids is not None:
            filtered_doctors = []
            for doctor in doctors:
                if "clinicaId" in doctor and doctor["clinicaId"] in clinic_ids:
                    filtered_doctors.append(doctor)
                elif "clinicaIds" in doctor:
                    clinica_ids_list = doctor["clinicaIds"] if isinstance(doctor["clinicaIds"], list) else [doctor["clinicaIds"]]
                    if any(cid in clinic_ids for cid in clinica_ids_list):
                        filtered_doctors.append(doctor)
            doctors = filtered_doctors
        
        total = len(doctors)
        start = (dto.page - 1) * dto.page_size
        end = start + dto.page_size
        paged = doctors[start:end]

        # Get specialty name if filtering by specialty
        specialty_name = None
        if dto.especialidad_id:
            specialty = self._specialties_repo.list_specialties(dto.especialidad_id)
            specialty_name = specialty[0]["nombre"] if specialty else None
        
        insurer_names = {ins["seguroId"]: ins["nombre"] for ins in self._insurers_repo.list_insurers(None)}
        clinic_lookup = {clinic["clinicaId"]: clinic for clinic in clinics}

        cards = [
            self._to_doctor_card(doctor, clinic_lookup, specialty_name, insurer_names)
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
        insurer_names: Dict[str, str],
    ) -> Dict[str, object]:
        # Handle both clinicaId (old) and clinicaIds (new array format)
        clinica_id = None
        if "clinicaId" in doctor:
            clinica_id = doctor["clinicaId"]
        elif "clinicaIds" in doctor and doctor["clinicaIds"]:
            clinica_id = doctor["clinicaIds"][0] if isinstance(doctor["clinicaIds"], list) else doctor["clinicaIds"]
        
        clinic = clinic_lookup.get(clinica_id)
        
        # Build seguros list
        seguros = []
        if clinic:
            for seguro_id in clinic.get("seguroIds", []):
                seguros.append({
                    "seguroId": seguro_id,
                    "nombre": insurer_names.get(seguro_id, seguro_id),
                })
        
        # Handle both nombreCompleto and separated name fields
        doctor_name = doctor.get("nombreCompleto")
        if not doctor_name:
            nombres = doctor.get("nombres", "")
            apellido_paterno = doctor.get("apellidoPaterno", "")
            apellido_materno = doctor.get("apellidoMaterno", "")
            doctor_name = f"{nombres} {apellido_paterno} {apellido_materno}".strip()
        
        # Handle both ubicacion and direccion
        clinic_address = None
        if clinic:
            clinic_address = clinic.get("ubicacion") or clinic.get("direccion", "")
        
        return {
            "doctorId": doctor["doctorId"],
            "doctorName": doctor_name,
            "photoUrl": doctor.get("photoUrl") or doctor.get("fotoUrl"),
            "mainSpecialty": specialty_name,
            "clinicId": clinic["clinicaId"] if clinic else None,
            "clinicName": clinic["nombreClinica"] if clinic else None,
            "clinicAddress": clinic_address,
            "seguros": seguros,
        }

    @staticmethod
    def _empty_payload(dto: SearchDoctorsQueryDTO) -> Dict[str, object]:
        return {"items": [], "page": dto.page, "pageSize": dto.page_size, "total": 0}
