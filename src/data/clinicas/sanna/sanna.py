#!/usr/bin/env python3
"""
Convert all Sanna JSON files to a single CSV format.

This script reads all JSON files from the Sanna data directory and converts
them to a single CSV file with all doctor information appended.
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Set


def get_all_json_files(directory: Path) -> List[Path]:
    """Get all JSON files in the directory, excluding the script itself."""
    json_files = sorted(directory.glob("*.json"))
    return json_files


def extract_doctors_from_json(json_file: Path) -> List[Dict]:
    """
    Extract doctors data from a JSON file.
    
    Args:
        json_file: Path to the JSON file
        
    Returns:
        List of doctor dictionaries
    """
    print(f"Reading JSON file: {json_file.name}")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract the data array
        if 'data' not in data:
            print(f"  ⚠️  WARNING: 'data' key not found in {json_file.name}")
            return []
        
        doctors = data['data']
        
        if not doctors:
            print(f"  ⚠️  WARNING: No doctors found in {json_file.name}")
            return []
        
        print(f"  ✅ Found {len(doctors)} doctors")
        return doctors
        
    except Exception as e:
        print(f"  ❌ ERROR reading {json_file.name}: {e}")
        return []


def get_all_fieldnames(doctors_list: List[List[Dict]]) -> List[str]:
    """Get all unique field names from all doctor records."""
    all_fields: Set[str] = set()
    
    for doctors in doctors_list:
        for doctor in doctors:
            all_fields.update(doctor.keys())
    
    # Sort for consistent column order
    return sorted(all_fields)


def convert_all_json_to_csv(directory: Path, output_csv: str = "sanna_todos_doctores.csv"):
    """
    Convert all JSON files in the directory to a single CSV file.
    
    Args:
        directory: Directory containing JSON files
        output_csv: Output CSV filename
    """
    json_files = get_all_json_files(directory)
    
    if not json_files:
        print("No JSON files found in directory")
        return
    
    print(f"Found {len(json_files)} JSON files:")
    for json_file in json_files:
        print(f"  - {json_file.name}")
    print()
    
    # Extract doctors from all JSON files
    all_doctors_lists = []
    for json_file in json_files:
        doctors = extract_doctors_from_json(json_file)
        if doctors:
            all_doctors_lists.append(doctors)
    
    if not all_doctors_lists:
        print("No doctors found in any JSON file")
        return
    
    # Get all fieldnames
    fieldnames = get_all_fieldnames(all_doctors_lists)
    
    # Flatten all doctors into a single list
    all_doctors = []
    for doctors in all_doctors_lists:
        all_doctors.extend(doctors)
    
    print(f"\nTotal doctors: {len(all_doctors)}")
    print(f"Columns: {len(fieldnames)}")
    
    # Write to CSV
    output_path = directory / output_csv
    print(f"\nWriting CSV file: {output_path}")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for doctor in all_doctors:
            # Convert None values to empty strings and ensure all fields are present
            row = {}
            for field in fieldnames:
                value = doctor.get(field)
                row[field] = (value if value is not None else '')
            writer.writerow(row)
    
    print(f"✅ CSV saved: {output_path} ({len(all_doctors)} doctors)")
    print(f"\nColumns: {', '.join(fieldnames)}")


def main():
    """Main function to convert all Sanna JSON files to a single CSV."""
    script_dir = Path(__file__).parent
    convert_all_json_to_csv(script_dir)


if __name__ == "__main__":
    main()

