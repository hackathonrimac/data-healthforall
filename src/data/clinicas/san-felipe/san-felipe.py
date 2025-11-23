import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time

BASE_URL = "https://www.clinicasanfelipe.com"
LIST_URL = BASE_URL + "/medicos/"

session = requests.Session()

def get_soup(url):
    resp = session.get(url)
    if resp.status_code == 404:
        print(f"404 for {url}, skipping")
        return None
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def scrape_list_page():
    soup = get_soup(LIST_URL)
    doctors = []

    for a in soup.find_all("a", string=lambda s: s and "Conócelo aquí" in s):
        card = a.find_parent(["div", "article", "li"])
        if card is None:
            continue

        texts = [t.strip() for t in card.stripped_strings if t.strip()]

        specialty = name = location = ""
        if len(texts) >= 3:
            specialty = texts[0]
            name = texts[1]
            location = texts[2]

        img = card.find("img")
        img_url = urljoin(BASE_URL, img["src"]) if img and img.get("src") else ""

        href = a.get("href") or ""
        if href.startswith("http"):
            profile_url = href
        else:
            profile_url = urljoin(LIST_URL, href)

        doctors.append({
            "name": name,
            "specialty": specialty,
            "location_list": location,
            "profile_url": profile_url,
            "image_url": img_url,
        })

    print(f"Found {len(doctors)} doctors in list page")
    return doctors

def get_value_after_label(soup, label_substring):
    """
    Looks for a string that contains label_substring (e.g. 'CMP:' or 'Universidad (Pre Grado):')
    and returns the value on the same line (after ':') or the very next non-empty text.
    """
    el = soup.find(string=lambda s: s and label_substring in s)
    if not el:
        return ""

    text = el.strip()
    # Case like "CMP: 065254"
    if ":" in text:
        label, value = text.split(":", 1)
        value = value.strip()
        if value:
            return value

    # Case where label is alone in a line and value is next line
    next_text = el.find_next(string=lambda t: t and t.strip())
    if next_text:
        return next_text.strip()

    return ""

def scrape_profile(profile_url):
    if not profile_url:
        return {}

    try:
        soup = get_soup(profile_url)
    except Exception as e:
        print(f"Error fetching {profile_url}: {e}")
        return {}

    data = {}

    # Name (H1)
    h1 = soup.find("h1")
    if h1:
        data["profile_name"] = h1.get_text(strip=True)
    else:
        data["profile_name"] = ""

    # Extra fields
    data["especialidad_detalle"] = get_value_after_label(soup, "Especialidad")
    data["tipo_atencion"] = get_value_after_label(soup, "Tipo de Atención")
    data["atiende_en_detalle"] = get_value_after_label(soup, "Atiende en")
    data["cmp"] = get_value_after_label(soup, "CMP")
    data["rne"] = get_value_after_label(soup, "RNE")
    data["universidad_pregrado"] = get_value_after_label(soup, "Universidad (Pre Grado)")
    data["residencia"] = get_value_after_label(soup, "Residencia")
    data["universidad_pasantias"] = get_value_after_label(soup, "Universidad (Pasantias)")
    data["idiomas"] = get_value_after_label(soup, "Idiomas")
    data["area_interes"] = get_value_after_label(soup, "Area de interes")

    return data

def main():
    doctors = scrape_list_page()

    all_rows = []
    for i, doc in enumerate(doctors, start=1):
        print(f"[{i}/{len(doctors)}] Scraping profile: {doc['name']}")
        extra = scrape_profile(doc["profile_url"])
        row = {**doc, **extra}
        all_rows.append(row)

        # OPTIONAL: be nice with the server
        time.sleep(0.5)

    csv_file = "clinica_san_felipe_medicos_full.csv"
    fieldnames = [
        "name",
        "specialty",
        "location_list",
        "profile_url",
        "image_url",
        "profile_name",
        "especialidad_detalle",
        "tipo_atencion",
        "atiende_en_detalle",
        "cmp",
        "rne",
        "universidad_pregrado",
        "residencia",
        "universidad_pasantias",
        "idiomas",
        "area_interes",
    ]

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Saved {len(all_rows)} rows to {csv_file}")

if __name__ == "__main__":
    main()
