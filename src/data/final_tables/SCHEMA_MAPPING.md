# Database Schema Mapping

This document outlines the mapping between CSV column names and DynamoDB attribute names.

## Summary of Changes Made

1. ✅ Created `tables.py` to analyze CSV schemas
2. ✅ Added `GruposTable` to `backend.yml`
3. ✅ Added IAM permissions for `GruposTable`
4. ✅ Added `RIMAC_ENSURED` column to DOCTORES table schema

## Table Schemas and Mappings

### DOCTORES Table
**DynamoDB Key:** `doctorId` (String - S)

| CSV Column         | Data Type | DynamoDB Attribute | DynamoDB Type | Notes                    |
|-------------------|-----------|-------------------|---------------|--------------------------|
| CMP               | Number    | doctorId          | S (String)    | Primary Key - Convert to string |
| nombres           | String    | nombres           | S (String)    | -                        |
| apellido_paterno  | String    | apellidoPaterno   | S (String)    | Camel case               |
| apellido_materno  | String    | apellidoMaterno   | S (String)    | Camel case               |
| status            | String    | status            | S (String)    | -                        |
| foto_url          | String    | fotoUrl           | S (String)    | Camel case               |
| especialidad_id   | Number    | especialidadId    | S (String)    | Convert to string        |
| loc_id_arrays     | String    | clinicaIds        | L (List)      | Parse JSON array         |
| **RIMAC_ENSURED** | **Boolean** | **rimacEnsured** | **BOOL (Boolean)** | **NEW COLUMN - Default: false** |

### CLINICAS Table
**DynamoDB Key:** `clinicaId` (String - S)

| CSV Column        | Data Type | DynamoDB Attribute | DynamoDB Type | Notes                    |
|------------------|-----------|-------------------|---------------|--------------------------|
| ID               | String    | clinicaId         | S (String)    | Primary Key              |
| nombre_grupo     | String    | nombreGrupo       | S (String)    | Camel case               |
| id_grupo         | String    | grupoId           | S (String)    | Camel case               |
| nombre_clinica   | String    | nombreClinica     | S (String)    | Camel case               |
| distrito         | String    | distrito          | S (String)    | -                        |
| direccion        | String    | direccion         | S (String)    | -                        |
| ubigeo           | Number    | ubigeoId          | S (String)    | Convert to string        |
| url_landing_page | String    | urlLandingPage    | S (String)    | Camel case               |
| url_lista_medicos| String    | urlListaMedicos   | S (String)    | Camel case               |

### ESPECIALIDAD Table
**DynamoDB Key:** `especialidadId` (String - S)

| CSV Column    | Data Type | DynamoDB Attribute | DynamoDB Type | Notes                    |
|--------------|-----------|-------------------|---------------|--------------------------|
| id           | Number    | especialidadId    | S (String)    | Primary Key - Convert to string |
| nombre       | String    | nombre            | S (String)    | -                        |
| descripcion  | String    | descripcion       | S (String)    | -                        |

### GRUPOS Table (NEW)
**DynamoDB Key:** `grupoId` (String - S)

| CSV Column    | Data Type | DynamoDB Attribute | DynamoDB Type | Notes                    |
|--------------|-----------|-------------------|---------------|--------------------------|
| ID_GRUPO     | String    | grupoId           | S (String)    | Primary Key              |
| NOMBRE_GRUPO | String    | nombreGrupo       | S (String)    | Camel case               |

### UBIGEO Table
**DynamoDB Key:** `ubigeoId` (String - S)

| CSV Column         | Data Type | DynamoDB Attribute | DynamoDB Type | Notes                    |
|-------------------|-----------|-------------------|---------------|--------------------------|
| ID_UBIGEO         | Number    | ubigeoId          | S (String)    | Primary Key - Convert to string |
| Departamento      | Number    | departamento      | N (Number)    | -                        |
| Provincia         | Number    | provincia         | N (Number)    | -                        |
| Distrito          | Number    | distrito          | N (Number)    | -                        |
| Nombre de Distrito| String    | nombreDistrito    | S (String)    | Camel case               |
| ID_cercarnos      | String    | idCercanos        | S (String)    | Camel case, parse as list |

## Changes Required

### 1. Data Transformation Script
Create a script to transform CSV data to match DynamoDB schema:
- Convert snake_case to camelCase
- Convert numeric IDs to strings where needed
- Parse JSON string arrays to proper lists
- Add default values for new columns (e.g., `rimacEnsured: false`)

### 2. Backend.yml Changes
✅ **COMPLETED:**
- Added `GruposTable` definition
- Added IAM permissions for `GruposTable`

### 3. Lambda Code Updates
**NO CHANGES NEEDED** - Lambda code already uses correct attribute names:
- `doctorId`, `clinicaId`, `especialidadId`, `ubigeoId`, `grupoId`
- All lambdas are properly structured

### 4. Populate Script Updates
**FUTURE:** Update `populate_tables.py` to:
- Add grupos table population
- Support new RIMAC_ENSURED column
- Transform CSV data to DynamoDB format

## DynamoDB Attribute Types

- **S**: String
- **N**: Number
- **BOOL**: Boolean
- **L**: List
- **M**: Map

## Notes

1. All partition keys in DynamoDB are defined as Strings (S) for consistency
2. Numeric values can be stored as Numbers (N) for non-key attributes
3. Array fields in CSV (like `loc_id_arrays`) should be parsed and stored as Lists (L)
4. Consider adding GSI (Global Secondary Index) for frequent query patterns

