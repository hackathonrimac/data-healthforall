# Database Information

## DynamoDB Tables

### doctors-{environment}
| Column | Type | Description |
|--------|------|-------------|
| DoctorId | String (PK) | Unique doctor identifier |
| NombreCompleto | String | Doctor's full name |
| EspecialidadPrincipalId | String | Main specialty ID |
| SubEspecialidadIds | List[String] | List of subspecialty IDs |
| ClinicaId | String | Clinic where doctor works |
| PhotoUrl | String | Doctor's photo URL |

### clinics-{environment}
| Column | Type | Description |
|--------|------|-------------|
| ClinicaId | String (PK) | Unique clinic identifier |
| NombreClinica | String | Clinic name |
| Ubicacion | String | Clinic address |
| UbigeoId | String | Geographic location ID |
| EspecialidadIds | List[String] | List of available specialties |
| SeguroIds | List[String] | List of accepted insurances |
| GrupoClinicaId | String | Clinic group identifier |
| URL | String | Clinic website URL |
| URLStaffMedico | String | Medical staff page URL |

### especialidades-{environment}
| Column | Type | Description |
|--------|------|-------------|
| EspecialidadId | String (PK) | Unique specialty identifier |
| Nombre | String | Specialty name |
| Descripcion | String | Specialty description |

### subespecialidades-{environment}
| Column | Type | Description |
|--------|------|-------------|
| SubEspecialidadId | String (PK) | Unique subspecialty identifier |
| EspecialidadId | String | Parent specialty ID |
| Nombre | String | Subspecialty name |
| Descripcion | String | Subspecialty description |

### seguros-{environment}
| Column | Type | Description |
|--------|------|-------------|
| SeguroId | String (PK) | Unique insurance identifier |
| Nombre | String | Insurance company name |
| Descripcion | String | Insurance description |

### ubigeo-{environment}
| Column | Type | Description |
|--------|------|-------------|
| UbigeoId | String (PK) | Unique ubigeo identifier |
| Departamento | String | Department name |
| Provincia | String | Province name |
| DistritoId | String | District ID |
| NombreDistrito | String | District name |

**Note:** All tables use PAY_PER_REQUEST billing mode. The `{environment}` suffix is either `dev` or `prod`. PK = Partition Key.

