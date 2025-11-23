import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import csv
import time

BASE_URL = "https://www.crp.com.pe"


# --------- HELPERS ---------

def get_soup(url: str) -> BeautifulSoup:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


# --------- PARSE LIST PAGE ---------

def parse_list_page(list_url: str):
    """
    Devuelve una lista de dicts mínimos con:
    - detail_url
    - cmp (si viene en el query string)
    - nombre_list (texto del listado)
    - especialidad_list
    """
    soup = get_soup(list_url)
    doctors = []

    for li in soup.select("#itemContainerMedico > li"):
        a = li.find("a", href=True)
        if not a:
            continue

        detail_url = urljoin(BASE_URL, a["href"])

        # CMP viene en el query param ?cmp=09944
        parsed = urlparse(detail_url)
        qs = parse_qs(parsed.query)
        cmp_value = qs.get("cmp", [None])[0]

        # Nombre y especialidad tal como aparecen en el listado
        cont_span = a.select_one(".contenido > span")
        nombre_list = None
        especialidad_list = None

        if cont_span:
            # El nombre está en dos <strong> y la especialidad como texto plano después
            strongs = cont_span.find_all("strong")
            nombre_list = " ".join(s.get_text(strip=True) for s in strongs if s.get_text(strip=True))
            # Lo que quede de texto en el span, sin los strong, lo tomamos como especialidad
            for s in strongs:
                s.extract()
            especialidad_list = cont_span.get_text(" ", strip=True) or None

        doctors.append(
            {
                "detail_url": detail_url,
                "cmp_from_list": cmp_value,
                "nombre_list": nombre_list,
                "especialidad_list": especialidad_list,
            }
        )

    return doctors


# --------- PARSE DETAIL PAGE ---------

def parse_doctor_detail(detail_url: str):
    soup = get_soup(detail_url)

    # Nombre
    name_el = soup.select_one(".content-detalle-medico h1")
    full_name = name_el.get_text(strip=True) if name_el else None

    # Especialidad principal
    spec_el = soup.select_one(".content-detalle-medico .txt-cargo")
    main_specialty = spec_el.get_text(strip=True) if spec_el else None

    # Colegiatura
    coleg_el = soup.select_one("#colegia")
    colegiatura = None
    if coleg_el:
        text = coleg_el.get_text(strip=True)
        # "Colegiatura: 09944" → 09944
        if ":" in text:
            colegiatura = text.split(":", 1)[1].strip()
        else:
            colegiatura = text

    # Teléfonos y anexos
    phone_text = None
    anexos = None
    num_telf_container = soup.select_one("#num-telf, #num-telf, #num-telf, #num-telf")  # por si cambian el id

    if num_telf_container:
        # span con los teléfonos
        span_tel = num_telf_container.select_one(".numTelf")
        if span_tel:
            phone_text = span_tel.get_text(" ", strip=True)

        # el texto completo incluye “Anexo(s) : 1279-1605”
        full_contact = num_telf_container.get_text(" ", strip=True)
        # Buscamos la palabra Anexo(s)
        if "Anexo" in full_contact:
            # ejemplo: "... 224·2224 - ... Anexo(s) : 1279-1605"
            parts = full_contact.split("Anexo", 1)[1]
            anexos = parts.replace("Anexo(s)", "").replace(":", "").strip()

    # Educación (tab #marzen)
    education_items = []
    for block in soup.select("#marzen .contenido1"):
        texts = []
        for p in block.select(".txt p, .profe p"):
            txt = p.get_text(" ", strip=True)
            if txt:
                texts.append(txt)
        if texts:
            education_items.append(" | ".join(texts))
    education = " || ".join(education_items) if education_items else None

    # Membresías (tab #rauchbier)
    membership_items = []
    for block in soup.select("#rauchbier .contenido1"):
        texts = []
        for p in block.select(".txt p, .profe p"):
            txt = p.get_text(" ", strip=True)
            if txt:
                texts.append(txt)
        if texts:
            membership_items.append(" | ".join(texts))
    memberships = " || ".join(membership_items) if membership_items else None

    # Foto
    photo_el = soup.select_one(".content-detalle-medico .right img")
    photo_url = urljoin(BASE_URL, photo_el["src"]) if photo_el and photo_el.has_attr("src") else None

    return {
        "detail_url": detail_url,
        "nombre": full_name,
        "especialidad_principal": main_specialty,
        "colegiatura": colegiatura,
        "telefonos": phone_text,
        "anexos": anexos,
        "educacion": education,
        "membresias": memberships,
        "foto_url": photo_url,
    }


# --------- ORQUESTA TODO Y GUARDA EN CSV ---------

def scrape_crp_plantel(list_url: str, output_csv: str = "crp_medicos.csv"):
    doctors_basic = parse_list_page(list_url)
    rows = []

    for i, basic in enumerate(doctors_basic, start=1):
        detail_url = basic["detail_url"]
        print(f"[{i}/{len(doctors_basic)}] Procesando: {detail_url}")
        try:
            detail_data = parse_doctor_detail(detail_url)
        except Exception as e:
            print(f"  Error en {detail_url}: {e}")
            continue

        row = {**basic, **detail_data}
        rows.append(row)

        # para no bombardear el server
        time.sleep(0.5)

    # Guardamos CSV
    if rows:
        fieldnames = list(rows[0].keys())
        with open(output_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    print(f"Listo. Guardado en {output_csv}")


if __name__ == "__main__":
    # URL del plantel médico (la que tiene el listado con <ul id="itemContainerMedico">)
    LIST_URL = "https://www.crp.com.pe/plantel-medico-profesionales-altamente-calificados/"
    scrape_crp_plantel(LIST_URL)