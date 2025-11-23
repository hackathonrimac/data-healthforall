#!/usr/bin/env python3
"""
Extract column names and data types from CSV files in final_tables directory.
Simple CSV analysis without external dependencies.
"""

import csv
from pathlib import Path

# Define the directory containing CSV files
CSV_DIR = Path(__file__).parent

# Define CSV files to analyze
CSV_FILES = {
    'DOCTORES': 'DOCTORES.csv',
    'CLINICAS': 'CLINICAS.csv',
    'ESPECIALIDAD': 'ESPECIALIDAD.csv',
    'GRUPOS': 'GRUPOS.csv',
    'UBIGEO': 'UBIGEO.csv'
}

def infer_type(value):
    """Infer data type from string value."""
    if not value or value.strip() == '':
        return 'string'
    
    # Check if it's a number
    try:
        int(value)
        return 'number'
    except ValueError:
        pass
    
    try:
        float(value)
        return 'number'
    except ValueError:
        pass
    
    return 'string'

def analyze_csv(file_path):
    """Read CSV and extract column names and inferred types."""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        # Read first row to infer types
        first_row = next(reader, None)
        
        if first_row:
            types = {col: infer_type(first_row[col]) for col in headers}
        else:
            types = {col: 'string' for col in headers}
        
        return types

def main():
    """Analyze all CSV files and print schema information."""
    print("=" * 80)
    print("DATABASE SCHEMA ANALYSIS")
    print("=" * 80)
    
    schemas = {}
    
    for table_name, csv_file in CSV_FILES.items():
        file_path = CSV_DIR / csv_file
        print(f"\n{table_name} Table:")
        print("-" * 80)
        
        schema = analyze_csv(file_path)
        
        # Add RIMAC_ENSURED column to DOCTORES
        if table_name == 'DOCTORES':
            schema['RIMAC_ENSURED'] = 'boolean'
        
        schemas[table_name] = schema
        
        for col_name, dtype in schema.items():
            # Map to DynamoDB types
            if dtype == 'number':
                db_type = 'N (Number)'
            elif dtype == 'boolean':
                db_type = 'BOOL (Boolean)'
            else:
                db_type = 'S (String)'
            
            print(f"  {col_name}: {dtype} -> DynamoDB: {db_type}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\nKey Columns for DynamoDB:")
    print("  - DOCTORES: CMP (Partition Key) - String")
    print("  - CLINICAS: ID (Partition Key) - String")
    print("  - ESPECIALIDAD: id (Partition Key) - String/Number")
    print("  - GRUPOS: ID_GRUPO (Partition Key) - String")
    print("  - UBIGEO: ID_UBIGEO (Partition Key) - Number")
    print("\nNew Column Added:")
    print("  - DOCTORES.RIMAC_ENSURED: Boolean (indicates if doctor is Rimac-insured)")
    print("\nAll tables use String types for IDs except where numerical IDs are used.")
    print("DynamoDB will store all attributes as their native types.")

if __name__ == '__main__':
    main()
