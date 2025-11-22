"""Repository tests built on the shared mock dataset."""
from shared.repositories.clinics_repo import ClinicsRepository
from shared.repositories.doctors_repo import DoctorsRepository
from shared.repositories.insurers_repo import InsurersRepository
from shared.repositories.specialties_repo import (
    SpecialtiesRepository,
    SubSpecialtiesRepository,
)
from shared.repositories.ubigeo_repo import UbigeoRepository


# Clinics -----------------------------------------------------------------
def test_list_clinics_filters_by_ubigeo():
    repo = ClinicsRepository()

    results = repo.list_clinics({"ubigeoId": "150101"})

    assert [clinic["clinicaId"] for clinic in results] == ["CLIN-001"]


def test_list_clinics_filters_by_multiple_fields():
    repo = ClinicsRepository()

    results = repo.list_clinics({"seguroId": "RIMAC", "especialidadId": "DERM"})

    assert [clinic["clinicaId"] for clinic in results] == ["CLIN-002"]


def test_get_clinic_returns_none_for_unknown_id():
    repo = ClinicsRepository()

    assert repo.get_clinic("UNKNOWN") is None


# Doctors -----------------------------------------------------------------
def test_list_doctors_filters_by_clinic():
    repo = DoctorsRepository()

    results = repo.list_doctors({"clinicaId": "CLIN-002"})

    assert [doctor["doctorId"] for doctor in results] == ["DOC-002"]


def test_list_doctors_filters_by_specialty():
    repo = DoctorsRepository()

    results = repo.list_doctors({"especialidadId": "CARD"})

    assert [doctor["doctorId"] for doctor in results] == ["DOC-001"]


# Specialties --------------------------------------------------------------
def test_list_specialties_returns_specific_item():
    repo = SpecialtiesRepository()

    results = repo.list_specialties("CARD")

    assert len(results) == 1
    assert results[0]["nombre"] == "Cardiología"


def test_list_subspecialties_by_parent():
    repo = SubSpecialtiesRepository()

    results = repo.list_subspecialties("CARD")

    assert [item["subEspecialidadId"] for item in results] == ["CARD_INT"]


# Insurers -----------------------------------------------------------------
def test_list_insurers_filters_by_id():
    repo = InsurersRepository()

    results = repo.list_insurers("RIMAC")

    assert [insurer["nombre"] for insurer in results] == ["RIMAC Seguros"]


def test_list_clinics_by_insurer_returns_joined_data():
    repo = InsurersRepository()

    results = repo.list_clinics_by_insurer("PACIFICO")

    assert [clinic["clinicaId"] for clinic in results] == ["CLIN-001"]


# Ubigeo -------------------------------------------------------------------
def test_ubigeo_exists_and_get_name():
    repo = UbigeoRepository()

    assert repo.exists("150101") is True
    assert repo.exists("000000") is False
    assert repo.get_name("150132") == "Santiago de Surco"
    assert repo.get_name("999999") is None

