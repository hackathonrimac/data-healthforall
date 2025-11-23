"""
Merge loc_id_arrays from clinical_data CSVs into DOCTORES_CLEAN.csv
Only extracts CMP and loc_id_arrays columns, aggregating data for doctors appearing in multiple clinics.
"""

import pandas as pd
import ast
import os
from pathlib import Path

def parse_loc_id_array(value):
    """Parse loc_id_arrays from string representation to list"""
    if pd.isna(value) or value == '':
        return []
    
    try:
        # Handle string representation of lists
        if isinstance(value, str):
            # Remove extra quotes and parse
            value = value.strip().strip('"')
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return parsed
            return [parsed]
        elif isinstance(value, list):
            return value
        else:
            return [str(value)]
    except (ValueError, SyntaxError):
        print(f"Warning: Could not parse value: {value}")
        return []

def normalize_cmp(cmp):
    """Normalize CMP to integer, handling various formats"""
    if pd.isna(cmp):
        return None
    
    # Convert to string and remove leading zeros and spaces
    cmp_str = str(cmp).strip().lstrip('0')
    
    # If empty after removing zeros, it was '0' or '00000'
    if cmp_str == '':
        cmp_str = '0'
    
    try:
        return int(cmp_str)
    except ValueError:
        print(f"Warning: Could not convert CMP to int: {cmp}")
        return None

def read_clinical_data():
    """Read all clinical_data CSV files and extract CMP and loc_id_arrays"""
    clinical_data_dir = Path(__file__).parent / 'clinical_data'
    
    # Dictionary to aggregate clinic IDs by CMP
    cmp_to_clinics = {}
    
    # Get all CSV files in clinical_data directory
    csv_files = list(clinical_data_dir.glob('*.csv'))
    print(f"Found {len(csv_files)} clinical data files")
    
    for csv_file in csv_files:
        print(f"\nProcessing: {csv_file.name}")
        
        try:
            # Read CSV
            df = pd.read_csv(csv_file)
            
            # Find CMP column (case-insensitive)
            cmp_col = None
            for col in df.columns:
                if col.lower() == 'cmp':
                    cmp_col = col
                    break
            
            if cmp_col is None:
                print(f"  Warning: No CMP column found in {csv_file.name}")
                continue
            
            # Check for loc_id_arrays column
            if 'loc_id_arrays' not in df.columns:
                print(f"  Warning: No loc_id_arrays column found in {csv_file.name}")
                continue
            
            # Extract only CMP and loc_id_arrays
            records_processed = 0
            for _, row in df.iterrows():
                cmp = normalize_cmp(row[cmp_col])
                
                if cmp is None:
                    continue
                
                loc_ids = parse_loc_id_array(row['loc_id_arrays'])
                
                # Aggregate clinic IDs for this CMP
                if cmp not in cmp_to_clinics:
                    cmp_to_clinics[cmp] = set()
                
                cmp_to_clinics[cmp].update(loc_ids)
                records_processed += 1
            
            print(f"  Processed {records_processed} records")
            
        except Exception as e:
            print(f"  Error processing {csv_file.name}: {e}")
            continue
    
    print(f"\n✓ Total unique doctors found: {len(cmp_to_clinics)}")
    
    # Convert to DataFrame
    merged_data = []
    for cmp, clinics in cmp_to_clinics.items():
        # Sort clinic IDs for consistency
        clinic_list = sorted(list(clinics))
        merged_data.append({
            'CMP': cmp,
            'loc_id_arrays': clinic_list
        })
    
    return pd.DataFrame(merged_data)

def merge_with_doctores():
    """Merge clinical data with DOCTORES_CLEAN.csv"""
    print("\n" + "="*60)
    print("MERGING PROCESS")
    print("="*60)
    
    # Read clinical data
    print("\n1. Reading clinical data files...")
    clinical_df = read_clinical_data()
    
    # Read DOCTORES_CLEAN.csv
    print("\n2. Reading DOCTORES_CLEAN.csv...")
    doctores_path = Path(__file__).parent / 'DOCTORES_CLEAN.csv'
    doctores_df = pd.read_csv(doctores_path)
    
    print(f"   Original records: {len(doctores_df)}")
    print(f"   Original columns: {list(doctores_df.columns)}")
    
    # Normalize CMP in doctores_df
    doctores_df['CMP'] = doctores_df['CMP'].apply(normalize_cmp)
    
    # Merge on CMP
    print("\n3. Merging data...")
    merged_df = doctores_df.merge(
        clinical_df,
        on='CMP',
        how='left'
    )
    
    # Fill NaN with empty lists
    merged_df['loc_id_arrays'] = merged_df['loc_id_arrays'].apply(
        lambda x: x if isinstance(x, list) else []
    )
    
    # Convert lists to string representation for CSV storage
    merged_df['loc_id_arrays'] = merged_df['loc_id_arrays'].apply(
        lambda x: str(x) if x else '[]'
    )
    
    # Statistics
    doctors_with_clinics = (merged_df['loc_id_arrays'] != '[]').sum()
    
    print(f"\n4. Merge statistics:")
    print(f"   Total doctors: {len(merged_df)}")
    print(f"   Doctors with clinic assignments: {doctors_with_clinics}")
    print(f"   Doctors without clinic assignments: {len(merged_df) - doctors_with_clinics}")
    print(f"   Final columns: {list(merged_df.columns)}")
    
    # Save to new file
    output_path = Path(__file__).parent / 'DOCTORES_MERGED.csv'
    merged_df.to_csv(output_path, index=False)
    
    print(f"\n✓ Merged data saved to: {output_path.name}")
    
    # Show sample of doctors with clinics
    print("\n5. Sample of doctors with clinic assignments:")
    sample = merged_df[merged_df['loc_id_arrays'] != '[]'].head(10)
    for _, row in sample.iterrows():
        print(f"   CMP {row['CMP']}: {row['nombres']} {row['apellido_paterno']} -> {row['loc_id_arrays']}")
    
    return merged_df

if __name__ == "__main__":
    print("="*60)
    print("DOCTOR-CLINIC DATA MERGING TOOL")
    print("="*60)
    
    result = merge_with_doctores()
    
    print("\n" + "="*60)
    print("✓ MERGE COMPLETED SUCCESSFULLY")
    print("="*60)

