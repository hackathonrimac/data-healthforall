#!/usr/bin/env python3
"""
San Pablo Doctor Data Parser
Extracts doctor information from the iframe content loaded from qualab.com.pe

The HTML file contains an iframe that loads:
https://www.qualab.com.pe/staff/staff-medico-surco.php

This script attempts to:
1. Fetch the iframe URL directly
2. Parse the HTML content to extract doctor data
3. If direct fetch fails, provides instructions for using Selenium
"""

import csv
import re
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional
from bs4 import BeautifulSoup

IFRAME_URL = "https://www.qualab.com.pe/staff/staff-medico-surco.php"
BASE_URL = "https://www.sanpablo.com.pe"
OUTPUT_CSV = "san-pablo.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Referer": "https://www.sanpablo.com.pe/staff-medico/",
}


def fetch_iframe_content(url: str) -> Optional[str]:
    """
    Attempt to fetch the iframe content directly.
    
    Args:
        url: URL of the iframe source
        
    Returns:
        HTML content as string, or None if fetch fails
    """
    print(f"Attempting to fetch iframe content from: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        print(f"✓ Successfully fetched {len(response.text)} characters")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to fetch iframe content: {e}")
        print("  This might require browser automation (Selenium) to extract.")
        return None


def extract_cmp_rne(text: str) -> tuple:
    """
    Extract CMP and RNE codes from text.
    
    Returns:
        tuple: (cmp_code, rne_code)
    """
    cmp_code = ""
    rne_code = ""
    
    # Pattern for CMP (various formats)
    cmp_patterns = [
        r'CMP[:\s]*(\d+)',
        r'C\.M\.P\.\s*(\d+)',
        r'C\.M\.P[:\s]*(\d+)',
    ]
    for pattern in cmp_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            cmp_code = match.group(1).strip()
            break
    
    # Pattern for RNE
    rne_patterns = [
        r'RNE[:\s]*(\d+)',
        r'R\.N\.E\.\s*(\d+)',
        r'R\.N\.E[:\s]*(\d+)',
    ]
    for pattern in rne_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            rne_code = match.group(1).strip()
            break
    
    return (cmp_code, rne_code)


def clean_name(name: str) -> str:
    """Remove common prefixes from doctor names."""
    name = name.strip()
    prefixes = ["Dr.", "Dra.", "Dr ", "Dra ", "Doctor ", "Doctora "]
    for prefix in prefixes:
        if name.startswith(prefix):
            return name[len(prefix):].strip()
    return name


def parse_doctor_from_card(card) -> Dict:
    """
    Parse a doctor card element from the HTML.
    Structure: <div class="card shadow-sm"> with:
    - img.foto-med: Photo
    - .card-body h3: Name (with "Dr. " prefix)
    - .card-body span: CMP code and specialty
    
    Args:
        card: BeautifulSoup card element
        
    Returns:
        Dictionary with doctor data
    """
    doctor = {
        "name": "",
        "especialidad": "",
        "cmp": "",
        "rne": "",
        "telefono": "",
        "email": "",
        "photo_url": "",
        "profile_url": "",
    }
    
    # Extract name from h3 in card-body
    card_body = card.find("div", class_="card-body")
    if card_body:
        h3 = card_body.find("h3")
        if h3:
            name_text = h3.get_text(strip=True)
            doctor["name"] = clean_name(name_text)
        
        # Extract CMP and specialty from spans
        spans = card_body.find_all("span")
        for span in spans:
            text = span.get_text(strip=True)
            # Check if it's CMP
            if text.startswith("CMP:"):
                cmp_match = re.search(r'CMP:\s*(\d+)', text)
                if cmp_match:
                    doctor["cmp"] = cmp_match.group(1).strip()
            # Otherwise it's likely the specialty
            elif text and not text.startswith("CMP") and not text.startswith("RNE"):
                if not doctor["especialidad"]:  # Only set if not already set
                    doctor["especialidad"] = text
    
    # Extract photo
    img = card.find("img", class_="foto-med")
    if img and img.get("src"):
        src = img.get("src")
        if src.startswith("http"):
            doctor["photo_url"] = src
        elif src.startswith("/"):
            doctor["photo_url"] = f"https://www.qualab.com.pe{src}"
        else:
            doctor["photo_url"] = f"https://www.qualab.com.pe/{src}"
    
    return doctor


def parse_doctors_from_html(html_content: str) -> List[Dict]:
    """
    Parse all doctors from HTML content.
    Doctors are in <div class="card shadow-sm"> elements.
    
    Args:
        html_content: HTML content as string
        
    Returns:
        List of doctor dictionaries
    """
    soup = BeautifulSoup(html_content, "html.parser")
    doctors = []
    
    # Find all doctor cards
    cards = soup.find_all("div", class_=lambda x: x and "card" in str(x) and "shadow-sm" in str(x))
    
    print(f"Found {len(cards)} doctor cards")
    
    # Parse each card
    for i, card in enumerate(cards):
        doctor = parse_doctor_from_card(card)
        if doctor["name"]:  # Only add if we found a name
            doctors.append(doctor)
            if i < 5 or (i + 1) % 10 == 0:  # Print first 5 and every 10th
                print(f"  [{i+1}] Extracted: {doctor['name']} - {doctor['especialidad']}")
    
    print(f"\nExtracted {len(doctors)} doctors")
    return doctors


