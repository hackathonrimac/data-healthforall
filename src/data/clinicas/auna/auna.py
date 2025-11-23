#!/usr/bin/env python3
"""
Auna Doctor Data Parser
Extracts unique doctors and their related data from auna.html

JSON OUTPUT FORMAT:
==================

The script generates auna_doctores.json with the following structure:

{
  "total_doctors": 1015,
  "doctors": [
    {
      "name": "Doctor Name",
      "cmp": "CMP Code",
      "rne": "RNE Code",
      "specialties": "Comma-separated specialties",
      "locations": "Comma-separated locations",
      "photo": "Photo URL",
      "slug": "URL slug",
      "profile_url": "Full profile URL",
      "raw_data": {
        // Complete original data structure (see below)
      }
    }
  ]
}

RAW_DATA STRUCTURE:
==================

Each doctor's raw_data contains the complete original JSON structure with:

BASIC INFORMATION:
  - DNI: str - National ID number (e.g., "40347059")
  - name: str - Full name (e.g., "Barrionuevo Poquet Grisell Patricia")
  - gender: str - Gender (e.g., "Femenino", "Masculino")
  - prefix: str - Title prefix (e.g., "Dra", "Dr")
  - urlPath: str - Relative URL path (e.g., "/pe/staff-medico/barrionuevo-poquet-grisell-patricia")

MEDICAL LICENSING:
  - typeMedicalLicensing: str - License type (e.g., "CMP", "RNE")
  - medicalLicenseNumber: str - License number (CMP/RNE code, e.g., "41119")
  - typeOfScheduling: str - Scheduling type (e.g., "APP")

SPECIALTIES:
  - commercialSpecialties: str - Primary commercial specialty (e.g., "Cardiología")
  - specialties: list - Array of specialty objects
    Each specialty: {
      "attributes": {
        "name": "Specialty Name"
      }
    }
  - normalizedSpecialties: list - Normalized specialty names
  - normalizedSubspecialties: list - Normalized subspecialty names

LOCATIONS (SITES):
  - sites: {
      "data": [
        {
          "id": 99,
          "attributes": {
            "name": "Auna Arequipa (Vallesur) - Clínica",
            "address": "Av. La Salle 116 Arequipa, Arequipa",
            "email": "servicioalcliente.vallesur@auna.pe",
            "schedule": "Lunes a viernes de 09:00 a.m. a 5:30 p.m...",
            "urlMaps": "http://maps.google.com/maps?q=-16.4011097,-71.5251508",
            "urlPath": "/pe/sedes/clinica-vallesur",
            "online": false,
            "city": {
              "data": {
                "attributes": {
                  "name": "Arequipa"
                }
              }
            },
            "specialties": {
              "data": [
                {
                  "attributes": {
                    "name": "Anestesiología"
                  }
                },
                // ... more specialties available at this site
              ]
            }
          }
        }
      ]
    }

PROFILE IMAGES:
  - profileImages: {
      "desktop": {
        "data": {
          "attributes": {
            "url": "https://web-auna-backend-prd-images.s3.amazonaws.com/40347059_57fdc3e546.png"
          }
        }
      },
      "mobile": {
        "data": {
          "attributes": {
            "url": "https://web-auna-backend-prd-images.s3.amazonaws.com/40347059_mobile_d4efeb7f2b.png"
          }
        }
      }
    }

EDUCATION:
  - undergraduate: {
      "id": ...,
      "title": "Degree Title",
      "university": "University Name",
      "endDate": "YYYY-MM-DD"
    }
  - postgraduate: list - Array of postgraduate education objects
  - languages: list - Array of language objects
    Each language: {
      "id": 14130,
      "name": "Español"
    }

OTHER FIELDS:
  - city: {
      "data": {
        "attributes": {
          "name": "Arequipa"
        }
      }
    }
  - areaOfInterest: str | null - Area of interest
  - coordinator: str | null - Coordinator information
  - medicalUnit: str | null - Medical unit
  - eid: str | null - Event ID

DATA ACCESS EXAMPLES:
====================

# Load JSON
import json
with open('auna_doctores.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Access normalized fields
doctor = data['doctors'][0]
print(doctor['name'])  # "Barrionuevo Poquet Grisell Patricia"
print(doctor['cmp'])    # "41119" (if extracted)

# Access raw data
raw = doctor['raw_data']
print(raw['DNI'])                           # "40347059"
print(raw['medicalLicenseNumber'])          # "41119" (CMP code)
print(raw['commercialSpecialties'])         # "Cardiología"
print(raw['profileImages']['desktop']['data']['attributes']['url'])

# Access sites/locations
for site in raw['sites']['data']:
    site_attrs = site['attributes']
    print(site_attrs['name'])      # "Auna Arequipa (Vallesur) - Clínica"
    print(site_attrs['address'])   # "Av. La Salle 116 Arequipa, Arequipa"
    print(site_attrs['email'])     # "servicioalcliente.vallesur@auna.pe"
    
    # Get specialties available at this site
    site_specialties = site_attrs['specialties']['data']
    for spec in site_specialties:
        print(spec['attributes']['name'])

# Access specialties
for specialty in raw['specialties']:
    print(specialty['attributes']['name'])

# Access education
if raw.get('undergraduate'):
    print(raw['undergraduate']['title'])
    print(raw['undergraduate']['university'])

for pg in raw.get('postgraduate', []):
    print(pg['title'])  # if available

NOTES:
======
- The normalized fields (name, cmp, rne, specialties, locations, photo, slug, profile_url)
  are extracted and simplified, but may be empty if the extraction logic didn't find them.
- The raw_data contains the complete original structure with all nested information.
- medicalLicenseNumber contains the CMP code when typeMedicalLicensing is "CMP".
- Sites contain detailed information including addresses, schedules, and available specialties.
- Profile images are available in both desktop and mobile formats.
- Each doctor can have multiple sites (locations) where they practice.
- Each site can have multiple specialties available.
"""

