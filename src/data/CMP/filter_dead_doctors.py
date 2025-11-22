#!/usr/bin/env python3
"""
Filter out dead doctors (FALLECIDO) from existing CSV and JSON files.
Creates clean copies without dead doctors.
"""

import json
import csv
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def is_dead_doctor(doctor: dict) -> bool:
    """Check if doctor is dead based on status field."""
    status = doctor.get('status', '').strip().upper()
    return status == 'FALLECIDO'


def filter_csv(input_file: str, output_file: str):
    """Filter dead doctors from CSV file."""
    logger.info(f"Filtering CSV: {input_file} -> {output_file}")
    
    if not Path(input_file).exists():
        logger.error(f"Input file not found: {input_file}")
        return 0, 0
    
    total_rows = 0
    removed_rows = 0
    kept_rows = 0
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        if not fieldnames:
            logger.error("CSV file has no headers")
            return 0, 0
        
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                total_rows += 1
                if is_dead_doctor(row):
                    removed_rows += 1
                else:
                    writer.writerow(row)
                    kept_rows += 1
    
    logger.info(f"CSV filtering complete: {total_rows} total, {removed_rows} removed, {kept_rows} kept")
    return removed_rows, kept_rows


def filter_json(input_file: str, output_file: str):
    """Filter dead doctors from JSON file."""
    logger.info(f"Filtering JSON: {input_file} -> {output_file}")
    
    if not Path(input_file).exists():
        logger.error(f"Input file not found: {input_file}")
        return 0, 0
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            doctors = json.load(f)
        
        total = len(doctors)
        alive_doctors = [doc for doc in doctors if not is_dead_doctor(doc)]
        removed = total - len(alive_doctors)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(alive_doctors, f, ensure_ascii=False, indent=2)
        
        logger.info(f"JSON filtering complete: {total} total, {removed} removed, {len(alive_doctors)} kept")
        return removed, len(alive_doctors)
        
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {e}")
        return 0, 0
    except Exception as e:
        logger.error(f"Error filtering JSON: {e}")
        return 0, 0


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Filter dead doctors from CMP data files')
    parser.add_argument('--csv-input', type=str, default='doctors_data.csv',
                       help='Input CSV file (default: doctors_data.csv)')
    parser.add_argument('--csv-output', type=str, default='doctors_data_alive.csv',
                       help='Output CSV file (default: doctors_data_alive.csv)')
    parser.add_argument('--json-input', type=str, default='doctors_data.json',
                       help='Input JSON file (default: doctors_data.json)')
    parser.add_argument('--json-output', type=str, default='doctors_data_alive.json',
                       help='Output JSON file (default: doctors_data_alive.json)')
    parser.add_argument('--backup', action='store_true',
                       help='Create backup of original files before filtering')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Filtering Dead Doctors (FALLECIDO) from CMP Data")
    print("=" * 80)
    print()
    
    # Create backups if requested
    if args.backup:
        import shutil
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        csv_backup = f"{args.csv_input}.backup_{timestamp}"
        json_backup = f"{args.json_input}.backup_{timestamp}"
        
        if Path(args.csv_input).exists():
            shutil.copy2(args.csv_input, csv_backup)
            logger.info(f"Created CSV backup: {csv_backup}")
        
        if Path(args.json_input).exists():
            shutil.copy2(args.json_input, json_backup)
            logger.info(f"Created JSON backup: {json_backup}")
        print()
    
    # Filter CSV
    csv_removed, csv_kept = filter_csv(args.csv_input, args.csv_output)
    print()
    
    # Filter JSON
    json_removed, json_kept = filter_json(args.json_input, args.json_output)
    print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"CSV: Removed {csv_removed} dead doctor records, kept {csv_kept} alive records")
    print(f"JSON: Removed {json_removed} dead doctors, kept {json_kept} alive doctors")
    print()
    print(f"Clean files created:")
    print(f"  - {args.csv_output}")
    print(f"  - {args.json_output}")
    print("=" * 80)


if __name__ == '__main__':
    main()

