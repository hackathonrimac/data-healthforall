### Backend architecture overview

This backend supports health search and reference data using **only AWS services** and **one REST API + one Lambda per API group (domain)**.

Instead of a single `search` API, you will have **multiple domain APIs**, each with its **own REST API Gateway + Lambda**:

- **Clinics API** → API Gateway `ClinicsApi` + Lambda `clinics`.
- **Doctors API** → API Gateway `DoctorsApi` + Lambda `doctors`.
- **Especialidades API** → API Gateway `EspecialidadesApi` + Lambda `especialidades`.
- **Seguros API** → API Gateway `SegurosApi` + Lambda `seguros`.
- **(Optional) Search API** → API Gateway `SearchApi` + Lambda `search` (cross-domain "search near me").

---

### Populate DynamoDB tables with test data

After deploying your backend, populate the DynamoDB tables with mock data:

```bash
# Populate all tables in dev environment
python3 scripts/populate_tables.py --env dev

# Populate all tables in prod environment
python3 scripts/populate_tables.py --env prod

# Populate specific tables only
python3 scripts/populate_tables.py --env dev --tables doctors clinics

# Use different AWS region
python3 scripts/populate_tables.py --env dev --region us-west-2
```

**Available options:**
- `--env`: Environment (dev or prod). Default: dev
- `--region`: AWS region. Default: us-east-1
- `--tables`: Specific tables to populate (doctors, clinics, especialidades, subespecialidades, seguros, ubigeo, all). Default: all

**Note:** The script always uses the `hackathon` AWS profile.

**Sample data includes:**
- 5 clinics across different districts in Lima
- 8 doctors with various specialties
- 7 medical specialties
- 5 subspecialties
- 3 insurance providers
- 4 ubigeo locations (districts)

---

### What you actually need to build for this API

- **API surface (groups and example endpoints)**
  - **Clinics API (Lambda `clinics`)**
    - `GET /clinics` → list clinics (filter by `ubigeoId`, `especialidadId`, `seguroId`, and optionally `clinicaId` for detail).
  - **Doctors API (Lambda `doctors`)**
    - `GET /doctors` → list doctors (filter by `especialidadId`, `clinicaId`, and optionally `doctorId` for detail).
  - **Especialidades API (Lambda `especialidades`)**
    - `GET /especialidades` → list specialties (optionally filter by `especialidadId`).
    - `GET /subespecialidades` → list subspecialties (filter by `especialidadId`).
  - **Seguros API (Lambda `seguros`)**
    - `GET /seguros` → list insurers (optionally filter by `seguroId`).
    - `GET /seguros-clinicas` → clinics covered by an insurer (filter by `seguroId`).
  - **(Optional) Search API (Lambda `search`)**
    - `GET /search/doctors` → “doctor cards near me” (doctor + specialties + clinic info for UI carousels).

- **Lambda code**
  - **One folder per API group**, each with:
    - `handler.py` as the AWS Lambda entrypoint (no internal router, just one REST endpoint per group).
    - `dto.py` with request/response DTOs and validation.
    - `services/*.py` with the core domain logic.
    - `repositories/*.py` to read from DynamoDB tables.

- **AWS infrastructure (defined in `aws/backend.yml`)**
  - One REST API Gateway **per group** (`ClinicsApi`, `DoctorsApi`, `EspecialidadesApi`, `SegurosApi`, optional `SearchApi`).
  - Each REST API exposes a single resource path (e.g. `/clinics`, `/doctors`) integrated with its Lambda.
  - DynamoDB tables: `Doctor`, `Clinicas`, `Especialidad`, `SubEspecialidad`, `Seguros`, `Ubigeo`.
  - IAM roles/policies so each Lambda can read from only the tables it needs (principle of least privilege).

- **Deployment plumbing**
  - `scripts/package_lambdas.sh` to build & zip **all** Lambda codes.
  - `scripts/deploy_backend.sh` to run `aws cloudformation deploy` with the right parameters.

