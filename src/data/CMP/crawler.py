#!/usr/bin/env python3
"""
CMP Doctor Data Crawler
Crawls and extracts doctor data from the CMP website structure.
"""

import re
import json
import csv
import time
import sys
import os
import requests
import urllib3
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
from typing import List, Dict, Optional, Set
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

# Disable SSL warnings for sites with certificate issues
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup logging with unbuffered output
import sys
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
    force=True
)
# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None
logger = logging.getLogger(__name__)


class CMPCrawler:
    def __init__(self, base_url: Optional[str] = None, use_local_files: bool = False, save_json: bool = False):
        """
        Initialize the crawler.
        
        Args:
            base_url: Base URL of the website (default: https://aplicaciones.cmp.org.pe/conoce_a_tu_medico/)
            use_local_files: If True, read from local HTML files instead of making HTTP requests (default: False)
            save_json: If True, save data to JSON in addition to CSV (default: False for lightweight operation)
        """
        self.base_url = base_url or "https://aplicaciones.cmp.org.pe/conoce_a_tu_medico/"
        self.use_local_files = use_local_files
        self.save_json = save_json
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        # Disable SSL verification for sites with certificate issues
        self.session.verify = False
        # Set default timeout
        self.session.timeout = (10, 30)  # (connect timeout, read timeout)
        self.doctors_data = []
        self.existing_doctors_data = []  # Store existing data to preserve it
        self.specialties = []
        self.existing_cmps: Set[str] = set()
        self.data_lock = Lock()  # Thread lock for thread-safe operations
        self.save_counter = 0
        self.last_save_time = time.time()
        self.csv_filename = "doctors_data.csv"
        self.json_filename = "doctors_data.json"
        self.last_activity_time = time.time()  # Track last activity for heartbeat
        
    def _read_html(self, url_or_path: str) -> Optional[str]:
        """Read HTML from local file or fetch from URL."""
        if self.use_local_files:
            # Try to read from local file
            path = Path(url_or_path)
            if path.exists():
                logger.info(f"Reading local file: {path}")
                return path.read_text(encoding='utf-8', errors='ignore')
            else:
                # Try to extract filename from URL
                parsed = urlparse(url_or_path)
                filename = Path(parsed.path).name
                local_path = Path(filename)
                if local_path.exists():
                    logger.info(f"Reading local file: {local_path}")
                    return local_path.read_text(encoding='utf-8', errors='ignore')
                logger.warning(f"Local file not found: {url_or_path}, trying URL...")
        
        # Fetch from URL with retry logic and better error handling
        max_retries = 3
        retry_delay = 2.0
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Fetching URL (attempt {attempt + 1}/{max_retries}): {url_or_path}")
                sys.stdout.flush()  # Force output
                
                response = self.session.get(
                    url_or_path, 
                    timeout=(10, 30)  # (connect timeout, read timeout)
                )
                response.raise_for_status()
                
                # Success - log and return
                logger.debug(f"✓ Successfully fetched {len(response.text)} characters")
                sys.stdout.flush()
                return response.text
                
            except requests.exceptions.Timeout as e:
                logger.warning(f"⏱️  Timeout fetching {url_or_path} (attempt {attempt + 1}/{max_retries}): {e}")
                sys.stdout.flush()
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    logger.info(f"   Retrying in {wait_time} seconds...")
                    sys.stdout.flush()
                    time.sleep(wait_time)  # Exponential backoff
                    continue
                else:
                    logger.error(f"✗ Failed to fetch {url_or_path} after {max_retries} attempts (timeout)")
                    sys.stdout.flush()
                    return None
                    
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"🔌 Connection error fetching {url_or_path} (attempt {attempt + 1}/{max_retries}): {e}")
                sys.stdout.flush()
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    logger.info(f"   Retrying in {wait_time} seconds...")
                    sys.stdout.flush()
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"✗ Failed to fetch {url_or_path} after {max_retries} attempts (connection error)")
                    sys.stdout.flush()
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"⚠️  Request error fetching {url_or_path} (attempt {attempt + 1}/{max_retries}): {e}")
                sys.stdout.flush()
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return None
                
            except Exception as e:
                logger.error(f"❌ Unexpected error fetching {url_or_path}: {e}")
                sys.stdout.flush()
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return None
        
        return None
    
    def parse_specialties(self, html_file: Optional[str] = None) -> List[Dict]:
        """
        Parse specialties from the landing page.
        
        Returns list of specialty dictionaries with id, name, and url.
        """
        logger.info("Parsing specialties from landing page...")
        
        # Use the specialties page URL if not using local files
        if not html_file and not self.use_local_files:
            html_file = f"{self.base_url}lista-especialidad.php?key=17"
        
        html = self._read_html(html_file or "cmp.html")
        if not html:
            logger.error("Could not read landing page HTML")
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        specialties = []
        
        # Find all specialty links in the table
        table = soup.find('table')
        if not table:
            logger.error("Could not find specialties table")
            return []
        
        rows = table.find_all('tr', class_='cabecera_tr2')
        for row in rows:
            link = row.find('a')
            if link and link.get('href'):
                href = link['href']
                # Extract specialty name from the second td
                tds = row.find_all('td')
                if len(tds) >= 2:
                    specialty_name = tds[1].get_text(strip=True)
                    
                    # Parse URL parameters
                    if 'lista-medicos-especialidad.php' in href:
                        # Extract id, key, des from URL
                        parsed = urlparse(href)
                        params = parse_qs(parsed.query)
                        
                        specialty = {
                            'id': params.get('id', [''])[0],
                            'key': params.get('key', [''])[0],
                            'name': specialty_name,
                            'url': href
                        }
                        specialties.append(specialty)
                        logger.debug(f"Found specialty: {specialty_name}")
        
        logger.info(f"Found {len(specialties)} specialties")
        self.specialties = specialties
        return specialties
    
    def parse_doctors_from_specialty(self, specialty: Dict, html_file: Optional[str] = None) -> List[Dict]:
        """
        Parse doctor links from a specialty page.
        
        Returns list of doctor dictionaries with basic info and detail URL.
        """
        logger.info(f"Parsing doctors for specialty: {specialty['name']}")
        
        # If html_file is provided, use it; otherwise construct URL
        if html_file:
            html = self._read_html(html_file)
        else:
            # Construct full URL for specialty page
            url = urljoin(self.base_url, specialty['url'])
            html = self._read_html(url)
        
        if not html:
            logger.warning(f"Could not read specialty page for {specialty['name']}")
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        doctors = []
        
        # Find the specialty name from the page
        specialty_name_elem = soup.find('p')
        if specialty_name_elem:
            specialty_text = specialty_name_elem.get_text(strip=True)
            if 'Registro:' in specialty_text:
                specialty_name = specialty_text.replace('Registro:', '').strip()
            else:
                specialty_name = specialty['name']
        else:
            specialty_name = specialty['name']
        
        # Find doctor table
        table = soup.find('table')
        if not table:
            logger.warning(f"No table found for specialty {specialty['name']}")
            return []
        
        rows = table.find_all('tr', class_='cabecera_tr2')
        for row in rows:
            link = row.find('a')
            if link and link.get('href'):
                href = link['href']
                tds = row.find_all('td')
                
                if len(tds) >= 5:
                    doctor = {
                        'detail_url': href,
                        'cmp': tds[1].get_text(strip=True),
                        'apellido_paterno': tds[2].get_text(strip=True),
                        'apellido_materno': tds[3].get_text(strip=True),
                        'nombres': tds[4].get_text(strip=True),
                        'specialty': specialty_name,
                        'specialty_id': specialty.get('id', ''),
                    }
                    doctors.append(doctor)
        
        logger.info(f"Found {len(doctors)} doctors for {specialty_name}")
        return doctors
    
    def parse_doctor_detail(self, doctor: Dict, html_file: Optional[str] = None) -> Dict:
        """
        Parse detailed information from a doctor's profile page.
        
        Returns updated doctor dictionary with all details.
        """
        logger.debug(f"Parsing details for doctor: {doctor.get('nombres', 'Unknown')}")
        
        # If html_file is provided, use it; otherwise construct URL
        if html_file:
            html = self._read_html(html_file)
        else:
            # Construct full URL for doctor detail page
            url = urljoin(self.base_url, doctor['detail_url'])
            html = self._read_html(url)
        
        if not html:
            logger.warning(f"Could not read doctor detail page")
            return doctor
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all tables
        tables = soup.find_all('table')
        
        # First table: CMP, Apellidos, Nombres
        if len(tables) > 0:
            first_table = tables[0]
            rows = first_table.find_all('tr', class_='cabecera_tr2')
            if rows:
                tds = rows[0].find_all('td')
                if len(tds) >= 3:
                    doctor['cmp'] = tds[0].get_text(strip=True)
                    doctor['apellidos'] = tds[1].get_text(strip=True)
                    doctor['nombres'] = tds[2].get_text(strip=True)
        
        # Second table: Status (HÁBIL, etc.)
        if len(tables) > 1:
            second_table = tables[1]
            rows = second_table.find_all('tr', class_='cabecera_tr2')
            if rows:
                doctor['status'] = rows[0].get_text(strip=True)
        
        # Third table: Foto, Email, Consejo Regional
        if len(tables) > 2:
            third_table = tables[2]
            rows = third_table.find_all('tr', class_='cabecera_tr2')
            if rows:
                tds = rows[0].find_all('td')
                if len(tds) >= 3:
                    # Foto
                    img = rows[0].find('img')
                    if img and img.get('src'):
                        doctor['foto_url'] = img['src']
                    
                    # Email
                    doctor['email'] = tds[1].get_text(strip=True) if len(tds) > 1 else ''
                    
                    # Consejo Regional
                    doctor['consejo_regional'] = tds[2].get_text(strip=True) if len(tds) > 2 else ''
        
        # Fourth table: Registro (specialty), Tipo, Código, Fecha
        if len(tables) > 3:
            fourth_table = tables[3]
            rows = fourth_table.find_all('tr', class_='cabecera_tr2')
            registrations = []
            for row in rows:
                tds = row.find_all('td')
                if len(tds) >= 4:
                    registration = {
                        'registro': tds[0].get_text(strip=True),
                        'tipo': tds[1].get_text(strip=True),
                        'codigo': tds[2].get_text(strip=True),
                        'fecha': tds[3].get_text(strip=True)
                    }
                    registrations.append(registration)
            
            # Store all registrations (a doctor can have multiple specialties)
            doctor['registrations'] = registrations
            
            # Also store the first registration for backward compatibility
            if registrations:
                doctor['registro'] = registrations[0]['registro']
                doctor['tipo'] = registrations[0]['tipo']
                doctor['codigo'] = registrations[0]['codigo']
                doctor['fecha'] = registrations[0]['fecha']
        
        return doctor
    
    def load_existing_records(self, csv_file: str = "doctors_data.csv", json_file: str = "doctors_data.json"):
        """
        Load existing records from CSV/JSON to preserve data.
        Returns set of CMP numbers that already exist.
        """
        # Try to load from JSON first (more complete data structure) if JSON saving is enabled
        if self.save_json:
            json_path = Path(json_file)
            if json_path.exists():
                try:
                    logger.info(f"Loading existing records from {json_file}...")
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.existing_doctors_data = data.copy()
                    logger.info(f"Loaded {len(data)} existing doctors from JSON")
                except Exception as e:
                    logger.warning(f"Error reading JSON: {e}")
        # Always check CSV (primary data source)
        csv_path = Path(csv_file)
        if csv_path.exists():
            logger.info(f"Loading existing records from {csv_file}...")
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    # Reconstruct doctor records from CSV (for compatibility)
                    csv_data = []
                    for row in reader:
                        csv_data.append(row)
                    # If we don't have JSON data, use CSV data
                    if not self.existing_doctors_data:
                        self.existing_doctors_data = csv_data
                        logger.info(f"Loaded {len(csv_data)} existing doctors from CSV")
            except Exception as e:
                logger.warning(f"Error reading CSV: {e}")
        # We no longer treat existing CMPs as duplicates across runs.
        # Duplicate checking is now limited to doctors processed in the current run.
        self.existing_cmps = set()
        return self.existing_cmps
    
    def is_duplicate(self, doctor: Dict) -> bool:
        """Check if doctor already exists based on CMP number."""
        cmp_num = doctor.get('cmp', '').strip()
        if not cmp_num:
            return False
        return cmp_num in self.existing_cmps
    
    def is_dead_doctor(self, doctor: Dict) -> bool:
        """Check if doctor is dead based on status field."""
        status = doctor.get('status', '').strip().upper()
        return status == 'FALLECIDO'
    
    def periodic_save(self, force: bool = False, save_interval: int = 30):
        """
        Save data periodically based on record count only.
        
        Args:
            force: Force save regardless of intervals
            save_interval: Save every N records (default: 10)
        """
        should_save = force or self.save_counter >= save_interval
        
        if should_save and (self.doctors_data or force):
            try:
                save_start = time.time()
                total_records = len(self.existing_doctors_data) + len(self.doctors_data)
                logger.info(f"💾 Starting save: {len(self.doctors_data)} new records (Total: {total_records})...")
                sys.stdout.flush()
                
                with self.data_lock:
                    logger.debug("  Lock acquired, saving CSV...")
                    sys.stdout.flush()
                    self._save_to_csv_internal(self.csv_filename)
                    if self.save_json:
                        logger.debug("  CSV saved, saving JSON...")
                        sys.stdout.flush()
                        self._save_to_json_internal(self.json_filename)
                    logger.debug("  Save complete, resetting counter...")
                    sys.stdout.flush()
                    self.save_counter = 0
                    self.last_save_time = time.time()
                
                save_elapsed = time.time() - save_start
                logger.info(f"✓ Save complete! ({save_elapsed:.2f}s)")
                sys.stdout.flush()
                
            except Exception as e:
                logger.error(f"✗ Error during save: {e}")
                logger.error(f"  Continuing anyway...")
                sys.stdout.flush()
                import traceback
                logger.debug(traceback.format_exc())
                # Don't reset counter on error so it will retry
    
    def _save_to_csv_internal(self, filename: str):
        """Internal CSV save method (thread-safe). Saves existing + new data."""
        try:
            # Combine existing and new data
            all_doctors = self.existing_doctors_data + self.doctors_data
            
            if not all_doctors:
                return
            
            # Flatten data for CSV (handle multiple registrations)
            flattened_data = []
            for doctor in all_doctors:
                registrations = doctor.get('registrations', [])
                if not registrations:
                    row = {
                        'cmp': doctor.get('cmp', ''),
                        'apellidos': doctor.get('apellidos', ''),
                        'nombres': doctor.get('nombres', ''),
                        'apellido_paterno': doctor.get('apellido_paterno', ''),
                        'apellido_materno': doctor.get('apellido_materno', ''),
                        'status': doctor.get('status', ''),
                        'email': doctor.get('email', ''),
                        'consejo_regional': doctor.get('consejo_regional', ''),
                        'foto_url': doctor.get('foto_url', ''),
                        'specialty': doctor.get('specialty', ''),
                        'specialty_id': doctor.get('specialty_id', ''),
                        'registro': doctor.get('registro', ''),
                        'tipo': doctor.get('tipo', ''),
                        'codigo': doctor.get('codigo', ''),
                        'fecha': doctor.get('fecha', ''),
                    }
                    flattened_data.append(row)
                else:
                    for reg in registrations:
                        row = {
                            'cmp': doctor.get('cmp', ''),
                            'apellidos': doctor.get('apellidos', ''),
                            'nombres': doctor.get('nombres', ''),
                            'apellido_paterno': doctor.get('apellido_paterno', ''),
                            'apellido_materno': doctor.get('apellido_materno', ''),
                            'status': doctor.get('status', ''),
                            'email': doctor.get('email', ''),
                            'consejo_regional': doctor.get('consejo_regional', ''),
                            'foto_url': doctor.get('foto_url', ''),
                            'specialty': reg.get('registro', doctor.get('specialty', '')),
                            'specialty_id': doctor.get('specialty_id', ''),
                            'registro': reg.get('registro', ''),
                            'tipo': reg.get('tipo', ''),
                            'codigo': reg.get('codigo', ''),
                            'fecha': reg.get('fecha', ''),
                        }
                        flattened_data.append(row)
            
            if flattened_data:
                fieldnames = flattened_data[0].keys()
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(flattened_data)
        except Exception as e:
            logger.error(f"Error in _save_to_csv_internal: {e}")
            raise
    
    def _save_to_json_internal(self, filename: str):
        """Internal JSON save method (thread-safe). Saves existing + new data."""
        try:
            # Combine existing and new data
            all_doctors = self.existing_doctors_data + self.doctors_data
            
            if not all_doctors:
                return
            
            # Write to temporary file first, then rename (atomic operation)
            temp_filename = filename + '.tmp'
            with open(temp_filename, 'w', encoding='utf-8') as f:
                json.dump(all_doctors, f, ensure_ascii=False, indent=2)
            
            # Atomic rename
            os.replace(temp_filename, filename)
        except Exception as e:
            logger.error(f"Error in _save_to_json_internal: {e}")
            # Clean up temp file if it exists
            try:
                temp_filename = filename + '.tmp'
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
            except:
                pass
            raise
    
    def process_doctor_parallel(self, doctor: Dict) -> Optional[Dict]:
        """
        Process a single doctor (for parallel execution).
        Returns None if duplicate or dead, otherwise returns detailed doctor dict.
        """
        # Check if duplicate
        if self.is_duplicate(doctor):
            logger.debug(f"Skipping duplicate doctor: CMP {doctor.get('cmp', 'Unknown')}")
            return None
        
        # Get doctor details
        detailed_doctor = self.parse_doctor_detail(doctor)
        
        # Check if dead doctor
        if self.is_dead_doctor(detailed_doctor):
            logger.debug(f"Skipping dead doctor: CMP {detailed_doctor.get('cmp', 'Unknown')} - {detailed_doctor.get('nombres', '')} {detailed_doctor.get('apellidos', '')}")
            return None
        
        # Check again after getting details (CMP might have been updated)
        if self.is_duplicate(detailed_doctor):
            logger.debug(f"Skipping duplicate doctor: CMP {detailed_doctor.get('cmp', 'Unknown')}")
            return None
        
        # Add to existing set to prevent duplicates in same run
        cmp_num = detailed_doctor.get('cmp', '').strip()
        if cmp_num:
            with self.data_lock:
                self.existing_cmps.add(cmp_num)
        
        return detailed_doctor
    
    def crawl_all(self, start_from_specialty: int = 0, max_specialties: Optional[int] = None,
                  delay: float = 1.0, use_local_files: bool = False, 
                  max_workers: int = 2, save_interval: int = 10, 
                  check_duplicates: bool = True,
                  csv_file: str = "doctors_data.csv", json_file: str = "doctors_data.json",
                  specialty_index: Optional[int] = None, save_json: Optional[bool] = None):
        """
        Crawl all specialties and doctors.
        
        Args:
            start_from_specialty: Index to start from (for resuming)
            max_specialties: Maximum number of specialties to process (None for all)
            delay: Delay between requests in seconds
            use_local_files: Whether to use local HTML files
            max_workers: Number of parallel workers for processing doctors (default: 2)
            save_interval: Save every N records (default: 10)
            check_duplicates: Whether to check for existing records
            csv_file: CSV filename for periodic saves
            json_file: JSON filename for periodic saves (only used if save_json=True)
            specialty_index: Process only this specific specialty index (None for all)
            save_json: Override instance save_json setting (None to use instance default)
        """
        self.use_local_files = use_local_files
        self.csv_filename = csv_file
        self.json_filename = json_file
        if save_json is not None:
            self.save_json = save_json
        
        # Load existing records to avoid duplicates
        if check_duplicates:
            self.load_existing_records(csv_file, json_file)
            if self.existing_cmps:
                logger.info(f"Duplicate check is limited to current run; {len(self.existing_cmps)} CMPs already processed in this session")
        
        # Parse specialties
        specialties = self.parse_specialties()
        if not specialties:
            logger.error("No specialties found. Exiting.")
            return
        
        # Process single specialty if specified
        if specialty_index is not None:
            if specialty_index < 0 or specialty_index >= len(specialties):
                logger.error(f"Specialty index {specialty_index} out of range (0-{len(specialties)-1})")
                return
            specialties = [specialties[specialty_index]]
            logger.info(f"Processing single specialty at index {specialty_index}: {specialties[0]['name']}")
        # Limit specialties if specified
        elif max_specialties:
            specialties = specialties[start_from_specialty:start_from_specialty + max_specialties]
        else:
            specialties = specialties[start_from_specialty:]
        
        worker_mode = "sequential" if max_workers == 1 else f"{max_workers} parallel workers"
        logger.info(f"Processing {len(specialties)} specialties with {worker_mode}...")
        
        # Process each specialty
        for idx, specialty in enumerate(specialties, start=1):
            logger.info(f"[{idx}/{len(specialties)}] Processing specialty: {specialty['name']}")
            
            # Get doctors from specialty page
            doctors = self.parse_doctors_from_specialty(specialty)
            
            if not doctors:
                logger.warning(f"No doctors found for {specialty['name']}")
                continue
            
            # Filter out duplicates and dead doctors before processing
            if check_duplicates:
                initial_count = len(doctors)
                doctors = [d for d in doctors if not self.is_duplicate(d)]
                logger.info(f"  {len(doctors)} new doctors to process (after duplicate check, {initial_count - len(doctors)} duplicates skipped)")
            
            # Note: Dead doctors will be filtered during processing (after we get their status)
            
            if not doctors:
                logger.info(f"  All doctors already exist, skipping...")
                continue
            
            # Process doctors (parallel if max_workers > 1, sequential otherwise)
            if max_workers > 1 and not use_local_files:
                logger.info(f"  Processing {len(doctors)} doctors with {max_workers} parallel workers...")
                sys.stdout.flush()
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # Submit all doctor processing tasks
                    future_to_doctor = {
                        executor.submit(self.process_doctor_parallel, doctor): (idx, doctor)
                        for idx, doctor in enumerate(doctors, start=1)
                    }
                    
                    # Collect results as they complete
                    completed = 0
                    for future in as_completed(future_to_doctor):
                        doctor_idx, doctor = future_to_doctor[future]
                        completed += 1
                        self.last_activity_time = time.time()  # Update heartbeat
                        
                        try:
                            detailed_doctor = future.result()
                            if detailed_doctor:
                                with self.data_lock:
                                    self.doctors_data.append(detailed_doctor)
                                    self.save_counter += 1
                                
                                timestamp = time.strftime("%H:%M:%S")
                                logger.info(f"[{timestamp}] ✓ [{completed}/{len(doctors)}] Saved: {detailed_doctor.get('nombres', '')} {detailed_doctor.get('apellidos', '')} (Total: {len(self.doctors_data)})")
                                sys.stdout.flush()
                                
                                # Periodic save (every N records only) - outside lock
                                if self.save_counter >= save_interval:
                                    self.periodic_save(save_interval=save_interval)
                            else:
                                timestamp = time.strftime("%H:%M:%S")
                                # Could be duplicate or dead - log generically
                                logger.debug(f"[{timestamp}] ⊘ [{completed}/{len(doctors)}] Skipped: {doctor.get('nombres', 'Unknown')} (duplicate or dead)")
                                sys.stdout.flush()
                                
                        except Exception as e:
                            timestamp = time.strftime("%H:%M:%S")
                            logger.error(f"[{timestamp}] ✗ [{completed}/{len(doctors)}] Error processing {doctor.get('nombres', 'Unknown')}: {e}")
                            sys.stdout.flush()
                        
                        # Progress update every 5 doctors
                        if completed % 5 == 0:
                            timestamp = time.strftime("%H:%M:%S")
                            logger.info(f"[{timestamp}] 📊 Progress: {completed}/{len(doctors)} doctors ({completed*100//len(doctors)}%) | New: {len(self.doctors_data)} | Total: {len(self.existing_doctors_data) + len(self.doctors_data)}")
                            sys.stdout.flush()
            else:
                # Sequential processing (for local files or single worker)
                for doctor_idx, doctor in enumerate(doctors, start=1):
                    start_time = time.time()
                    self.last_activity_time = time.time()  # Update heartbeat
                    
                    # Log every doctor with timestamp to track progress
                    timestamp = time.strftime("%H:%M:%S")
                    logger.info(f"[{timestamp}] [{doctor_idx}/{len(doctors)}] Processing: {doctor.get('nombres', 'Unknown')} {doctor.get('apellido_paterno', '')} (CMP: {doctor.get('cmp', 'N/A')})")
                    sys.stdout.flush()  # Force output flush
                    
                    try:
                        detailed_doctor = self.process_doctor_parallel(doctor)
                        elapsed = time.time() - start_time
                        self.last_activity_time = time.time()  # Update heartbeat
                        
                        if detailed_doctor:
                            with self.data_lock:
                                self.doctors_data.append(detailed_doctor)
                                self.save_counter += 1
                            
                            logger.info(f"    ✓ Saved doctor: {detailed_doctor.get('nombres', '')} {detailed_doctor.get('apellidos', '')} (Total: {len(self.doctors_data)}, Time: {elapsed:.1f}s)")
                            sys.stdout.flush()
                            
                            # Periodic save (every N records only) - outside lock to avoid blocking
                            if self.save_counter >= save_interval:
                                self.periodic_save(save_interval=save_interval)
                        else:
                            # Could be duplicate or dead - log generically
                            logger.debug(f"    ⊘ Skipped (duplicate or dead) (Time: {elapsed:.1f}s)")
                            sys.stdout.flush()
                        
                    except Exception as e:
                        elapsed = time.time() - start_time
                        self.last_activity_time = time.time()  # Update heartbeat
                        logger.error(f"    ✗ Error processing doctor: {e} (Time: {elapsed:.1f}s)")
                        logger.error(f"    Continuing to next doctor...")
                        sys.stdout.flush()
                        # Continue to next doctor instead of stopping
                    
                    # Delay to avoid overwhelming the server
                    if not use_local_files:
                        time.sleep(delay)
                    
                    # Log progress every 5 doctors to keep output active
                    if doctor_idx % 5 == 0:
                        timestamp = time.strftime("%H:%M:%S")
                        logger.info(f"[{timestamp}] 📊 Progress: {doctor_idx}/{len(doctors)} doctors ({doctor_idx*100//len(doctors)}%) | New: {len(self.doctors_data)} | Total: {len(self.existing_doctors_data) + len(self.doctors_data)}")
                        sys.stdout.flush()
            
            # Delay between specialties
            if not use_local_files:
                time.sleep(delay)
        
        # Final save
        logger.info("Performing final save...")
        sys.stdout.flush()
        self.periodic_save(force=True, save_interval=save_interval)
        
        logger.info(f"Crawling complete! Collected {len(self.doctors_data)} doctor records.")
    
    def save_to_csv(self, filename: str = "doctors_data.csv"):
        """Save collected data to CSV file."""
        if not self.doctors_data:
            logger.warning("No data to save")
            return
        
        logger.info(f"Saving {len(self.doctors_data)} records to {filename}...")
        self._save_to_csv_internal(filename)
        logger.info(f"Data saved to {filename}")
    
    def save_to_json(self, filename: str = "doctors_data.json"):
        """Save collected data to JSON file (existing + new)."""
        all_doctors = self.existing_doctors_data + self.doctors_data
        if not all_doctors:
            logger.warning("No data to save")
            return
        
        logger.info(f"Saving {len(all_doctors)} total records ({len(self.existing_doctors_data)} existing + {len(self.doctors_data)} new) to {filename}...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_doctors, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Data saved to {filename}")


