#!/usr/bin/env python3
"""
Test script to demonstrate the crawler with local HTML files.
"""

from crawler import CMPCrawler
import json

def test_with_local_files():
    """Test the crawler with local HTML files."""
    print("=" * 60)
    print("Testing CMP Crawler with Local Files")
    print("=" * 60)
    
    # Create crawler instance
    crawler = CMPCrawler(use_local_files=True)
    
    # Test 1: Parse specialties
    print("\n[Test 1] Parsing specialties from cmp.html...")
    specialties = crawler.parse_specialties('cmp.html')
    print(f"Found {len(specialties)} specialties")
    
    if specialties:
        print("\nFirst 5 specialties:")
        for spec in specialties[:5]:
            print(f"  - {spec['name']} (ID: {spec['id']})")
    
    # Test 2: Parse doctors from a specialty page
    print("\n[Test 2] Parsing doctors from speciality-cmp.html...")
    if specialties:
        # Use first specialty or create a dummy one
        test_specialty = specialties[0] if specialties else {
            'id': '00003',
            'key': '17',
            'name': 'ADMINISTRACIÓN DE HOSPITALES',
            'url': 'lista-medicos-especialidad.php?id=00003&key=17'
        }
        
        doctors = crawler.parse_doctors_from_specialty(
            test_specialty, 
            'speciality-cmp.html'
        )
        print(f"Found {len(doctors)} doctors")
        
        if doctors:
            print("\nFirst 3 doctors:")
            for doc in doctors[:3]:
                print(f"  - {doc['nombres']} {doc['apellido_paterno']} {doc['apellido_materno']} (CMP: {doc['cmp']})")
    
    # Test 3: Parse doctor details
    print("\n[Test 3] Parsing doctor details from dr-cmp.html...")
    if doctors:
        test_doctor = doctors[0]
        detailed = crawler.parse_doctor_detail(test_doctor, 'dr-cmp.html')
        
        print("\nDoctor details:")
        print(json.dumps(detailed, indent=2, ensure_ascii=False))
    
    # Test 4: Full crawl (limited to 1 specialty for testing)
    print("\n[Test 4] Full crawl test (1 specialty only)...")
    crawler.doctors_data = []  # Reset
    crawler.crawl_all(
        use_local_files=True,
        max_specialties=1,
        start_from_specialty=0
    )
    
    if crawler.doctors_data:
        print(f"\nCollected {len(crawler.doctors_data)} doctor records")
        print("\nSample record:")
        sample = crawler.doctors_data[0]
        print(json.dumps(sample, indent=2, ensure_ascii=False))
        
        # Save test output
        print("\n[Test 5] Saving test output...")
        crawler.save_to_csv('test_output.csv')
        crawler.save_to_json('test_output.json')
        print("Saved to test_output.csv and test_output.json")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_with_local_files()