import re
import json
import csv
from pathlib import Path
from typing import List, Dict, Set, Any, Optional


def extract_next_data(html_content: str) -> Optional[Dict]:
    """Extract JSON data from __NEXT_DATA__ script tag."""
    match = re.search(
        r'<script id="__NEXT_DATA__".*?>(.*?)</script>',
        html_content,
        re.DOTALL
    )
    if not match:
        return None
    
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def is_clinic_or_location_name(name: str) -> bool:
    """Check if a name is likely a clinic/location rather than a doctor."""
    if not name:
        return True
    
    name_lower = name.lower()
    clinic_keywords = [
        'auna', 'clínica', 'clinica', 'centro médico', 'centro medico',
        'hospital', 'sede', 'guardia civil', 'delgado', 'arequipa',
        'piura', 'chiclayo', 'oncosalud', 'vallesur'
    ]
    
    return any(keyword in name_lower for keyword in clinic_keywords)


def find_doctors_in_data(data: Any, path: str = "", results: List[Dict] = None, depth: int = 0) -> List[Dict]:
    """Recursively search for doctor data in the JSON structure."""
    if results is None:
        results = []
    
    # Limit recursion depth to avoid too many false positives
    if depth > 20:
        return results
    
    if isinstance(data, dict):
        # Check if this dict looks like doctor data
        # Must have a name field AND at least one other doctor-related field
        name_fields = ['name', 'fullname', 'fullName', 'firstName', 'lastName']
        doctor_fields = ['cmp', 'CMP', 'rne', 'RNE', 'specialty', 'especialidad',
                        'specialties', 'especialidades', 'location', 'sede', 'sedes',
                        'photo', 'image', 'url_image', 'profile', 'slug', 'medicalCode']
        
        has_name = any(key in data for key in name_fields)
        has_doctor_field = any(key in data for key in doctor_fields)
        
        # More strict: must have name AND at least one doctor field
        if has_name and has_doctor_field:
            # Extract name to verify it's not empty/null
            name_val = data.get('name') or data.get('fullname') or data.get('fullName') or ''
            if isinstance(name_val, dict):
                name_val = name_val.get('name') or name_val.get('title') or name_val.get('attributes', {}).get('name') or ''
            
            name_str = str(name_val).strip() if name_val else ''
            
            # Filter out clinic/location names
            if (name_str and 
                name_str.lower() not in ['null', 'none', ''] and
                not is_clinic_or_location_name(name_str)):
                # This looks like a doctor object
                results.append({
                    'path': path,
                    'data': data
                })
        
        # Recursively search nested structures
        for key, value in data.items():
            find_doctors_in_data(value, f"{path}.{key}" if path else key, results, depth + 1)
    
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            find_doctors_in_data(item, f"{path}[{idx}]", results, depth + 1)
    
    return results


