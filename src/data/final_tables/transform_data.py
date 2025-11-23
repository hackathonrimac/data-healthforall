#!/usr/bin/env python3
"""
Transform CSV data to DynamoDB-compatible format.

This script reads CSV files from final_tables directory and transforms them
to match the expected DynamoDB schema with proper attribute names and types.
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List


CSV_DIR = Path(__file__).parent


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


def transform_csv_file(
    input_file: Path,
    output_file: Path,
    transform_func: callable
) -> int:
    """Transform a CSV file using the provided transformation function."""
    count = 0
    transformed_items = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                transformed = transform_func(row)
                transformed_items.append(transformed)
                count += 1
            except Exception as e:
                print(f"  ⚠️  Error transforming row: {e}")
                print(f"     Row: {row}")
    
    # Write as JSON Lines format (one JSON object per line)
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in transformed_items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    return count


def main():
    """Transform all CSV files."""
    output_dir = CSV_DIR / 'transformed'
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 80)
    print("CSV TO DYNAMODB TRANSFORMATION")
    print("=" * 80)
    
    transformations = [
        ('DOCTORES.csv', 'doctores.jsonl', transform_doctores),
        ('CLINICAS.csv', 'clinicas.jsonl', transform_clinicas),
        ('ESPECIALIDAD.csv', 'especialidades.jsonl', transform_especialidad),
        ('GRUPOS.csv', 'grupos.jsonl', transform_grupos),
        ('UBIGEO.csv', 'ubigeo.jsonl', transform_ubigeo)
    ]
    
    total_items = 0
    
    for input_name, output_name, transform_func in transformations:
        input_file = CSV_DIR / input_name
        output_file = output_dir / output_name
        
        print(f"\n📄 Transforming {input_name}...")
        
        if not input_file.exists():
            print(f"  ⚠️  File not found: {input_file}")
            continue
        
        count = transform_csv_file(input_file, output_file, transform_func)
        total_items += count
        
        print(f"  ✅ Transformed {count} items -> {output_file}")
    
    print("\n" + "=" * 80)
    print("TRANSFORMATION COMPLETE")
    print("=" * 80)
    print(f"Total items transformed: {total_items}")
    print(f"Output directory: {output_dir}")
    print("\nNext steps:")
    print("1. Review transformed data in the 'transformed/' directory")
    print("2. Use AWS CLI or boto3 to batch-write items to DynamoDB")
    print("3. Update populate_tables.py to use these transformed files")


if __name__ == '__main__':
    main()

