import pandas as pd
import json
import unicodedata
import csv

def normalize_unicode(text):
    """
    Normalize Unicode escape sequences and ensure proper encoding.
    Converts \u00cd to Í, \u00c1 to Á, etc.
    """
    if pd.isna(text) or text == '':
        return text
    
    # Convert to string if not already
    text = str(text)
    
    # Decode Unicode escape sequences
    try:
        # First try to decode if it's a string with escape sequences
        if '\\u' in text:
            text = text.encode('utf-8').decode('unicode_escape')
    except:
        pass
    
    # Normalize Unicode characters (NFD to NFC)
    text = unicodedata.normalize('NFC', text)
    
    return text

def normalize_name(name):
    """
    Normalize name to have first letter uppercase and rest lowercase.
    Handles multi-word names (like "JORGE ENRIQUE" -> "Jorge Enrique").
    """
    if pd.isna(name) or name == '':
        return name
    
    name = str(name).strip()
    
    # Split by spaces and capitalize each word
    words = name.split()
    normalized_words = []
    
    for word in words:
        if word:
            # First letter uppercase, rest lowercase
            normalized_word = word[0].upper() + word[1:].lower() if len(word) > 1 else word.upper()
            normalized_words.append(normalized_word)
    
    return ' '.join(normalized_words)

def consolidate_doctors_data(input_file, output_file):
    """
    Consolidate duplicate CMP entries by grouping specialties and related fields into arrays.
    """
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    
    print(f"Original rows: {len(df)}")
    print(f"Unique CMPs: {df['cmp'].nunique()}")
    
    # Remove columns: email, consejo_regional, registro, fecha
    columns_to_remove = ['email', 'consejo_regional', 'registro', 'fecha']
    for col in columns_to_remove:
        if col in df.columns:
            df = df.drop(columns=[col])
            print(f"Removed column: {col}")
    
    # Normalize Unicode in specialty field first
    print("Normalizing Unicode characters...")
    df['specialty'] = df['specialty'].apply(normalize_unicode)
    
    # Normalize name fields
    print("Normalizing name fields...")
    name_fields = ['apellidos', 'nombres', 'apellido_paterno', 'apellido_materno']
    for field in name_fields:
        if field in df.columns:
            df[field] = df[field].apply(normalize_name)
    
    # Normalize specialty field (for display)
    df['specialty'] = df['specialty'].apply(lambda x: normalize_name(x) if pd.notna(x) and x != '' else x)
    
    # Fields that should be consolidated into arrays (removed 'registro' since we're dropping it)
    array_fields = ['specialty', 'specialty_id', 'tipo', 'codigo']
    
    # Fields that should remain as single values (take first non-null value)
    single_fields = [col for col in df.columns if col not in array_fields and col != 'cmp']
    
    # Group by CMP and consolidate
    consolidated_rows = []
    
    for cmp_id, group in df.groupby('cmp'):
        row_dict = {'cmp': cmp_id}
        
        # For array fields, collect unique values
        for field in array_fields:
            values = group[field].dropna().unique().tolist()
            # Remove empty strings
            values = [v for v in values if v != '']
            
            # Always store as array format for CSV (pipe-separated for CSV compatibility)
            if len(values) > 0:
                # Convert to proper types for specialty_id (should be numeric or string)
                if field == 'specialty_id':
                    # Try to convert to int if possible, otherwise keep as string
                    try:
                        values = [int(v) if str(v).isdigit() else v for v in values]
                    except:
                        pass
                
                # Store as pipe-separated string for CSV compatibility
                # Format: [value1|value2|value3] to indicate it's an array
                values_str = '|'.join(str(v) for v in values)
                row_dict[field] = f'[{values_str}]'
            else:
                row_dict[field] = '[]'
        
        # For single fields, take the first non-null value
        for field in single_fields:
            value = group[field].dropna().iloc[0] if not group[field].dropna().empty else ''
            row_dict[field] = value
        
        consolidated_rows.append(row_dict)
    
    # Create consolidated dataframe
    consolidated_df = pd.DataFrame(consolidated_rows)
    
    # Reorder columns to match original order (excluding removed columns)
    original_order = [col for col in df.columns.tolist() if col not in columns_to_remove]
    consolidated_df = consolidated_df[original_order]
    
    print(f"Consolidated rows: {len(consolidated_df)}")
    print(f"Reduction: {len(df) - len(consolidated_df)} rows ({100 * (len(df) - len(consolidated_df)) / len(df):.2f}%)")
    
    # Write CSV - arrays are already in pipe-separated format [value1|value2]
    print(f"Writing CSV to {output_file}...")
    consolidated_df.to_csv(output_file, index=False, quoting=csv.QUOTE_MINIMAL)
    
    print(f"Saved consolidated data to {output_file}")
    
    # Show some examples
    print("\nExample consolidated entries:")
    for i, row in consolidated_df.head(3).iterrows():
        print(f"\nCMP: {row['cmp']}")
        print(f"  Name: {row['nombres']} {row['apellidos']}")
        specialty_str = str(row['specialty'])
        if specialty_str.startswith('[') and specialty_str.endswith(']'):
            # Parse pipe-separated array format
            values = specialty_str[1:-1].split('|') if len(specialty_str) > 2 else []
            print(f"  Specialties ({len(values)}): {values[:3]}{'...' if len(values) > 3 else ''}")
        else:
            print(f"  Specialty: {row['specialty']}")

if __name__ == "__main__":
    input_file = "doctors_data.csv"
    output_file = "doctors_data_clean.csv"
    
    consolidate_doctors_data(input_file, output_file)