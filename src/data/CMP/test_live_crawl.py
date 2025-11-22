#!/usr/bin/env python3
"""
Quick test to verify the crawler can fetch from the live website.
"""

from crawler import CMPCrawler

def test_live_crawl():
    """Test crawling from live website."""
    print("=" * 60)
    print("Testing Live Website Crawl")
    print("=" * 60)
    
    # Create crawler (default: use live site)
    crawler = CMPCrawler()
    
    print(f"\nBase URL: {crawler.base_url}")
    print(f"Use local files: {crawler.use_local_files}")
    
    # Test fetching specialties page
    print("\n[Test 1] Fetching specialties page...")
    specialties_url = f"{crawler.base_url}lista-especialidad.php?key=17"
    print(f"URL: {specialties_url}")
    
    html = crawler._read_html(specialties_url)
    if html:
        print(f"✓ Successfully fetched page ({len(html)} characters)")
        
        # Try to parse specialties
        print("\n[Test 2] Parsing specialties...")
        specialties = crawler.parse_specialties()
        if specialties:
            print(f"✓ Found {len(specialties)} specialties")
            print("\nFirst 3 specialties:")
            for spec in specialties[:3]:
                print(f"  - {spec['name']} (ID: {spec['id']})")
        else:
            print("✗ No specialties found")
    else:
        print("✗ Failed to fetch page")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
    print("\nTo run full crawl:")
    print("  python3 crawler.py --delay 2.0 --max 5")

if __name__ == '__main__':
    test_live_crawl()