def main():
    """Main function to run the crawler."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Crawl CMP doctor data')
    parser.add_argument('--local', action='store_true', 
                       help='Use local HTML files instead of making HTTP requests (default: crawl live site)')
    parser.add_argument('--base-url', type=str, 
                       default='https://aplicaciones.cmp.org.pe/conoce_a_tu_medico/',
                       help='Base URL of the website')
    parser.add_argument('--start', type=int, default=0,
                       help='Start from specialty index (for resuming)')
    parser.add_argument('--max', type=int, default=None,
                       help='Maximum number of specialties to process')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='Delay between requests in seconds')
    parser.add_argument('--output-csv', type=str, default='doctors_data.csv',
                       help='Output CSV filename')
    parser.add_argument('--output-json', type=str, default='doctors_data.json',
                       help='Output JSON filename')
    parser.add_argument('--max-workers', type=int, default=3,
                       help='Number of parallel workers (default: 3)')
    parser.add_argument('--save-interval', type=int, default=30,
                       help='Save every N records (default: 30)')
    parser.add_argument('--no-check-duplicates', action='store_true',
                       help='Disable duplicate checking')
    parser.add_argument('--specialty-index', type=int, default=None,
                       help='Process only this specific specialty index (0-based)')
    parser.add_argument('--list-specialties', action='store_true',
                       help='List all available specialties with their indices and exit')
    parser.add_argument('--save-json', action='store_true',
                       help='Also save data to JSON file (default: CSV only for lightweight operation)')
    
    args = parser.parse_args()
    
    # Create crawler (default: use live site, not local files, CSV only)
    crawler = CMPCrawler(base_url=args.base_url, use_local_files=args.local, save_json=args.save_json)
    
    # List specialties if requested
    if args.list_specialties:
        logger.info("Fetching specialties list...")
        specialties = crawler.parse_specialties()
        if specialties:
            print("\n" + "=" * 80)
            print(f"Found {len(specialties)} specialties:")
            print("=" * 80)
            for idx, spec in enumerate(specialties):
                print(f"{idx:3d}. {spec['name']} (ID: {spec['id']})")
            print("=" * 80)
            print(f"\nTo process a specific specialty, use:")
            print(f"  python3 crawler.py --specialty-index <index>")
            print(f"\nExample:")
            print(f"  python3 crawler.py --specialty-index 0")
        return
    
    # Crawl (default: use live site, not local files)
    crawler.crawl_all(
        start_from_specialty=args.start,
        max_specialties=args.max,
        delay=args.delay,
        use_local_files=args.local,
        max_workers=args.max_workers,
        save_interval=args.save_interval,
        check_duplicates=not args.no_check_duplicates,
        csv_file=args.output_csv,
        json_file=args.output_json,
        specialty_index=args.specialty_index,
        save_json=args.save_json
    )
    
    # Final save (CSV is always saved, JSON only if enabled)
    crawler.save_to_csv(args.output_csv)
    if args.save_json:
        crawler.save_to_json(args.output_json)
    
    logger.info("Done!")


if __name__ == '__main__':
    main()

