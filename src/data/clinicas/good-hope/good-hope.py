#!/usr/bin/env python3
"""
Good Hope Doctor Data Parser
Extracts doctor information from good-hope.html

The HTML structure contains doctor profiles in <article> tags with:
- id_medico: Doctor ID
- Name: In title attribute and link text (with "Dr. " prefix)
- Primary specialty: In <h6 class="cmsmasters_profile_subtitle">
- Additional specialties: In <div class="cmsmasters_profile_content entry-content"><p>
- CMP (N.C.) and RNE codes: In <span class="cmsmasters-icon-briefcase-4">
- Photo URL: In img src
"""

import re
import csv
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Dict


def extract_cmp_rne(text: str) -> tuple:
    """
    Extract CMP and RNE codes from text like "N.C. 027730" and "R.N.E. 015910"
    
    Returns:
        tuple: (cmp_code, rne_code)
    """
    cmp_code = ""
    rne_code = ""
    
    # Pattern for N.C. (CMP)
    cmp_match = re.search(r'N\.C\.\s*(\d+)', text)
    if cmp_match:
        cmp_code = cmp_match.group(1).strip()
    
    # Pattern for R.N.E.
    rne_match = re.search(r'R\.N\.E\.\s*(\d+)', text)
    if rne_match:
        rne_code = rne_match.group(1).strip()
    
    return (cmp_code, rne_code)


def clean_name(name: str) -> str:
    """Remove 'Dr. ' or 'Dra. ' prefix from name."""
    name = name.strip()
    if name.startswith("Dr. "):
        return name[4:].strip()
    elif name.startswith("Dra. "):
        return name[5:].strip()
    return name


def parse_doctor_article(article) -> Dict:
    """
    Parse a single doctor article element.
    
    Args:
        article: BeautifulSoup article element
        
    Returns:
        Dictionary with doctor data
    """
    doctor = {
        "id_medico": "",
        "name": "",
        "primary_specialty": "",
        "additional_specialties": "",
        "cmp": "",
        "rne": "",
        "photo_url": "",
    }
    
    # Extract id_medico from the link
    link = article.find("a", class_="cmsmasters_img_link")
    if link:
        doctor["id_medico"] = link.get("id_medico", "").strip()
        doctor["name"] = clean_name(link.get("title", "").strip())
        
        # Extract photo URL
        img = link.find("img")
        if img and img.get("src"):
            doctor["photo_url"] = img.get("src", "").strip()
    
    # If name not found in link title, try the text link
    if not doctor["name"]:
        text_link = article.find("a", class_="dspDetailDoctor")
        if text_link:
            name_text = text_link.get_text(strip=True)
            doctor["name"] = clean_name(name_text)
            if not doctor["id_medico"]:
                doctor["id_medico"] = text_link.get("id_medico", "").strip()
    
    # Extract primary specialty from h6
    h6 = article.find("h6", class_="cmsmasters_profile_subtitle")
    if h6:
        doctor["primary_specialty"] = h6.get_text(strip=True)
    
    # Extract additional specialties from content div
    content_div = article.find("div", class_="cmsmasters_profile_content")
    if content_div:
        p_tag = content_div.find("p")
        if p_tag:
            additional = p_tag.get_text(strip=True)
            # Remove &nbsp; and clean up
            additional = additional.replace("&nbsp;", " ").replace("\xa0", " ").strip()
            # Skip if it's just "-"
            if additional and additional != "-":
                doctor["additional_specialties"] = additional
    
    # Extract CMP and RNE from contact info
    contact_info = article.find("span", class_="cmsmasters-icon-briefcase-4")
    if contact_info:
        contact_text = contact_info.get_text(separator=" ", strip=True)
        cmp_code, rne_code = extract_cmp_rne(contact_text)
        doctor["cmp"] = cmp_code
        doctor["rne"] = rne_code
    
    return doctor


def extract_doctors_from_html(html_file: str) -> List[Dict]:
    """
    Extract all doctors from the HTML file.
    
    Args:
        html_file: Path to the HTML file
        
    Returns:
        List of doctor dictionaries
    """
    print(f"Reading HTML file: {html_file}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all article elements with class containing "profile"
    articles = soup.find_all("article", class_=lambda x: x and "profile" in x)
    
    print(f"Found {len(articles)} doctor articles")
    
    doctors = []
    for article in articles:
        doctor = parse_doctor_article(article)
        # Only add if we have at least a name
        if doctor["name"]:
            doctors.append(doctor)
    
    print(f"Extracted {len(doctors)} doctors")
    return doctors


def save_to_csv(doctors: List[Dict], filename: str = "good_hope_doctores.csv"):
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
        "id_medico",
        "name",
        "primary_specialty",
        "additional_specialties",
        "cmp",
        "rne",
        "photo_url",
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(doctors)
    
    print(f"✅ CSV saved: {filename} ({len(doctors)} doctors)")


def main():
    """Main function to parse good-hope.html and save to CSV."""
    script_dir = Path(__file__).parent
    html_file = script_dir / "good-hope.html"
    
    if not html_file.exists():
        print(f"ERROR: File not found: {html_file}")
        return
    
    doctors = extract_doctors_from_html(str(html_file))
    save_to_csv(doctors, str(script_dir / "good_hope_doctores.csv"))


if __name__ == "__main__":
    main()

