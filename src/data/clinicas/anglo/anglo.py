import csv
import re
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_LIST_URL = "https://clinicaangloamericana.pe/medicos/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AngloScraper/1.0; +https://example.com)"
}

def get_page_url(page_num: int) -> str:
    if page_num == 1:
        return BASE_LIST_URL
    return f"{BASE_LIST_URL}page/{page_num}/"

def extract_doctor_cards(soup: BeautifulSoup):
    cards = soup.find_all("article")
    if cards:
        return cards
    # fallback if they change markup
    candidates = []
    for h in soup.find_all(["h2", "h3"]):
        if h.find("a") and h.find_next(string=lambda s: isinstance(s, str) and "Ver Perfil" in s):
            candidates.append(h.parent)
    return candidates

def parse_list_page(html: str):
    soup = BeautifulSoup(html, "html.parser")
    cards = extract_doctor_cards(soup)
    doctors = []

    for card in cards:
        name_tag = card.find(["h2", "h3"])
        if not name_tag:
            continue
        link = name_tag.find("a")
        if not link:
            continue

        name = link.get_text(strip=True)
        profile_url = urljoin(BASE_LIST_URL, link.get("href", ""))

        # list-page specialty (may be 1 or many)
        specialties = []
        for a in card.find_all("a"):
            text = a.get_text(strip=True)
            if not text:
                continue
            if "Ver Perfil" in text:
                continue
            specialties.append(text)
        specialties = list(dict.fromkeys(specialties))

        # email on list page (quick grab)
        email = None
        email_link = card.find("a", href=lambda h: h and h.startswith("mailto:"))
        if email_link:
            email = email_link.get_text(strip=True) or email_link["href"].replace("mailto:", "")

        doctors.append(
            {
                "name": name,
                "list_specialties": " | ".join(specialties),
                "list_email": email or "",
                "profile_url": profile_url,
            }
        )

    return doctors

