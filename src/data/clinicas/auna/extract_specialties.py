#!/usr/bin/env python3
"""
Extract unique specialties from auna_doctores.csv

This script reads the CSV file and extracts all unique specialty values,
outputting them in multiple formats:
- TXT: One specialty per line
- CSV: Single column with header
- JSON: Structured format with count
- Array: Comma-separated values (quoted) in a single line
"""

import csv
from pathlib import Path
from typing import Set


def extract_unique_specialties(csv_file: str = "auna_doctores.csv", 
                                output_txt: str = "auna_especialidades.txt",
                                output_csv: str = "auna_especialidades.csv",
                                output_json: str = "auna_especialidades.json",
                                output_array: str = "auna_especialidades_array.txt"):
    """Extract all unique specialty values from the CSV file."""
    import json
    specialties_set: Set[str] = set()
    
    print(f"Reading CSV file: {csv_file}")
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        
        for row in reader:
            specialties_str = row.get('specialties', '').strip()
            if specialties_str:
                # Split by comma and clean each specialty
                specialties = [s.strip() for s in specialties_str.split(',')]
                for spec in specialties:
                    if spec:  # Only add non-empty strings
                        specialties_set.add(spec)
    
    # Sort for consistent output
    unique_specialties = sorted(specialties_set)
    
    print(f"\nFound {len(unique_specialties)} unique specialties")
    
    base_path = Path(csv_file).parent
    
    # Save as TXT (one per line)
    txt_path = base_path / output_txt
    with open(txt_path, 'w', encoding='utf-8') as f:
        for spec in unique_specialties:
            f.write(f"{spec}\n")
    print(f"✅ TXT saved to: {txt_path}")
    
    # Save as CSV
    csv_path = base_path / output_csv
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['specialty'])
        for spec in unique_specialties:
            writer.writerow([spec])
    print(f"✅ CSV saved to: {csv_path}")
    
    # Save as JSON
    json_path = base_path / output_json
    json_data = {
        'total_specialties': len(unique_specialties),
        'specialties': unique_specialties
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON saved to: {json_path}")
    
    # Save as comma-separated array (single line)
    array_path = base_path / output_array
    # Quote each specialty and join with commas
    quoted_specialties = [f'"{spec}"' for spec in unique_specialties]
    comma_separated = ', '.join(quoted_specialties)
    with open(array_path, 'w', encoding='utf-8') as f:
        f.write(comma_separated)
    print(f"✅ Comma-separated array saved to: {array_path}")
    
    # Also print first 20 for preview
    print("\nFirst 20 specialties:")
    for i, spec in enumerate(unique_specialties[:20], 1):
        print(f"  {i}. {spec}")
    
    if len(unique_specialties) > 20:
        print(f"  ... and {len(unique_specialties) - 20} more")
    
    return unique_specialties


def main():
    csv_file = Path(__file__).parent / "auna_doctores.csv"
    
    if not csv_file.exists():
        print(f"ERROR: File not found: {csv_file}")
        return
    
    extract_unique_specialties(str(csv_file))


if __name__ == "__main__":
    main()

