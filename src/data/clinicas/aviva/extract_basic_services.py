import csv

def extract_unique_basic_services(csv_file):
    """Extract unique basicService values from the CSV file."""
    services = set()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            service = row['basicService'].strip()
            if service:
                services.add(service)
    
    return sorted(services)


def main():
    csv_file = 'aviva_todas_sedes_doctores.csv'
    unique_services = extract_unique_basic_services(csv_file)
    
    print("Unique basicService list:")
    print("-" * 50)
    for service in unique_services:
        print(service)
    
    print(f"\n\nTotal unique services: {len(unique_services)}")
    
    # Also save to a text file
    with open('basic_services_list.txt', 'w', encoding='utf-8') as f:
        for service in unique_services:
            f.write(service + '\n')
    
    print(f"\nList saved to: basic_services_list.txt")
    
    # Also create a Python list format
    with open('basic_services_list.py', 'w', encoding='utf-8') as f:
        f.write("# Unique basicService list from aviva_todas_sedes_doctores.csv\n")
        f.write("BASIC_SERVICES = [\n")
        for service in unique_services:
            f.write(f'    "{service}",\n')
        f.write("]\n")
    
    print(f"Python list saved to: basic_services_list.py")


if __name__ == "__main__":
    main()