---

### Endpoints (high-level contracts by group)

- **Clinics API (`ClinicsApi`, path `/clinics`)**
  - **GET `/clinics`**
    - Query params: `ubigeoId?`, `especialidadId?`, `seguroId?`, `clinicaId?`, `page?`, `pageSize?`.
    - If `clinicaId` is present → return detail for that clinic.
    - Otherwise → return a paginated list of clinics with basic info.

- **Doctors API (`DoctorsApi`, path `/doctors`)**
  - **GET `/doctors`**
    - Query params: `especialidadId?`, `clinicaId?`, `doctorId?`, `page?`, `pageSize?`.
    - If `doctorId` is present → return detail for that doctor.
    - Otherwise → return a paginated list of doctors.

- **Especialidades API (`EspecialidadesApi`, paths `/especialidades`, `/subespecialidades`)**
  - **GET `/especialidades`**
    - Query params: `especialidadId?`.
    - Returns all specialties or a specific one.
  - **GET `/subespecialidades`**
    - Query params: `especialidadId` (to filter subspecialties by parent specialty).

- **Seguros API (`SegurosApi`, paths `/seguros`, `/seguros-clinicas`)**
  - **GET `/seguros`**
    - Query params: `seguroId?`.
    - Returns all insurers or a specific one.
  - **GET `/seguros-clinicas`**
    - Query params: `seguroId` (required).
    - Returns clinics covered by a given insurer.

- **(Optional) Search API (`SearchApi`, path `/search/doctors`)**
  - **GET `/search/doctors`**
    - Query params: `ubigeoId` (required), `especialidadId` (required), `seguroId?`, `page?`, `pageSize?`.
    - Returns **doctor cards “near me”** in a denormalized, frontend-friendly format (doctor + specialties + clinic).

You can refine field names and payloads later, but keep the **URLs + query params** stable once you integrate the frontend.

---

### Search doctor card DTO (for carousel)

The `GET /search/doctors` endpoint should return a list of **doctor cards**, already shaped for direct rendering in a UI carousel, for example:

- **Doctor fields**
  - `doctorId`
  - `doctorName`
  - `photoUrl` (optional, for avatar)
  - `mainSpecialty`
  - `subSpecialties` (array of names)
- **Clinic fields**
  - `clinicId`
  - `clinicName`
  - `clinicAddress`
- **Insurance & meta**
  - `seguros` (array of insurer names or IDs)

This DTO is **denormalized**: `search_service.py` should join data from `Doctor`, `Clinicas`, `Especialidad`/`SubEspecialidad`, and `Seguros` so the frontend doesn’t need additional API calls to build the carousel cards.

---

### Folder structure

```text
src/backend/
  aws/
    backend.yml          # Main CloudFormation: API Gateway, Lambdas, IAM, DynamoDB tables
    params-dev.json      # CFN parameters per environment (optional)
    params-prod.json

  lambdas/
    clinics/
      handler.py          # Single entrypoint for ClinicsApi REST API
      dto.py
      services/
        clinics_service.py
      repositories/
        clinics_repo.py
        ubigeo_repo.py

    doctors/
      handler.py          # Single entrypoint for DoctorsApi REST API
      dto.py
      services/
        doctors_service.py
      repositories/
        doctors_repo.py
        clinics_repo.py
        specialties_repo.py

    especialidades/
      handler.py          # Single entrypoint for EspecialidadesApi REST API
      dto.py
      services/
        especialidades_service.py
      repositories/
        specialties_repo.py

    seguros/
      handler.py          # Single entrypoint for SegurosApi REST API
      dto.py
      services/
        seguros_service.py
      repositories/
        insurers_repo.py
        clinics_repo.py

    search/   # optional, if you want a dedicated “search near me” Lambda
      handler.py          # Single entrypoint for SearchApi REST API
      dto.py
      services/
        search_service.py
      repositories/
        clinics_repo.py
        doctors_repo.py
        specialties_repo.py
        insurers_repo.py
        ubigeo_repo.py

  scripts/
    package_lambdas.sh   # Zip Lambda code and upload to S3 (for CloudFormation)
    deploy_backend.sh    # aws cloudformation deploy --template-file aws/backend.yml
```