def scrape_all_list_pages(max_pages: int = 200, delay: float = 1.0):
    all_doctors = []
    page = 1
    while page <= max_pages:
        url = get_page_url(page)
        print(f"[LIST] Fetching page {page}: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=15)

        if resp.status_code == 404:
            print("Got 404 on list, stopping.")
            break
        if not resp.ok:
            print(f"Error {resp.status_code} on list, stopping.")
            break

        doctors = parse_list_page(resp.text)
        if not doctors:
            print("No doctors found on this list page, stopping.")
            break

        all_doctors.extend(doctors)
        page += 1
        time.sleep(delay)  # politeness
    return all_doctors

# ---------------- PROFILE PARSER ---------------- #

LABELS = {
    "Especialidad",
    "Teléfono",
    "Email",
    "Pregrado",
    "Posgrado",
    "Fellowship / Especialidad",
    "Grados académicos",
    "Certificaciones",
    "Interés especial",
    "Asociaciones",
}
SECTION_BREAKS = {"CV"}  # break value collection when this appears
INLINE_CODES = ["CMP", "RNE"]  # come as "CMP: 75022", "RNE: 40981"

def parse_profile(html: str):
    soup = BeautifulSoup(html, "html.parser")
    data = {
        "name_h1": "",
        "especialidad": "",
        "telefono": "",
        "email": "",
        "cmp": "",
        "rne": "",
        "pregrado": "",
        "posgrado": "",
        "fellowship_especialidad": "",
        "grados_academicos": "",
        "certificaciones": "",
        "interes_especial": "",
        "asociaciones": "",
    }

    # Name from h1 (just to double-check)
    h1 = soup.find("h1")
    if h1:
        data["name_h1"] = h1.get_text(strip=True)

    # Find "Información" section
    info_heading = soup.find(
        lambda tag: tag.name in ["h2", "h3", "h4"]
        and "Información" in tag.get_text(strip=True)
    )
    if not info_heading:
        return data  # nothing else we can do safely

    # First, try to extract CMP and RNE from <b> tags in the CV section
    cv_section = soup.find("div", id="cv-ficha")
    if cv_section:
        # Get all text from the CV section and extract CMP/RNE using regex
        cv_text = cv_section.get_text()
        
        # Extract CMP: pattern (e.g., "CMP: 36687" or "<b>CMP:</b> 36687")
        cmp_match = re.search(r"CMP:\s*(\d+)", cv_text)
        if cmp_match:
            data["cmp"] = cmp_match.group(1)
        
        # Extract RNE: pattern (e.g., "RNE: 13020" or "<b>RNE:</b> 13020")
        rne_match = re.search(r"RNE:\s*(\d+)", cv_text)
        if rne_match:
            data["rne"] = rne_match.group(1)

    # Collect all text tokens between "Información" and the first "Sede "
    tokens = []
    reached_info = False
    for string in info_heading.next_elements:
        if not isinstance(string, str):
            continue
        text = string.strip()
        if not text:
            continue
        if not reached_info:
            # skip the "Información" label itself
            if text == "Información":
                reached_info = True
            continue

        # stop at first Sede section
        if text.startswith("Sede "):
            break

        tokens.append(text)

    # Now tokens is like:
    # ['Especialidad', 'Anestesiología', 'Teléfono', '6168900 anexo 1458', 'Email', 'gacosta@...', 'CV', 'CMP: 75022', 'RNE: 40981', 'Pregrado:', 'Universidad ...', ...]

    i = 0
    while i < len(tokens):
        t = tokens[i]

        # handle inline CMP/RNE: "CMP: 75022" (fallback if not found in <b> tags)
        handled_inline = False
        for code in INLINE_CODES:
            if t.startswith(code + ":"):
                _, val = t.split(":", 1)
                val = val.strip()
                key = code.lower()  # 'cmp', 'rne'
                # Only set if we haven't already found it from <b> tags
                if not data[key]:
                    data[key] = val
                handled_inline = True
                break
        if handled_inline:
            i += 1
            continue

        # detect labels of the form "Label" or "Label:"
        base = t.rstrip(":")
        if base in SECTION_BREAKS:
            # just a section header, skip
            i += 1
            continue

        if base in LABELS:
            label = base
            # accumulate values until we hit another label / section break / sede
            values = []
            j = i + 1
            while j < len(tokens):
                t2 = tokens[j]
                base2 = t2.rstrip(":")

                # join multi-line values until next 'real' label
                if (
                    base2 in LABELS
                    or base2 in SECTION_BREAKS
                    or t2.startswith("Sede ")
                    or any(t2.startswith(code + ":") for code in INLINE_CODES)
                ):
                    break
                values.append(t2)
                j += 1

            value_str = " ".join(values).strip()
            if label == "Especialidad":
                data["especialidad"] = value_str
            elif label == "Teléfono":
                data["telefono"] = value_str
            elif label == "Email":
                data["email"] = value_str
            elif label == "Pregrado":
                data["pregrado"] = value_str
            elif label == "Posgrado":
                data["posgrado"] = value_str
            elif label == "Fellowship / Especialidad":
                data["fellowship_especialidad"] = value_str
            elif label == "Grados académicos":
                data["grados_academicos"] = value_str
            elif label == "Certificaciones":
                data["certificaciones"] = value_str
            elif label == "Interés especial":
                data["interes_especial"] = value_str
            elif label == "Asociaciones":
                data["asociaciones"] = value_str

            i = j
        else:
            i += 1

    return data

def enrich_doctor_with_profile(doc: dict, delay: float = 0.7):
    url = doc["profile_url"]
    print(f"[PROFILE] {doc['name']} → {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if not resp.ok:
            print(f"  ! Error {resp.status_code} for profile")
            return doc
    except requests.RequestException as e:
        print(f"  ! Request error for {url}: {e}")
        return doc

    info = parse_profile(resp.text)

    # merge list info + profile info
    merged = {
        **doc,
        "name_profile": info["name_h1"],
        "especialidad_profile": info["especialidad"],
        "telefono": info["telefono"],
        "email_profile": info["email"] or doc.get("list_email", ""),
        "cmp": info["cmp"],
        "rne": info["rne"],
        "pregrado": info["pregrado"],
        "posgrado": info["posgrado"],
        "fellowship_especialidad": info["fellowship_especialidad"],
        "grados_academicos": info["grados_academicos"],
        "certificaciones": info["certificaciones"],
        "interes_especial": info["interes_especial"],
        "asociaciones": info["asociaciones"],
    }

    time.sleep(delay)
    return merged

def main():
    # 1) get all doctors from list pages
    doctors_basic = scrape_all_list_pages()

    # 2) enrich with profile data
    doctors_full = []
    for d in doctors_basic:
        full = enrich_doctor_with_profile(d)
        doctors_full.append(full)

    # 3) save
    fieldnames = [
        "name",
        "name_profile",
        "list_specialties",
        "especialidad_profile",
        "list_email",
        "email_profile",
        "telefono",
        "cmp",
        "rne",
        "pregrado",
        "posgrado",
        "fellowship_especialidad",
        "grados_academicos",
        "certificaciones",
        "interes_especial",
        "asociaciones",
        "profile_url",
    ]

    with open("anglo_doctors_full.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in doctors_full:
            writer.writerow(d)

    print(f"Saved {len(doctors_full)} doctors to anglo_doctors_full.csv")

if __name__ == "__main__":
    main()