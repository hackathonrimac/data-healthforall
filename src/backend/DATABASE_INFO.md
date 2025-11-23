# Database Information

## DynamoDB Tables

### doctors-{environment}
| Column | Type | Description |
|--------|------|-------------|
| doctorId | String (PK) | Unique doctor identifier |
| nombreCompleto | String | Doctor's full name |
| especialidadPrincipalId | String | Main specialty ID |
| subEspecialidadIds | List[String] | List of subspecialty IDs |
| clinicaId | String | Clinic where doctor works |
| photoUrl | String | Doctor's photo URL |

### clinics-{environment}
| Column | Type | Description |
|--------|------|-------------|
| clinicaId | String (PK) | Unique clinic identifier |
| nombreClinica | String | Clinic name |
| ubicacion | String | Clinic address |
| ubigeoId | String | Geographic location ID |
| especialidadIds | List[String] | List of available specialties |
| seguroIds | List[String] | List of accepted insurances |
| grupoClinicaId | String | Clinic group identifier |
| url | String | Clinic website URL |
| urlStaffMedico | String | Medical staff page URL |

### especialidades-{environment}
| Column | Type | Description |
|--------|------|-------------|
| especialidadId | String (PK) | Unique specialty identifier |
| nombre | String | Specialty name |
| descripcion | String | Specialty description |

### subespecialidades-{environment}
| Column | Type | Description |
|--------|------|-------------|
| subEspecialidadId | String (PK) | Unique subspecialty identifier |
| especialidadId | String | Parent specialty ID |
| nombre | String | Subspecialty name |
| descripcion | String | Subspecialty description |

### seguros-{environment}
| Column | Type | Description |
|--------|------|-------------|
| seguroId | String (PK) | Unique insurance identifier |
| nombre | String | Insurance company name |
| descripcion | String | Insurance description |

### ubigeo-{environment}
| Column | Type | Description |
|--------|------|-------------|
| ubigeoId | String (PK) | Unique ubigeo identifier |
| departamento | String | Department name |
| provincia | String | Province name |
| distritoId | String | District ID |
| nombreDistrito | String | District name |

**Note:** All tables use PAY_PER_REQUEST billing mode. The `{environment}` suffix is either `dev` or `prod`. PK = Partition Key.