---

### DynamoDB tables (logical model)

All tables are provisioned and managed via `aws/backend.yml` (CloudFormation).

- **Doctor**
  - `doctorId` (PK) → Número de colegiatura
  - `nombreCompleto` (String)
  - `especialidadPrincipalId` (ID)
  - `subEspecialidadIds` (Array of IDs)

- **Clinicas**
  - `clinicaId` (PK)
  - `nombreClinica` (String)
  - `ubicacion` (String)
  - `url` (String)
  - `urlStaffMedico` (String)
  - `grupoClinicaId` (ID)
  - `especialidadIds` (Array of IDs)
  - `ubigeoId` (ID, e.g. 140101 for Lima Metropolitana)

- **Especialidad**
  - `especialidadId` (PK)
  - `nombre` (String)
  - `descripcion` (String)

- **SubEspecialidad**
  - `subEspecialidadId` (PK)
  - `especialidadId` (FK)
  - `nombre` (String)
  - `descripcion` (String)

- **Seguros**
  - `seguroId` (PK)
  - `nombre` (String)
  - `clinicasAsociadas` (Optional JSON / list of Clinica IDs by network)

- **Ubigeo**
  - `ubigeoId` (PK)
  - `departamento` (String)
  - `provincia` (String)
  - `distritoId` (ID principal)
  - `NombreDistrito` (String)

---

### Example request flow (`GET /clinics` – ClinicsApi)

1. **Client request**
   - Frontend (web or mobile) calls:
     - `GET /clinics?ubigeoId=<code>&especialidadId=<id>&seguroId=<id?>&page=1&pageSize=20`
2. **ClinicsApi (REST API Gateway)**
   - Forwards the request to the `clinics` Lambda function (no additional routing).
3. **Lambda handler**
   - `handler.py` receives the raw `event` from API Gateway.
   - It calls the appropriate service function (e.g. `list_clinics`) based on the presence of parameters such as `clinicaId`.
4. **DTO & validation**
   - `dto.py` parses query params, applies defaults (e.g. `pageSize`), and validates required fields.
5. **Service layer**
   - `clinics_service.py`:
     - Uses `ubigeo_repo` to validate and normalize the `ubigeoId` (if present).
     - Queries `clinics_repo` to get clinics by filters (Ubigeo, Especialidad, Seguro).
6. **Response**
   - Returns a paginated JSON list of clinics/hospitals, ready to be rendered by the client.

---

### Implementation checklist

- **Infrastructure (`aws/backend.yml`)**
  - Define DynamoDB tables with keys and capacity.
  - Define one Lambda function per group (`clinics`, `doctors`, `especialidades`, `seguros`, optional `search`).
  - Define one REST API Gateway per group with the paths defined above.
  - Grant each Lambda IAM permissions to read only from the relevant tables.

- **Lambda code (`lambdas/*`)**
  - Implement `handler.py` to parse the event, call the corresponding service function, and format HTTP responses (statusCode, headers, body).
  - Implement DTOs in each `dto.py` (parsing, validation, default values).
  - Implement `*_service.py` using the repositories and returning DTOs ready for the frontend.
  - Implement repositories using `boto3` (or AWS SDK for your language of choice) with query-optimized access patterns.

- **Deployment scripts (`scripts/`)**
  - `package_lambdas.sh`: install dependencies, build, zip, and upload to S3.
  - `deploy_backend.sh`: call `aws cloudformation deploy` with the template and `params-*.json`.

---

### Environments: dev vs prod (and Next.js integration)

Use **two environments** so you can test safely before using real data:

