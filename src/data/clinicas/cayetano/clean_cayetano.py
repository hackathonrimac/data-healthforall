#!/usr/bin/env python3
"""
Script to clean cayetano.csv and create cayetano_clean.csv
- Convert semicolon-separated to comma-separated
- Remove "TELECONSULTA" from Sedes column
- Remove rows where Sedes is empty
- Add loc_id_arrays column based on Sedes values
- Keep only cmp, url_photo, and loc_id_arrays columns
"""

import csv
from pathlib import Path


def get_loc_id_array(sedes: str) -> str:
    """
    Convert Sedes value to loc_id_arrays format.
    
    Args:
        sedes: Sedes value (e.g., "SMP", "LINCE", "LINCE, SMP")
    
    Returns:
        String representation of array (e.g., "['CLIN-11']")
    """
    if not sedes or not sedes.strip():
        return "[]"
    
    # Normalize: remove extra spaces and split by comma
    sedes_clean = sedes.strip()
    sedes_list = [s.strip().upper() for s in sedes_clean.split(',')]
    
    loc_ids = []
    if 'SMP' in sedes_list:
        loc_ids.append('CLIN-11')
    if 'LINCE' in sedes_list:
        loc_ids.append('CLIN-10')
    
    # Return as string representation of array
    return str(loc_ids).replace("'", "'")


def clean_sedes(sedes: str) -> str:
    """
    Remove "TELECONSULTA" from Sedes and clean up extra spaces.
    
    Args:
        sedes: Original Sedes value
    
    Returns:
        Cleaned Sedes value
    """
    if not sedes:
        return ""
    
    # Remove TELECONSULTA (case-insensitive)
    sedes_clean = sedes.replace("TELECONSULTA", "").replace("teleconsulta", "").replace("Teleconsulta", "")
    
    # Split by comma, strip each part, and filter out empty strings
    parts = [part.strip() for part in sedes_clean.split(',') if part.strip()]
    
    # Join back with comma and space
    return ", ".join(parts)


def main():
    input_file = Path(__file__).parent / 'cayetano.csv'
    output_file = Path(__file__).parent / 'cayetano_clean.csv'
    
    if not input_file.exists():
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    rows_processed = 0
    rows_written = 0
    
    # Read the original CSV with semicolon delimiter
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        
        # Write to output file with comma delimiter
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            fieldnames = ['cmp', 'url_photo', 'loc_id_arrays']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=',')
            writer.writeheader()
            
            for row in reader:
                rows_processed += 1
                
                # Get and clean Sedes
                sedes = row.get('Sedes', '').strip()
                
                # Remove TELECONSULTA from Sedes
                sedes_clean = clean_sedes(sedes)
                
                # Skip rows where Sedes is empty after cleaning
                if not sedes_clean:
                    continue
                
                # Get loc_id_arrays based on cleaned Sedes
                loc_id_array = get_loc_id_array(sedes_clean)
                
                # Create new row with only the columns we need
                new_row = {
                    'cmp': row.get('CMP', '').strip(),
                    'url_photo': row.get('UrlFoto', '').strip(),
                    'loc_id_arrays': loc_id_array
                }
                
                writer.writerow(new_row)
                rows_written += 1
    
    print(f"Successfully processed {rows_processed} rows.")
    print(f"Rows written (after filtering): {rows_written} rows.")
    print(f"Delimiter changed from ';' to ','")
    print(f"✓ CSV file created: {output_file}")


if __name__ == '__main__':
    main()

