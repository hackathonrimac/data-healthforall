import requests
import csv
import json
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.maisondesante.org.pe"
API_BASE = "https://api.maisondesante.org.pe"  # Based on image URL pattern
STAFF_PAGE = f"{BASE_URL}/staff-medico/"
OUTPUT_CSV = "maison_de_sante_medicos.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15",
    "Accept": "application/json, text/plain, */*",
    "Referer": STAFF_PAGE,
    "Origin": BASE_URL,
}


def try_api_endpoints():
    """Try common API endpoints to find the staff data."""
    # Based on the image URL pattern: api.maisondesante.org.pe/resources/images/medicos/67114.jpg
    # Try various endpoint patterns
    possible_endpoints = [
        # Direct API endpoints
        f"{API_BASE}/api/staff",
        f"{API_BASE}/api/medicos",
        f"{API_BASE}/api/doctors",
        f"{API_BASE}/api/horarios",
        f"{API_BASE}/api/staff-medico",
        f"{API_BASE}/api/getStaff",
        f"{API_BASE}/api/getHorarios",
        f"{API_BASE}/api/getMedicos",
        # Alternative patterns
        f"{API_BASE}/staff",
        f"{API_BASE}/medicos",
        f"{API_BASE}/doctors",
        f"{API_BASE}/horarios",
        # Citas subdomain
        "https://citas.maisondesante.org.pe/api/staff",
        "https://citas.maisondesante.org.pe/api/medicos",
        "https://citas.maisondesante.org.pe/api/horarios",
        "https://citas.maisondesante.org.pe/api/getHorarios",
        # Main domain
        f"{BASE_URL}/api/staff",
        f"{BASE_URL}/api/medicos",
        f"{BASE_URL}/api/horarios",
    ]
    
    # Try GET requests first
    for endpoint in possible_endpoints:
        try:
            print(f"Trying GET: {endpoint}")
            r = requests.get(endpoint, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                try:
                    data = r.json()
                    if data and (isinstance(data, list) or (isinstance(data, dict) and data)):
                        print(f"✓ Found working endpoint: {endpoint}")
                        return data
                except:
                    pass
        except Exception as e:
            continue
    
    # Try POST requests (some APIs use POST for queries)
    post_endpoints = [
        f"{API_BASE}/api/horarios",
        f"{API_BASE}/api/getHorarios",
        "https://citas.maisondesante.org.pe/api/getHorarios",
        f"{API_BASE}/api/staff",
    ]
    
    for endpoint in post_endpoints:
        try:
            print(f"Trying POST: {endpoint}")
            # Try with empty body or common query params
            r = requests.post(endpoint, json={}, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                try:
                    data = r.json()
                    if data and (isinstance(data, list) or (isinstance(data, dict) and data)):
                        print(f"✓ Found working endpoint (POST): {endpoint}")
                        return data
                except:
                    pass
        except Exception as e:
            continue
    
    return None


def parse_page_for_data():
    """Parse the HTML page to extract embedded data or find API calls."""
    print(f"Fetching page: {STAFF_PAGE}")
    r = requests.get(STAFF_PAGE, headers=HEADERS, timeout=15)
    r.raise_for_status()
    
    soup = BeautifulSoup(r.text, "html.parser")
    import re
    
    # Look for embedded JSON data in script tags
    scripts = soup.find_all("script")
    for script in scripts:
        if script.string:
            content = script.string
            
            # Look for API URLs (full URLs)
            api_urls = re.findall(r'https?://[^\s"\'<>()]+api[^\s"\'<>()]+', content)
            if api_urls:
                print(f"Found API URLs in script: {api_urls[:5]}")
                for url in api_urls[:10]:  # Limit to first 10
                    try:
                        resp = requests.get(url, headers=HEADERS, timeout=10)
                        if resp.status_code == 200:
                            try:
                                data = resp.json()
                                if data:
                                    print(f"✓ Found data from: {url}")
                                    return data
                            except:
                                pass
                    except:
                        continue
            
            # Look for relative API paths
            relative_paths = re.findall(r'["\'](/[^\s"\'<>()]*api[^\s"\'<>()]*)["\']', content)
            if relative_paths:
                print(f"Found relative API paths: {relative_paths[:5]}")
                for path in set(relative_paths[:10]):
                    for base in [API_BASE, BASE_URL, "https://citas.maisondesante.org.pe"]:
                        url = base + path
                        try:
                            resp = requests.get(url, headers=HEADERS, timeout=10)
                            if resp.status_code == 200:
                                try:
                                    data = resp.json()
                                    if data:
                                        print(f"✓ Found data from: {url}")
                                        return data
                                except:
                                    pass
                        except:
                            continue
            
            # Look for embedded JSON data
            json_matches = re.findall(r'\{[^{}]*"(Medico|CMP|Nombre|especialidad)"[^{}]*\}', content)
            if json_matches:
                # Try to extract larger JSON objects
                json_blocks = re.findall(r'\[[^\]]*\{[^}]*"(Medico|CMP|Nombre)"[^}]*\}[^\]]*\]', content)
                if json_blocks:
                    print("Found potential JSON data in page")
                    # Try to parse it
                    for block in json_blocks[:3]:
                        try:
                            data = json.loads(block)
                            if isinstance(data, list) and len(data) > 0:
                                print("✓ Found embedded JSON data")
                                return data
                        except:
                            continue
    
    return None


def try_horarios_endpoint():
    """Try the horarios endpoint with different parameters since the page shows schedules."""
    # The correct endpoint is /api/get_horario_list (POST)
    endpoint = f"{API_BASE}/api/get_horario_list"
    
    try:
        print(f"Trying horarios endpoint: {endpoint}")
        # Try POST with empty body first
        r = requests.post(endpoint, json={}, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            try:
                data = r.json()
                if data and (isinstance(data, list) or (isinstance(data, dict) and data)):
                    print(f"✓ Found data from horarios endpoint: {endpoint}")
                    return data
            except:
                pass
    except Exception as e:
        print(f"  Error: {e}")
    
    # Fallback: try other endpoints
    horarios_endpoints = [
        f"{API_BASE}/api/horarios",
        f"{API_BASE}/api/getHorarios",
        "https://citas.maisondesante.org.pe/api/getHorarios",
        "https://citas.maisondesante.org.pe/api/horarios",
    ]
    
    # Try with different parameter combinations
    param_combinations = [
        {},  # No params
        {"sede": ""},  # Empty sede
        {"fecha": ""},  # Empty fecha (page says if fecha is empty, shows month schedule)
        {"sede": "", "fecha": ""},
        {"filter": ""},
    ]
    
    for endpoint in horarios_endpoints:
        for params in param_combinations:
            try:
                print(f"Trying horarios: {endpoint} with params: {params}")
                # Try GET
                r = requests.get(endpoint, params=params, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    try:
                        data = r.json()
                        if data and (isinstance(data, list) or (isinstance(data, dict) and data)):
                            print(f"✓ Found data from horarios endpoint: {endpoint}")
                            return data
                    except:
                        pass
                
                # Try POST
                r = requests.post(endpoint, json=params, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    try:
                        data = r.json()
                        if data and (isinstance(data, list) or (isinstance(data, dict) and data)):
                            print(f"✓ Found data from horarios endpoint (POST): {endpoint}")
                            return data
                    except:
                        pass
            except:
                continue
    
    return None


def get_doctors():
    """Main function to get all doctors."""
    # First try horarios endpoint (most likely based on page content)
    data = try_horarios_endpoint()
    
    if data is None:
        # Try other API endpoints
        data = try_api_endpoints()
    
    if data is None:
        # Try parsing the page
        data = parse_page_for_data()
    
    if data is None:
        raise Exception("Could not find API endpoint. Please inspect the network tab in browser dev tools.")
    
    # Handle different response formats
    if isinstance(data, list):
        doctors = data
    elif isinstance(data, dict):
        doctors = data.get("data", data.get("doctors", data.get("medicos", [])))
        if not doctors:
            # Maybe the whole dict is the data
            doctors = [data]
    else:
        raise Exception(f"Unexpected data format: {type(data)}")
    
    if doctors:
        print(f"Example doctor keys: {doctors[0].keys() if isinstance(doctors[0], dict) else 'Not a dict'}")
    
    return doctors


def save_csv(doctors):
    """Save doctors to CSV with all fields including schedule data."""
    if not doctors:
        print("No doctors to save")
        return
    
    # Field names based on the API response structure
    fieldnames = [
        "cmp", "nombre", "especialidad", "sexo", "foto",
        "sucursal", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado",
        "dia01", "dia02", "dia03", "dia04", "dia05", "dia06",
        "horario_inicio", "horario_fin"
    ]
    
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";", extrasaction="ignore")
        writer.writeheader()
        
        for d in doctors:
            # Extract basic doctor info
            cmp_val = d.get("CMP") or d.get("cmp") or ""
            nombre = d.get("Medico") or d.get("medico") or d.get("nombre") or ""
            especialidad = d.get("Nombre") or d.get("nombre") or d.get("especialidad") or ""
            sexo = d.get("Sexo") or d.get("sexo") or ""
            
            # Construct photo URL
            url_path = d.get("URL") or d.get("url") or ""
            if url_path:
                if url_path.startswith("http"):
                    foto = url_path
                else:
                    # Construct full URL: api.maisondesante.org.pe/resources/images/medicos/{url_path}
                    foto = f"{API_BASE}/resources/images/medicos/{url_path}"
            else:
                # Fallback: try to construct from CMP
                if cmp_val:
                    foto = f"{API_BASE}/resources/images/medicos/{cmp_val}.jpg"
                else:
                    foto = ""
            
            # Extract rides (schedules) - create one row per ride
            rides = d.get("rides") or []
            
            if not rides:
                # If no rides, create one row with just doctor info
                row = {
                    "cmp": cmp_val,
                    "nombre": nombre,
                    "especialidad": especialidad,
                    "sexo": sexo,
                    "foto": foto,
                }
                writer.writerow(row)
            else:
                # Create one row per ride (schedule)
                for ride in rides:
                    row = {
                        "cmp": cmp_val,
                        "nombre": nombre,
                        "especialidad": especialidad,
                        "sexo": sexo,
                        "foto": foto,
                        "sucursal": ride.get("Sucursal") or ride.get("sucursal") or "",
                        "lunes": ride.get("Lunes") or "",
                        "martes": ride.get("Martes") or "",
                        "miercoles": ride.get("Miercoles") or "",
                        "jueves": ride.get("Jueves") or "",
                        "viernes": ride.get("Viernes") or "",
                        "sabado": ride.get("Sabado") or "",
                        "dia01": ride.get("dia01") or "",
                        "dia02": ride.get("dia02") or "",
                        "dia03": ride.get("dia03") or "",
                        "dia04": ride.get("dia04") or "",
                        "dia05": ride.get("dia05") or "",
                        "dia06": ride.get("dia06") or "",
                        "horario_inicio": ride.get("HorarioI") or ride.get("horarioI") or "",
                        "horario_fin": ride.get("HorarioF") or ride.get("horarioF") or "",
                    }
                    writer.writerow(row)
    
    print(f"Saved → {OUTPUT_CSV}")


if __name__ == "__main__":
    print("=" * 60)
    print("Maison de Santé - Staff Médico Scraper")
    print("=" * 60)
    
    try:
        docs = get_doctors()
        print(f"\nFound {len(docs)} doctors")
        save_csv(docs)
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease:")
        print("1. Open https://www.maisondesante.org.pe/staff-medico/ in your browser")
        print("2. Open Developer Tools (F12) > Network tab")
        print("3. Filter by XHR/Fetch")
        print("4. Reload the page and look for API calls")
        print("5. Share the API endpoint URL and response format")