- **dev**
  - CloudFormation params: `aws/params-dev.json`.
  - Example stack name: `health-backend-dev`.
  - APIs: `ClinicsApi-dev`, `DoctorsApi-dev`, `SearchApi-dev`, etc.
  - Base URLs (examples):
    - `https://<dev-clinics-id>.execute-api.<region>.amazonaws.com/dev/clinics`
    - `https://<dev-search-id>.execute-api.<region>.amazonaws.com/dev/search/doctors`
- **prod**
  - CloudFormation params: `aws/params-prod.json`.
  - Example stack name: `health-backend-prod`.
  - Same resources, but pointing to **real data** tables and API URLs.

Typical workflow:

1. **Deploy dev**
   - Run: `scripts/package_lambdas.sh`
   - Run: `scripts/deploy_backend.sh --env dev` (internally passes `--parameter-overrides` from `params-dev.json`).
2. **Point Next.js to dev**
   - In your Next.js app, set environment variables (for example):
     - `NEXT_PUBLIC_SEARCH_API_URL=https://<dev-search-id>.execute-api.<region>.amazonaws.com/dev/search/doctors`
     - `NEXT_PUBLIC_CLINICS_API_URL=https://<dev-clinics-id>.execute-api.<region>.amazonaws.com/dev/clinics`
   - Use these URLs from your data-fetching hooks/components to render doctor cards and clinic lists.
3. **Test end-to-end**
   - Populate dev DynamoDB tables with sample data.
   - Verify that the Next.js UI (doctor carrousel, clinic search, etc.) works correctly against the dev APIs.
4. **Promote to prod**
   - Run: `scripts/deploy_backend.sh --env prod` (using `params-prod.json`).
   - Update your Next.js `.env.production` to point `NEXT_PUBLIC_*_API_URL` variables to the **prod** API Gateway URLs.

This keeps your real production data isolated, while allowing full integration testing with your Next.js frontend against the **dev** environment first.

---

### Local testing quickstart

You can exercise every Lambda without deploying anything by running the handler locally with a fake API Gateway event. Example for the doctor search carousel:

```bash
PYTHONPATH=src/backend/lambdas/search:src/backend \\
python - <<'PY'
from handler import handler

event = {
    "resource": "/search/doctors",
    "httpMethod": "GET",
    "queryStringParameters": {
        "ubigeoId": "150101",
        "especialidadId": "CARD",
        "seguroId": "RIMAC",
        "page": "1",
        "pageSize": "5"
    }
}

response = handler(event, None)
print(response["statusCode"])
print(response["body"])
PY
```

- Each Lambda folder has deterministic sample data under `shared/sample_data.py`, so you immediately get realistic responses (perfect for wiring your Next.js carousels).
- Update the sample data or stub repositories with mocks to simulate edge cases, pagination, etc.
- Once satisfied, run `src/backend/scripts/package_lambdas.sh` to produce `dist/*.zip`, upload them to S3, and deploy with `src/backend/scripts/deploy_backend.sh dev`.

---

### Recommendations and next steps

- **Search-optimized keys**
  - In `Clinicas`, define a GSI or composite key to efficiently query by `(especialidadId, ubigeoId)`:
    - Example pattern: `PK = "ESPECIALIDAD#<id>"`, `SK = "UBIGEO#<id>#CLINICA#<id>"`.
  - This allows `search_service.py` to avoid table scans and keep queries fast and cheap.

- **Consistent doctor card schema**
  - Keep the `DoctorCardDTO` (fields listed above) **stable and versioned** so the frontend carousel can rely on it.
  - If you need to evolve it, prefer adding optional fields rather than renaming/removing existing ones.

- **Denormalized DTOs for the frontend**
  - Keep DynamoDB tables normalized, but always return **denormalized DTOs** from the service layer (doctor + clinic + specialties + insurance + ubigeo data).
  - This makes the API intuitive, reduces client logic, and simplifies future integrations with an open API or partner apps.