def get_max_page_number(html_content: str) -> int:
    """
    Extract the maximum page number from pagination.
    
    Args:
        html_content: HTML content as string
        
    Returns:
        Maximum page number, or 1 if not found
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Look for pagination links
    pagination = soup.find("ul", class_=lambda x: x and "pagination" in str(x))
    if pagination:
        page_links = pagination.find_all("a", class_="page-link")
        max_page = 1
        for link in page_links:
            href = link.get("href", "")
            # Extract page number from href like "staff-medico-surco.php?pag=2"
            match = re.search(r'pag=(\d+)', href)
            if match:
                page_num = int(match.group(1))
                max_page = max(max_page, page_num)
        return max_page
    
    return 1


def scrape_all_pages(base_url: str = IFRAME_URL, max_pages: int = None) -> List[Dict]:
    """
    Scrape all pages of doctors.
    
    Args:
        base_url: Base URL for the iframe
        max_pages: Maximum number of pages to scrape (None = auto-detect)
        
    Returns:
        List of all doctor dictionaries
    """
    all_doctors = []
    
    # First, get the first page to determine total pages
    print("Fetching page 1...")
    html_content = fetch_iframe_content(base_url)
    if not html_content:
        return []
    
    doctors = parse_doctors_from_html(html_content)
    all_doctors.extend(doctors)
    
    # Determine max pages
    if max_pages is None:
        max_page = get_max_page_number(html_content)
        print(f"Detected {max_page} total pages")
    else:
        max_page = max_pages
    
    # Scrape remaining pages
    for page in range(2, max_page + 1):
        print(f"\nFetching page {page}...")
        page_url = f"{base_url}?b_medico=&b_sede=1&b_especialidad=&pag={page}"
        html_content = fetch_iframe_content(page_url)
        if html_content:
            doctors = parse_doctors_from_html(html_content)
            all_doctors.extend(doctors)
        else:
            print(f"  Failed to fetch page {page}, stopping")
            break
        time.sleep(0.5)  # Be polite
    
    # Remove duplicates based on name + CMP
    seen = set()
    unique_doctors = []
    for doctor in all_doctors:
        key = (doctor["name"].lower(), doctor["cmp"])
        if key not in seen:
            seen.add(key)
            unique_doctors.append(doctor)
    
    print(f"\nTotal unique doctors: {len(unique_doctors)}")
    return unique_doctors


def save_to_csv(doctors: List[Dict], filename: str = OUTPUT_CSV):
    """
    Save doctors data to CSV file.
    
    Args:
        doctors: List of doctor dictionaries
        filename: Output CSV filename
    """
    if not doctors:
        print("No doctors to save")
        return
    
    fieldnames = [
        "name",
        "especialidad",
        "cmp",
        "rne",
        "telefono",
        "email",
        "photo_url",
        "profile_url",
    ]
    
    script_dir = Path(__file__).parent
    output_path = script_dir / filename
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(doctors)
    
    print(f"✅ CSV saved: {output_path} ({len(doctors)} doctors)")


def print_selenium_instructions():
    """Print instructions for using Selenium if direct fetch fails."""
    print("\n" + "="*70)
    print("SELENIUM INSTRUCTIONS")
    print("="*70)
    print("""
If direct fetch fails, you'll need to use Selenium to extract the iframe content.

1. Install Selenium:
   pip install selenium webdriver-manager

2. Use this code snippet:

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

# Setup
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in background
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Load the main page
    driver.get("https://www.sanpablo.com.pe/staff-medico/")
    time.sleep(3)  # Wait for page to load
    
    # Switch to iframe
    iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='qualab.com.pe']")
    driver.switch_to.frame(iframe)
    time.sleep(2)  # Wait for iframe content
    
    # Get iframe HTML
    iframe_html = driver.page_source
    
    # Save or parse
    with open("san-pablo-iframe.html", "w", encoding="utf-8") as f:
        f.write(iframe_html)
    
    print("✓ Saved iframe content to san-pablo-iframe.html")
    
finally:
    driver.quit()

3. Then run this script on the saved HTML file.
    """)


def main():
    """Main function to extract doctor data."""
    print("="*70)
    print("San Pablo Doctor Data Extractor")
    print("="*70)
    
    # Scrape all pages
    doctors = scrape_all_pages()
    
    if doctors:
        save_to_csv(doctors)
        
        # Print sample
        print("\n" + "="*70)
        print("SAMPLE DOCTOR DATA:")
        print("="*70)
        for key, value in doctors[0].items():
            print(f"  {key}: {value}")
        
        # Print summary
        print("\n" + "="*70)
        print(f"SUMMARY:")
        print(f"  Total doctors: {len(doctors)}")
        print(f"  With CMP: {sum(1 for d in doctors if d['cmp'])}")
        print(f"  With specialty: {sum(1 for d in doctors if d['especialidad'])}")
        print(f"  With photo: {sum(1 for d in doctors if d['photo_url'])}")
    else:
        print("\n⚠️  No doctors found.")
        print("Please check the iframe URL and HTML structure.")


if __name__ == "__main__":
    main()