def normalize_doctor_data(doctor_obj: Dict) -> Dict:
    """Normalize doctor data into a consistent format from raw_data structure."""
    data = doctor_obj.get('data', {})
    
    # Extract name
    name = str(data.get('name', '')).strip()
    
    # Extract CMP/RNE from medicalLicenseNumber based on typeMedicalLicensing
    type_licensing = data.get('typeMedicalLicensing', '')
    medical_license = str(data.get('medicalLicenseNumber', '')).strip()
    
    cmp_code = ''
    rne_code = ''
    if type_licensing == 'CMP':
        cmp_code = medical_license
    elif type_licensing == 'RNE':
        rne_code = medical_license
    elif medical_license:
        # If type not specified but license exists, assume CMP
        cmp_code = medical_license
    
    # Extract specialties from specialties array
    def extract_specialty_names(spec_data):
        """Recursively extract specialty names from nested structures."""
        names = []
        if isinstance(spec_data, str):
            names.append(spec_data)
        elif isinstance(spec_data, dict):
            # Check for attributes.name structure
            if 'attributes' in spec_data:
                name = spec_data['attributes'].get('name') or spec_data['attributes'].get('title') or ''
                if name:
                    names.append(name)
            # Also check direct name fields
            name = spec_data.get('name') or spec_data.get('title') or ''
            if name:
                names.append(name)
            # Check if there's a 'data' array
            if 'data' in spec_data and isinstance(spec_data['data'], list):
                for item in spec_data['data']:
                    names.extend(extract_specialty_names(item))
        elif isinstance(spec_data, list):
            for item in spec_data:
                names.extend(extract_specialty_names(item))
        return names
    
    # Get specialties from specialties field
    specialties_list = data.get('specialties', [])
    specialty_names = extract_specialty_names(specialties_list)
    
    # Also check commercialSpecialties
    commercial_spec = data.get('commercialSpecialties', '')
    if commercial_spec and commercial_spec not in specialty_names:
        specialty_names.insert(0, commercial_spec)
    
    # Also check normalizedSpecialties
    normalized_specs = data.get('normalizedSpecialties', [])
    if isinstance(normalized_specs, list):
        for spec in normalized_specs:
            if isinstance(spec, dict):
                spec_name = spec.get('name') or spec.get('title') or ''
            else:
                spec_name = str(spec)
            if spec_name and spec_name not in specialty_names:
                specialty_names.append(spec_name)
    
    specialties_str = ', '.join(str(s).strip() for s in specialty_names if s and str(s).strip())
    
    # Extract locations from sites
    sites_data = data.get('sites', {})
    site_names = []
    if isinstance(sites_data, dict) and 'data' in sites_data:
        for site in sites_data.get('data', []):
            if isinstance(site, dict) and 'attributes' in site:
                site_name = site['attributes'].get('name', '')
                if site_name:
                    site_names.append(site_name)
    locations_str = ', '.join(site_names)
    
    # Extract photo from profileImages
    photo = ''
    profile_images = data.get('profileImages', {})
    if isinstance(profile_images, dict):
        # Try desktop first, then mobile
        desktop = profile_images.get('desktop', {})
        if isinstance(desktop, dict) and desktop.get('data'):
            attrs = desktop['data'].get('attributes', {})
            if attrs:
                photo = attrs.get('url', '')
        
        if not photo:
            mobile = profile_images.get('mobile', {})
            if isinstance(mobile, dict) and mobile.get('data'):
                attrs = mobile['data'].get('attributes', {})
                if attrs:
                    photo = attrs.get('url', '')
    
    # Extract slug from urlPath
    url_path = data.get('urlPath', '')
    slug = ''
    if url_path:
        # Extract slug from path like "/pe/staff-medico/barrionuevo-poquet-grisell-patricia"
        parts = url_path.strip('/').split('/')
        if len(parts) >= 3 and parts[1] == 'staff-medico':
            slug = parts[2]
    
    # Build profile URL
    profile_url = ''
    if slug:
        profile_url = f"https://auna.org{url_path}" if url_path.startswith('/') else f"https://auna.org/pe/staff-medico/{slug}"
    elif url_path:
        profile_url = f"https://auna.org{url_path}" if url_path.startswith('/') else url_path
    
    return {
        'name': name,
        'cmp': cmp_code,
        'rne': rne_code,
        'specialties': specialties_str,
        'locations': locations_str,
        'photo': photo,
        'slug': slug,
        'profile_url': profile_url,
        'raw_data': json.dumps(data, ensure_ascii=False)
    }


