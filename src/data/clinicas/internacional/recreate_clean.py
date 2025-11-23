#!/usr/bin/env python3
"""
Recreate internacional_clean.csv from internacional.csv
- Add loc_id_arrays column with random values
- Remove specified columns
- Change delimiter from ; to ,
"""

import csv
import random
from pathlib import Path

# Valores disponibles para loc_id_arrays
loc_ids = ['CLIN-4', 'CLIN-5', 'CLIN-52', 'CLIN-53']

# Columnas a eliminar
columns_to_remove = [
    'id', 'documentId', 'fullname', 'slug', 'profile_url',
    'createdAt', 'updatedAt', 'publishedAt',
    'specialties', 'sedes', 'sedes_slugs', 'modalities',
    'schedule_summary', 'education_titles', 'education_places',
    'education_dates', 'education_summary', 'certification',
    'awards', 'posts', 'expertise', 'isActive'
]

input_file = 'internacional.csv'
output_file = 'internacional_clean.csv'

input_path = Path(input_file)
output_path = Path(output_file)

if not input_path.exists():
    print(f"Error: Input file '{input_file}' not found.")
    exit(1)

# Read the original CSV with semicolon delimiter
with open(input_path, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile, delimiter=';')
    
    # Get columns to keep
    original_columns = reader.fieldnames
    columns_to_keep = [f for f in original_columns if f not in columns_to_remove]
    columns_to_keep.append('loc_id_arrays')  # Add the new column
    
    # Write to output file with comma delimiter
    with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=columns_to_keep, delimiter=',')
        writer.writeheader()
        
        rows_processed = 0
        for row in reader:
            # Create new row with only the columns to keep
            new_row = {k: v for k, v in row.items() if k in columns_to_keep[:-1]}  # Exclude loc_id_arrays
            
            # Add random loc_id_arrays (1 or 2 values)
            num_values = random.randint(1, 2)
            selected_ids = random.sample(loc_ids, num_values)
            new_row['loc_id_arrays'] = str(selected_ids).replace("'", "'")
            
            writer.writerow(new_row)
            rows_processed += 1

print(f"Successfully processed {rows_processed} rows.")
print(f"Removed columns: {', '.join(columns_to_remove)}")
print(f"Remaining columns: {', '.join(columns_to_keep)}")
print(f"Delimiter changed from ';' to ','")
print(f"✓ CSV file created: {output_file}")

