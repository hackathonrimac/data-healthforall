#!/usr/bin/env python3
"""
Monitor crawler progress by watching the output files.
"""

import json
import csv
import time
from pathlib import Path

def monitor_progress():
    csv_file = Path("doctors_data.csv")
    json_file = Path("doctors_data.json")
    
    print("Monitoring crawler progress...")
    print("Press Ctrl+C to stop\n")
    
    last_count = 0
    
    try:
        while True:
            # Check CSV
            csv_count = 0
            if csv_file.exists():
                try:
                    with open(csv_file, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        csv_count = sum(1 for _ in reader)
                except:
                    pass
            
            # Check JSON
            json_count = 0
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        json_count = len(data)
                except:
                    pass
            
            # Show progress
            current_count = max(csv_count, json_count)
            if current_count > last_count:
                new_records = current_count - last_count
                print(f"✓ Progress: {current_count} doctors collected (+{new_records} new)")
                last_count = current_count
            elif current_count > 0:
                print(f"⏳ Current: {current_count} doctors (waiting for updates...)")
            
            # Show file sizes
            if csv_file.exists():
                size_mb = csv_file.stat().st_size / (1024 * 1024)
                print(f"   CSV: {csv_count} rows, {size_mb:.2f} MB")
            if json_file.exists():
                size_mb = json_file.stat().st_size / (1024 * 1024)
                print(f"   JSON: {json_count} records, {size_mb:.2f} MB")
            
            print()
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        print("\n✓ Monitoring stopped")

if __name__ == '__main__':
    monitor_progress()

