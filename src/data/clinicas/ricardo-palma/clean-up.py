#!/usr/bin/env python3
"""
Script to clean CSV files by removing specified columns.
"""

import csv
import sys
import argparse
from pathlib import Path


def remove_columns(input_file, output_file, columns_to_remove):
    """
    Remove specified columns from a CSV file.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file (can be same as input)
        columns_to_remove: List of column names to remove
    """
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found.")
        return False
    
    # Read the CSV and write without the specified columns
    with open(input_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Get all fieldnames except the ones to remove
        original_columns = reader.fieldnames
        if not original_columns:
            print("Error: CSV file has no header row.")
            return False
        
        # Check which columns exist
        missing_columns = [col for col in columns_to_remove if col not in original_columns]
        if missing_columns:
            print(f"Warning: These columns were not found in the CSV: {missing_columns}")
        
        # Get columns to keep
        columns_to_keep = [f for f in original_columns if f not in columns_to_remove]
        
        if not columns_to_keep:
            print("Error: Cannot remove all columns from CSV.")
            return False
        
        # Write to temporary file first
        output_path = Path(output_file)
        temp_file = output_path.with_suffix('.tmp')
        
        with open(temp_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=columns_to_keep)
            writer.writeheader()
            
            rows_processed = 0
            for row in reader:
                # Create new row without the removed columns
                new_row = {k: v for k, v in row.items() if k in columns_to_keep}
                writer.writerow(new_row)
                rows_processed += 1
        
        # Replace original file if output is same as input
        if input_path == output_path:
            temp_file.replace(output_path)
        else:
            temp_file.replace(output_path)
    
    print(f"Successfully processed {rows_processed} rows.")
    print(f"Removed columns: {', '.join(columns_to_remove)}")
    print(f"Remaining columns: {', '.join(columns_to_keep)}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Remove specified columns from a CSV file.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Remove columns from a file (in-place)
  python clean_csv.py ricardo-palma.csv --remove detail_url nombre_list especialidad_list
  
  # Remove columns and save to new file
  python clean_csv.py input.csv output.csv --remove column1 column2
  
  # Remove columns interactively
  python clean_csv.py ricardo-palma.csv --remove detail_url nombre_list especialidad_list --interactive
        """
    )
    
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('output_file', nargs='?', help='Output CSV file path (default: same as input)')
    parser.add_argument('--remove', '-r', nargs='+', required=True,
                       help='Column names to remove from CSV')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Ask for confirmation before processing')
    
    args = parser.parse_args()
    
    # Set output file to input file if not specified
    output_file = args.output_file if args.output_file else args.input_file
    
    # Show what will be done
    print(f"Input file: {args.input_file}")
    print(f"Output file: {output_file}")
    print(f"Columns to remove: {', '.join(args.remove)}")
    
    if args.interactive:
        response = input("\nProceed with removing these columns? (y/n): ")
        if response.lower() not in ['y', 'yes']:
            print("Operation cancelled.")
            return
    
    # Process the file
    success = remove_columns(args.input_file, output_file, args.remove)
    
    if success:
        print("\n✓ CSV file cleaned successfully!")
    else:
        print("\n✗ Failed to clean CSV file.")
        sys.exit(1)


if __name__ == '__main__':
    main()