def extract_unique_doctors(html_file: str) -> List[Dict]:
    """Extract unique doctors from the HTML file."""
    print(f"Reading HTML file: {html_file}")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("Extracting __NEXT_DATA__ JSON...")
    next_data = extract_next_data(html_content)
    if not next_data:
        print("ERROR: Could not find __NEXT_DATA__ in HTML")
        return []
    
    print("Searching for doctor data in JSON structure...")
    doctor_objects = find_doctors_in_data(next_data)
    print(f"Found {len(doctor_objects)} potential doctor objects")
    
    # Normalize and deduplicate doctors
    unique_doctors = {}
    seen_names = set()
    
    for doctor_obj in doctor_objects:
        normalized = normalize_doctor_data(doctor_obj)
        name = normalized['name']
        
        if not name or name.lower() in ['', 'null', 'none']:
            continue
        
        # Skip if it's a clinic/location name
        if is_clinic_or_location_name(name):
            continue
        
        # Use name + CMP as unique key if CMP exists, otherwise just name
        unique_key = f"{name.lower()}_{normalized['cmp']}" if normalized['cmp'] else name.lower()
        
        if unique_key not in unique_doctors:
            unique_doctors[unique_key] = normalized
            seen_names.add(name.lower())
        else:
            # Merge data if we have more complete info
            existing = unique_doctors[unique_key]
            if not existing['cmp'] and normalized['cmp']:
                existing['cmp'] = normalized['cmp']
            if not existing['rne'] and normalized['rne']:
                existing['rne'] = normalized['rne']
            if not existing['specialties'] and normalized['specialties']:
                existing['specialties'] = normalized['specialties']
            if not existing['locations'] and normalized['locations']:
                existing['locations'] = normalized['locations']
            if not existing['photo'] and normalized['photo']:
                existing['photo'] = normalized['photo']
            if not existing['slug'] and normalized['slug']:
                existing['slug'] = normalized['slug']
                existing['profile_url'] = normalized['profile_url']
    
    doctors_list = list(unique_doctors.values())
    print(f"Extracted {len(doctors_list)} unique doctors")
    
    return doctors_list


def save_to_csv(doctors: List[Dict], filename: str = "auna_doctores.csv"):
    """Save doctors data to CSV file."""
    if not doctors:
        print("No doctors to save")
        return
    
    fieldnames = [
        'name', 'cmp', 'rne', 'specialties', 'locations', 
        'photo', 'slug', 'profile_url'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        
        for doctor in doctors:
            row = {k: doctor.get(k, '') for k in fieldnames}
            writer.writerow(row)
    
    print(f"✅ CSV saved: {filename} ({len(doctors)} doctors)")


def save_to_json(doctors: List[Dict], filename: str = "auna_doctores.json"):
    """Save doctors data to JSON file with full structure."""
    if not doctors:
        print("No doctors to save")
        return
    
    # Create a clean JSON structure
    output_data = {
        'total_doctors': len(doctors),
        'doctors': []
    }
    
    for doctor in doctors:
        # Parse raw_data if available to include original structure
        doctor_entry = {
            'name': doctor.get('name', ''),
            'cmp': doctor.get('cmp', ''),
            'rne': doctor.get('rne', ''),
            'specialties': doctor.get('specialties', ''),
            'locations': doctor.get('locations', ''),
            'photo': doctor.get('photo', ''),
            'slug': doctor.get('slug', ''),
            'profile_url': doctor.get('profile_url', '')
        }
        
        # Try to include raw data if available
        raw_data = doctor.get('raw_data', '')
        if raw_data:
            try:
                doctor_entry['raw_data'] = json.loads(raw_data)
            except:
                doctor_entry['raw_data'] = raw_data
        
        output_data['doctors'].append(doctor_entry)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON saved: {filename} ({len(doctors)} doctors)")


def main():
    html_file = Path(__file__).parent / "auna.html"
    
    if not html_file.exists():
        print(f"ERROR: File not found: {html_file}")
        return
    
    doctors = extract_unique_doctors(str(html_file))
    save_to_csv(doctors)
    save_to_json(doctors)


if __name__ == "__main__":
    main()

