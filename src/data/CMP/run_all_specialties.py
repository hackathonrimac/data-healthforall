#!/usr/bin/env python3
"""
Run all specialties one by one sequentially.
"""

import sys
import time
from crawler import CMPCrawler

def run_all_specialties(delay=1.0, save_interval=10, start_from=1):
    """Process all specialties one at a time, starting from a specific index."""
    
    print("=" * 80)
    print("CMP Crawler - Processing All Specialties Sequentially")
    print("=" * 80)
    print()
    
    # Create crawler
    crawler = CMPCrawler()
    
    # Get all specialties
    print("Fetching specialties list...")
    specialties = crawler.parse_specialties()
    
    if not specialties:
        print("ERROR: No specialties found!")
        return
    
    total = len(specialties)
    
    # Validate start_from
    if start_from < 0 or start_from >= total:
        print(f"ERROR: start_from index {start_from} is out of range (0-{total-1})")
        return
    
    specialties_to_process = total - start_from
    print(f"Found {total} specialties total")
    print(f"Starting from specialty index {start_from}")
    print(f"Will process {specialties_to_process} specialties (indices {start_from} to {total - 1})")
    print()
    
    # Process each specialty starting from start_from index
    for position, idx in enumerate(range(start_from, total), start=1):
        specialty = specialties[idx]
        print("=" * 80)
        print(f"Processing specialty {position}/{specialties_to_process} (index {idx}/{total-1}): {specialty['name']}")
        print("=" * 80)
        print()
        
        try:
            # Process this specialty
            crawler.crawl_all(
                specialty_index=idx,
                delay=delay,
                max_workers=2,
                save_interval=save_interval,
                check_duplicates=True
            )
            
            print()
            print(f"✓ Completed specialty {position}/{specialties_to_process}: {specialty['name']}")
            print(f"  Total doctors collected so far: {len(crawler.doctors_data)}")
            print()
            
            # Small delay between specialties
            if position < specialties_to_process:
                print("Waiting 2 seconds before next specialty...")
                time.sleep(2)
                print()
            
        except KeyboardInterrupt:
            print()
            print("=" * 80)
            print("INTERRUPTED by user")
            print(f"Stopped at specialty {position}/{specialties_to_process} (index {idx}): {specialty['name']}")
            print(f"To resume, run:")
            print(f"  python3 run_all_specialties.py --start-from {idx} --delay {delay}")
            print("=" * 80)
            sys.exit(1)
            
        except Exception as e:
            print()
            print(f"✗ ERROR processing specialty {position}/{specialties_to_process}: {e}")
            print(f"  Continuing to next specialty...")
            print()
            time.sleep(2)
            continue
    
    # Final summary
    print()
    print("=" * 80)
    print("ALL SPECIALTIES COMPLETED!")
    print("=" * 80)
    print(f"Total specialties processed: {specialties_to_process} (indices {start_from} to {total-1})")
    print(f"Total doctors collected: {len(crawler.doctors_data)}")
    print()
    print("Final save...")
    crawler.save_to_csv()
    crawler.save_to_json()
    print("✓ Done!")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Process all specialties sequentially')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--save-interval', type=int, default=10,
                       help='Save every N records (default: 10)')
    parser.add_argument('--start-from', type=int, default=1,
                       help='Start from this specialty index (default: 1, skips first specialty)')
    
    args = parser.parse_args()
    
    run_all_specialties(
        delay=args.delay,
        save_interval=args.save_interval,
        start_from=args.start_from
    )

