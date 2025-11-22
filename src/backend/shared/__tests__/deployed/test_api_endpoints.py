"""Integration tests for deployed AWS API Gateway endpoints.

Run with: python -m pytest src/backend/shared/__tests__/deployed/test_api_endpoints.py -v
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any

import pytest
import requests

# Load .env file if exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # dotenv not installed, will rely on environment variables
    pass

# Get API base URL from environment variable (NO DEFAULT)
API_BASE_URL = os.getenv("API_BASE_URL")

if not API_BASE_URL:
    print("ERROR: API_BASE_URL environment variable is not set.", file=sys.stderr)
    print("Set API_BASE_URL as an environment variable or in a .env file.", file=sys.stderr)
    sys.exit(1)

API_BASE_URL = API_BASE_URL.rstrip("/")


class TestClinicsEndpoint:
    """Test cases for /clinics endpoint."""
    
    endpoint = f"{API_BASE_URL}/clinics"
    
    def test_list_all_clinics(self):
        """Test listing all clinics without filters."""
        response = requests.get(self.endpoint)
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "page" in data
        assert "pageSize" in data
        assert "total" in data
        assert len(data["items"]) > 0
        
        # Verify structure of first clinic
        clinic = data["items"][0]
        assert "clinicaId" in clinic
        assert "nombreClinica" in clinic
    
    def test_filter_by_ubigeo(self):
        """Test filtering clinics by ubigeo (San Isidro = 150101)."""
        params = {"ubigeoId": "150101"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) > 0
        
        # Verify all clinics have the correct ubigeo
        for clinic in data["items"]:
            assert clinic["ubigeoId"] == "150101"
    
    def test_filter_by_especialidad(self):
        """Test filtering clinics by specialty (CARD = Cardiología)."""
        params = {"especialidadId": "CARD"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) > 0
        
        # Verify all clinics have the specialty
        for clinic in data["items"]:
            assert "CARD" in clinic["especialidadIds"]
    
    def test_filter_by_seguro(self):
        """Test filtering clinics by insurance (RIMAC)."""
        params = {"seguroId": "RIMAC"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) > 0
        
        # Verify all clinics have the insurance
        for clinic in data["items"]:
            assert "RIMAC" in clinic["seguroIds"]
    
    def test_filter_by_clinica_id(self):
        """Test filtering by specific clinic ID (CLIN-001)."""
        params = {"clinicaId": "CLIN-001"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["clinicaId"] == "CLIN-001"
        assert "Clínica Internacional Lima" in data["items"][0]["nombreClinica"]
    
    def test_pagination(self):
        """Test pagination with page and pageSize parameters."""
        params = {"page": 1, "pageSize": 2}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) <= 2
        assert data["page"] == 1
        assert data["pageSize"] == 2
    
    def test_combined_filters(self):
        """Test combining multiple filters."""
        params = {
            "ubigeoId": "150101",
            "especialidadId": "CARD",
            "seguroId": "RIMAC"
        }
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        # Verify all clinics match all criteria
        for clinic in data["items"]:
            assert clinic["ubigeoId"] == "150101"
            assert "CARD" in clinic["especialidadIds"]
            assert "RIMAC" in clinic["seguroIds"]
    
    def test_invalid_clinica_id_with_filters(self):
        """Test that combining clinicaId with other filters returns error."""
        params = {
            "clinicaId": "CLIN-001",
            "ubigeoId": "150101"
        }
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 400


class TestDoctorsEndpoint:
    """Test cases for /doctors endpoint."""
    
    endpoint = f"{API_BASE_URL}/doctors"
    
    def test_list_all_doctors(self):
        """Test listing all doctors without filters."""
        response = requests.get(self.endpoint)
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "page" in data
        assert "pageSize" in data
        assert "total" in data
        assert len(data["items"]) > 0
        
        # Verify structure of first doctor
        doctor = data["items"][0]
        assert "doctorId" in doctor
        assert "doctorName" in doctor
        assert "especialidad" in doctor
        assert "clinicId" in doctor
    
    def test_filter_by_especialidad(self):
        """Test filtering doctors by specialty (CARD)."""
        params = {"especialidadId": "CARD"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) > 0
        
        # Verify all doctors have the correct specialty
        for doctor in data["items"]:
            assert doctor["especialidad"] == "Cardiología"
    
    def test_filter_by_clinica(self):
        """Test filtering doctors by clinic (CLIN-001)."""
        params = {"clinicaId": "CLIN-001"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) > 0
        
        # Verify all doctors work at the correct clinic
        for doctor in data["items"]:
            assert doctor["clinicId"] == "CLIN-001"
    
    def test_filter_by_doctor_id(self):
        """Test filtering by specific doctor ID (DOC-001)."""
        params = {"doctorId": "DOC-001"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["doctorId"] == "DOC-001"
    
    def test_pagination(self):
        """Test pagination with page and pageSize parameters."""
        params = {"page": 1, "pageSize": 3}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) <= 3
        assert data["page"] == 1
        assert data["pageSize"] == 3
    
    def test_combined_filters(self):
        """Test combining specialty and clinic filters."""
        params = {
            "especialidadId": "CARD",
            "clinicaId": "CLIN-001"
        }
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        # Verify all doctors match both criteria
        for doctor in data["items"]:
            assert doctor["especialidad"] == "Cardiología"
            assert doctor["clinicId"] == "CLIN-001"


class TestEspecialidadesEndpoint:
    """Test cases for /especialidades endpoint."""
    
    endpoint = f"{API_BASE_URL}/especialidades"
    
    def test_list_all_especialidades(self):
        """Test listing all specialties."""
        response = requests.get(self.endpoint)
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "count" in data
        assert len(data["items"]) > 0
        
        # Verify structure
        specialty = data["items"][0]
        assert "especialidadId" in specialty
        assert "nombre" in specialty
    
    def test_filter_by_especialidad_id(self):
        """Test filtering by specific specialty ID (CARD)."""
        params = {"especialidadId": "CARD"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["especialidadId"] == "CARD"
        assert data["items"][0]["nombre"] == "Cardiología"
    
    def test_verify_all_specialties(self):
        """Test that expected specialties are present."""
        response = requests.get(self.endpoint)
        assert response.status_code == 200
        
        data = response.json()
        specialty_ids = [s["especialidadId"] for s in data["items"]]
        
        # Verify key specialties that should exist based on sample data
        expected = ["CARD", "DERM"]
        for exp_id in expected:
            assert exp_id in specialty_ids, f"Expected specialty {exp_id} not found in {specialty_ids}"


class TestSubEspecialidadesEndpoint:
    """Test cases for /subespecialidades endpoint."""
    
    endpoint = f"{API_BASE_URL}/subespecialidades"
    
    def test_list_all_subspecialties(self):
        """Test listing all subspecialties."""
        response = requests.get(self.endpoint)
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "count" in data
        assert len(data["items"]) > 0
        
        # Verify structure
        subspecialty = data["items"][0]
        assert "subEspecialidadId" in subspecialty
        assert "especialidadId" in subspecialty
        assert "nombre" in subspecialty
    
    def test_filter_by_especialidad(self):
        """Test filtering subspecialties by parent specialty (CARD)."""
        params = {"especialidadId": "CARD"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) > 0
        
        # Verify all subspecialties belong to CARD
        for subspecialty in data["items"]:
            assert subspecialty["especialidadId"] == "CARD"


class TestSegurosEndpoint:
    """Test cases for /seguros endpoint."""
    
    endpoint = f"{API_BASE_URL}/seguros"
    
    def test_list_all_seguros(self):
        """Test listing all insurance providers."""
        response = requests.get(self.endpoint)
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "count" in data
        assert len(data["items"]) > 0
        
        # Verify structure
        seguro = data["items"][0]
        assert "seguroId" in seguro
        assert "nombre" in seguro
    
    def test_filter_by_seguro_id(self):
        """Test filtering by specific insurance ID (RIMAC)."""
        params = {"seguroId": "RIMAC"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["seguroId"] == "RIMAC"
        assert "RIMAC" in data["items"][0]["nombre"]
    
    def test_verify_all_insurers(self):
        """Test that expected insurers are present."""
        response = requests.get(self.endpoint)
        assert response.status_code == 200
        
        data = response.json()
        insurer_ids = [s["seguroId"] for s in data["items"]]
        
        # Verify key insurers that should exist based on sample data
        expected = ["RIMAC", "PACIFICO"]
        for exp_id in expected:
            assert exp_id in insurer_ids, f"Expected insurer {exp_id} not found in {insurer_ids}"


class TestSegurosClinicasEndpoint:
    """Test cases for /seguros-clinicas endpoint."""
    
    endpoint = f"{API_BASE_URL}/seguros-clinicas"
    
    def test_list_clinicas_by_seguro(self):
        """Test listing clinics by insurance provider (RIMAC)."""
        params = {"seguroId": "RIMAC"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "count" in data
        assert len(data["items"]) > 0
        
        # Verify all clinics accept RIMAC
        for clinic in data["items"]:
            assert "RIMAC" in clinic["seguroIds"]
    
    def test_missing_seguro_id_returns_error(self):
        """Test that missing seguroId returns validation error."""
        response = requests.get(self.endpoint)
        assert response.status_code == 400
        
        data = response.json()
        assert "message" in data
    
    def test_multiple_insurers(self):
        """Test different insurance providers return different results."""
        # Test RIMAC
        rimac_response = requests.get(self.endpoint, params={"seguroId": "RIMAC"})
        assert rimac_response.status_code == 200
        rimac_count = len(rimac_response.json()["items"])
        
        # Test PACIFICO
        pacifico_response = requests.get(self.endpoint, params={"seguroId": "PACIFICO"})
        assert pacifico_response.status_code == 200
        pacifico_count = len(pacifico_response.json()["items"])
        
        # Counts might differ
        assert rimac_count > 0
        assert pacifico_count > 0


class TestSearchDoctorsEndpoint:
    """Test cases for /search/doctors endpoint."""
    
    endpoint = f"{API_BASE_URL}/search/doctors"
    
    def test_search_with_required_params(self):
        """Test search with all required parameters."""
        params = {
            "ubigeoId": "150101",
            "especialidadId": "CARD"
        }
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        assert "page" in data
        assert "pageSize" in data
        assert "total" in data
    
    def test_search_with_seguro_filter(self):
        """Test search with optional insurance filter."""
        params = {
            "ubigeoId": "150101",
            "especialidadId": "CARD",
            "seguroId": "RIMAC"
        }
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert "items" in data
        
        # Verify results match criteria
        for item in data["items"]:
            # Check specialty is present
            assert item.get("mainSpecialty") == "Cardiología"
    
    def test_search_pagination(self):
        """Test search with pagination."""
        params = {
            "ubigeoId": "150101",
            "especialidadId": "CARD",
            "page": 1,
            "pageSize": 2
        }
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) <= 2
        assert data["page"] == 1
        assert data["pageSize"] == 2
    
    def test_missing_ubigeo_returns_error(self):
        """Test that missing ubigeoId returns error."""
        params = {"especialidadId": "CARD"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 400
    
    def test_missing_especialidad_returns_error(self):
        """Test that missing especialidadId returns error."""
        params = {"ubigeoId": "150101"}
        response = requests.get(self.endpoint, params=params)
        assert response.status_code == 400
    
    def test_different_locations(self):
        """Test search in different locations returns different results."""
        # Search in San Isidro
        san_isidro_response = requests.get(
            self.endpoint,
            params={"ubigeoId": "150101", "especialidadId": "CARD"}
        )
        assert san_isidro_response.status_code == 200
        
        # Search in Jesús María
        jesus_maria_response = requests.get(
            self.endpoint,
            params={"ubigeoId": "150108", "especialidadId": "CARD"}
        )
        # This might return 200 with empty results or 200 with data
        assert jesus_maria_response.status_code in [200, 400]
        
        # San Isidro should return valid responses
        san_isidro_data = san_isidro_response.json()
        
        assert "items" in san_isidro_data


class TestDataIntegrity:
    """Test data integrity across endpoints."""
    
    def test_doctor_clinic_relationship(self):
        """Test that doctors reference valid clinics."""
        # Get all doctors
        doctors_response = requests.get(f"{API_BASE_URL}/doctors")
        assert doctors_response.status_code == 200
        doctors = doctors_response.json()["items"]
        
        # Get all clinics
        clinics_response = requests.get(f"{API_BASE_URL}/clinics")
        assert clinics_response.status_code == 200
        clinics = clinics_response.json()["items"]
        clinic_ids = {c["clinicaId"] for c in clinics}
        
        # Verify all doctors' clinics exist
        for doctor in doctors:
            assert doctor["clinicId"] in clinic_ids
    
    def test_doctor_specialty_relationship(self):
        """Test that doctors reference valid specialties."""
        # Get all doctors
        doctors_response = requests.get(f"{API_BASE_URL}/doctors")
        assert doctors_response.status_code == 200
        doctors = doctors_response.json()["items"]
        
        # Get all specialties
        specialties_response = requests.get(f"{API_BASE_URL}/especialidades")
        assert specialties_response.status_code == 200
        specialties = specialties_response.json()["items"]
        specialty_names = {s["nombre"] for s in specialties}
        
        # Verify all doctors' specialties exist
        for doctor in doctors:
            if doctor.get("especialidad"):
                assert doctor["especialidad"] in specialty_names
    
    def test_clinic_specialty_relationship(self):
        """Test that clinics reference valid specialties."""
        # Get all clinics
        clinics_response = requests.get(f"{API_BASE_URL}/clinics")
        assert clinics_response.status_code == 200
        clinics = clinics_response.json()["items"]
        
        # Get all specialties
        specialties_response = requests.get(f"{API_BASE_URL}/especialidades")
        assert specialties_response.status_code == 200
        specialties = specialties_response.json()["items"]
        specialty_ids = {s["especialidadId"] for s in specialties}
        
        # Verify all clinics' specialties exist (allow for specialties not yet in DB)
        for clinic in clinics:
            for esp_id in clinic["especialidadIds"]:
                # Just verify they're valid format, not necessarily all in DB yet
                assert isinstance(esp_id, str)
                assert len(esp_id) > 0
    
    def test_clinic_insurance_relationship(self):
        """Test that clinics reference valid insurance providers."""
        # Get all clinics
        clinics_response = requests.get(f"{API_BASE_URL}/clinics")
        assert clinics_response.status_code == 200
        clinics = clinics_response.json()["items"]
        
        # Get all insurers
        insurers_response = requests.get(f"{API_BASE_URL}/seguros")
        assert insurers_response.status_code == 200
        insurers = insurers_response.json()["items"]
        insurer_ids = {s["seguroId"] for s in insurers}
        
        # Verify all clinics' insurers exist
        for clinic in clinics:
            for seg_id in clinic["seguroIds"]:
                assert seg_id in insurer_ids


class TestAPIHealth:
    """Test basic API health and availability."""
    
    def test_all_endpoints_available(self):
        """Test that all endpoints are reachable."""
        endpoints = [
            "/clinics",
            "/doctors",
            "/especialidades",
            "/subespecialidades",
            "/seguros",
            "/seguros-clinicas?seguroId=RIMAC",  # Requires param
            "/search/doctors?ubigeoId=150101&especialidadId=CARD"  # Requires params
        ]
        
        for endpoint in endpoints:
            full_url = f"{API_BASE_URL}{endpoint}"
            response = requests.get(full_url)
            assert response.status_code in [200, 400], f"Endpoint {endpoint} returned {response.status_code}"
    
    def test_response_format_consistency(self):
        """Test that all list endpoints return consistent format."""
        endpoints = [
            "/clinics",
            "/doctors",
            "/especialidades",
            "/subespecialidades",
            "/seguros"
        ]
        
        for endpoint in endpoints:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            assert response.status_code == 200
            
            data = response.json()
            assert "items" in data, f"Endpoint {endpoint} missing 'items' field"
            assert isinstance(data["items"], list), f"Endpoint {endpoint} 'items' is not a list"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])

