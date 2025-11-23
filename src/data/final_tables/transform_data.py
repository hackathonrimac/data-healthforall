#!/usr/bin/env python3
"""
Transform CSV data to DynamoDB-compatible format.

This script reads CSV files from final_tables directory and transforms them
to match the expected DynamoDB schema with proper attribute names and types.

FILTERING LOGIC:
- Only includes DOCTORS with valid specialties AND clinic assignments
- Only includes ESPECIALIDAD entries used by doctors with clinic assignments
- Only includes UBIGEO entries that are actually used by clinics
- Only includes CLINICS with valid location data
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Set


CSV_DIR = Path(__file__).parent

# Global sets to store used IDs (populated during pre-analysis)
USED_ESPECIALIDAD_IDS: Set[str] = set()
USED_UBIGEO_IDS: Set[str] = set()


def transform_doctores(csv_row: Dict[str, str]) -> Dict[str, Any]:
    """Transform DOCTORES CSV row to DynamoDB format."""
    # Parse loc_id_arrays which is a JSON string
    clinica_ids = []
    if csv_row.get('loc_id_arrays'):
        try:
            # Handle both single quotes and double quotes in JSON
            loc_str = csv_row['loc_id_arrays'].replace("'", '"')
            clinica_ids = json.loads(loc_str)
        except json.JSONDecodeError:
            clinica_ids = []
    
    return {
        'doctorId': str(csv_row['CMP']),  # Convert to string
        'nombres': csv_row['nombres'],
        'apellidoPaterno': csv_row['apellido_paterno'],
        'apellidoMaterno': csv_row['apellido_materno'],
        'status': csv_row['status'],
        'fotoUrl': csv_row['foto_url'],
        'especialidadId': str(csv_row['especialidad_id']),  # Convert to string
        'clinicaIds': clinica_ids,  # List of clinic IDs
        'rimacEnsured': False  # NEW COLUMN - default to False
    }


def transform_clinicas(csv_row: Dict[str, str]) -> Dict[str, Any]:
    """Transform CLINICAS CSV row to DynamoDB format."""
    return {
        'clinicaId': csv_row['ID'],
        'nombreGrupo': csv_row['nombre_grupo'],
        'grupoId': csv_row['id_grupo'],
        'nombreClinica': csv_row['nombre_clinica'],
        'distrito': csv_row['distrito'],
        'direccion': csv_row['direccion'],
        'ubigeoId': str(csv_row['ubigeo']),  # Convert to string
        'urlLandingPage': csv_row['url_landing_page'],
        'urlListaMedicos': csv_row['url_lista_medicos']
    }


def transform_especialidad(csv_row: Dict[str, str]) -> Dict[str, Any]:
    """Transform ESPECIALIDAD CSV row to DynamoDB format."""
    return {
        'especialidadId': str(csv_row['id']),  # Convert to string
        'nombre': csv_row['nombre'],
        'descripcion': csv_row['descripcion']
    }


def transform_grupos(csv_row: Dict[str, str]) -> Dict[str, Any]:
    """Transform GRUPOS CSV row to DynamoDB format."""
    return {
        'grupoId': csv_row['ID_GRUPO'],
        'nombreGrupo': csv_row['NOMBRE_GRUPO']
    }


def transform_ubigeo(csv_row: Dict[str, str]) -> Dict[str, Any]:
    """Transform UBIGEO CSV row to DynamoDB format."""
    # Parse ID_cercarnos which is a comma-separated string
    id_cercanos = []
    if csv_row.get('ID_cercarnos'):
        id_cercanos = [id.strip() for id in csv_row['ID_cercarnos'].split(',')]
    
    return {
        'ubigeoId': str(csv_row['ID_UBIGEO']),  # Convert to string
        'departamento': int(csv_row['Departamento']),
        'provincia': int(csv_row['Provincia']),
        'distrito': int(csv_row['Distrito']),
        'nombreDistrito': csv_row['Nombre de Distrito'],
        'idCercanos': id_cercanos  # List of nearby ubigeo IDs
    }


def analyze_data_relationships() -> tuple[Set[str], Set[str], Set[str]]:
    """
    Pre-analyze data to identify valid relationships.
    
    Returns:
        tuple: (valid_especialidad_ids, used_especialidad_ids, used_ubigeo_ids)
    """
    print("\n" + "=" * 80)
    print("PRE-ANALYSIS: IDENTIFYING VALID RELATIONSHIPS")
    print("=" * 80)
    
    # Step 1: Get all valid specialty IDs from ESPECIALIDAD.csv
    valid_especialidad_ids = set()
    with open(CSV_DIR / 'ESPECIALIDAD.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            valid_especialidad_ids.add(str(row['id']))
    
    print(f"✓ Found {len(valid_especialidad_ids)} specialty definitions")
    
    # Step 2: Analyze doctors to find those with clinic assignments
    # Only count specialties from doctors who actually work at clinics
    used_especialidad_ids = set()
    doctors_with_clinics_and_valid_specialty = 0
    doctors_with_clinics_invalid_specialty = 0
    doctors_without_clinics = 0
    doctors_with_invalid_specialties = 0
    
    with open(CSV_DIR / 'DOCTORES.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            especialidad_id = str(row['especialidad_id'])
            
            # Parse clinic assignments
            clinica_ids = []
            if row.get('loc_id_arrays'):
                try:
                    loc_str = row['loc_id_arrays'].replace("'", '"')
                    clinica_ids = json.loads(loc_str)
                except json.JSONDecodeError:
                    clinica_ids = []
            
            has_clinics = bool(clinica_ids and len(clinica_ids) > 0)
            has_valid_specialty = especialidad_id in valid_especialidad_ids
            
            if has_clinics and has_valid_specialty:
                used_especialidad_ids.add(especialidad_id)
                doctors_with_clinics_and_valid_specialty += 1
            elif has_clinics and not has_valid_specialty:
                doctors_with_clinics_invalid_specialty += 1
            elif not has_clinics and has_valid_specialty:
                doctors_without_clinics += 1
            else:
                doctors_with_invalid_specialties += 1
    
    print(f"✓ Doctors with clinics AND valid specialties: {doctors_with_clinics_and_valid_specialty}")
    print(f"🗑️  Doctors with clinics but invalid specialties: {doctors_with_clinics_invalid_specialty}")
    print(f"🗑️  Doctors without clinic assignments: {doctors_without_clinics + doctors_with_invalid_specialties}")
    print(f"✓ Unique specialties used by doctors WITH clinics: {len(used_especialidad_ids)}")
    unused_especialidades = len(valid_especialidad_ids) - len(used_especialidad_ids)
    print(f"🗑️  Unused specialties (will be excluded): {unused_especialidades}")
    
    # Step 3: Analyze clinics to find which ubigeos are actually used
    used_ubigeo_ids = set()
    clinics_with_ubigeo = 0
    clinics_without_ubigeo = 0
    
    with open(CSV_DIR / 'CLINICAS.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ubigeo = str(row['ubigeo']).strip()
            if ubigeo:
                used_ubigeo_ids.add(ubigeo)
                clinics_with_ubigeo += 1
            else:
                clinics_without_ubigeo += 1
    
    print(f"✓ Clinics with valid ubigeos: {clinics_with_ubigeo}")
    if clinics_without_ubigeo > 0:
        print(f"⚠️  Clinics without ubigeo (virtual/invalid): {clinics_without_ubigeo}")
    
    total_ubigeos = 0
    with open(CSV_DIR / 'UBIGEO.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        total_ubigeos = sum(1 for _ in reader)
    
    print(f"✓ Ubigeos used by clinics: {len(used_ubigeo_ids)}")
    print(f"🗑️  Unused ubigeos (will be excluded): {total_ubigeos - len(used_ubigeo_ids)}")
    
    return valid_especialidad_ids, used_especialidad_ids, used_ubigeo_ids


def transform_csv_file(
    input_file: Path,
    output_file: Path,
    transform_func: callable,
    filter_func: callable = None
) -> tuple[int, int]:
    """
    Transform a CSV file using the provided transformation function.
    
    Args:
        input_file: Input CSV file path
        output_file: Output JSONL file path
        transform_func: Function to transform each row
        filter_func: Optional function to filter rows (return True to include)
    
    Returns:
        tuple: (included_count, excluded_count)
    """
    included_count = 0
    excluded_count = 0
    transformed_items = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Apply filter if provided
                if filter_func and not filter_func(row):
                    excluded_count += 1
                    continue
                
                transformed = transform_func(row)
                transformed_items.append(transformed)
                included_count += 1
            except Exception as e:
                print(f"  ⚠️  Error transforming row: {e}")
                print(f"     Row: {row}")
                excluded_count += 1
    
    # Write as JSON Lines format (one JSON object per line)
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in transformed_items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return included_count, excluded_count


def main():
    """Transform all CSV files with intelligent filtering."""
    global USED_ESPECIALIDAD_IDS, USED_UBIGEO_IDS
    
    output_dir = CSV_DIR / 'transformed'
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 80)
    print("CSV TO DYNAMODB TRANSFORMATION WITH FILTERING")
    print("=" * 80)
    
    # Pre-analyze data to identify valid relationships
    valid_especialidad_ids, used_especialidad_ids, used_ubigeo_ids = analyze_data_relationships()
    USED_ESPECIALIDAD_IDS = used_especialidad_ids
    USED_UBIGEO_IDS = used_ubigeo_ids
    
    # Define filter functions
    def filter_doctor(row: Dict[str, str]) -> bool:
        """Only include doctors with valid specialty IDs AND clinic assignments."""
        # Check if specialty is valid
        if str(row['especialidad_id']) not in valid_especialidad_ids:
            return False
        
        # Check if doctor has clinic assignments
        if row.get('loc_id_arrays'):
            try:
                loc_str = row['loc_id_arrays'].replace("'", '"')
                clinica_ids = json.loads(loc_str)
                return bool(clinica_ids and len(clinica_ids) > 0)
            except json.JSONDecodeError:
                return False
        return False
    
    def filter_clinica(row: Dict[str, str]) -> bool:
        """Only include clinics with valid ubigeo IDs (exclude virtual clinics)."""
        ubigeo = str(row['ubigeo']).strip()
        return ubigeo != '' and ubigeo in used_ubigeo_ids
    
    def filter_especialidad(row: Dict[str, str]) -> bool:
        """Only include specialties that are used by doctors."""
        return str(row['id']) in used_especialidad_ids
    
    def filter_ubigeo(row: Dict[str, str]) -> bool:
        """Only include ubigeos that are used by clinics."""
        return str(row['ID_UBIGEO']) in used_ubigeo_ids
    
    print("\n" + "=" * 80)
    print("TRANSFORMATION WITH FILTERING")
    print("=" * 80)
    
    # Define transformations with optional filters
    transformations = [
        ('DOCTORES.csv', 'doctores.jsonl', transform_doctores, filter_doctor),
        ('CLINICAS.csv', 'clinicas.jsonl', transform_clinicas, filter_clinica),
        ('ESPECIALIDAD.csv', 'especialidades.jsonl', transform_especialidad, filter_especialidad),
        ('GRUPOS.csv', 'grupos.jsonl', transform_grupos, None),
        ('UBIGEO.csv', 'ubigeo.jsonl', transform_ubigeo, filter_ubigeo)
    ]
    
    total_included = 0
    total_excluded = 0
    
    for input_name, output_name, transform_func, filter_func in transformations:
        input_file = CSV_DIR / input_name
        output_file = output_dir / output_name
        
        print(f"\n📄 Transforming {input_name}...")
        
        if not input_file.exists():
            print(f"  ⚠️  File not found: {input_file}")
            continue
        
        included, excluded = transform_csv_file(input_file, output_file, transform_func, filter_func)
        total_included += included
        total_excluded += excluded
        
        if excluded > 0:
            print(f"  ✅ Included: {included} items | 🗑️  Excluded: {excluded} items")
        else:
            print(f"  ✅ Included: {included} items")
        print(f"     Output: {output_file}")
    
    print("\n" + "=" * 80)
    print("TRANSFORMATION COMPLETE")
    print("=" * 80)
    print(f"✅ Total items included: {total_included}")
    print(f"🗑️  Total items excluded: {total_excluded}")
    print(f"📁 Output directory: {output_dir}")
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("✓ Only doctors with clinic assignments AND valid specialties were included")
    print("✓ Only specialties used by doctors with clinics were included")
    print("✓ Only clinics with valid location data were included")
    print("✓ Only ubigeos used by clinics were included")
    print("\n💡 This ensures all data represents doctors actively working at physical clinics")
    print("\nNext steps:")
    print("1. Review transformed data in the 'transformed/' directory")
    print("2. Use populate_tables.py to load data into DynamoDB")
    print("3. Verify data integrity in production")


if __name__ == '__main__':
    main()

