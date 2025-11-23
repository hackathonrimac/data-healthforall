import requests
import csv
import time
import urllib3

# Suppress SSL warnings when verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ENDPOINTS
LIST_API_URL = "https://clinicainternacional.com.pe/api/doctors"
DETAIL_API_URL = "https://clinicainternacional.com.pe/api/doctors"

# Parámetros para el listado general
BASE_PARAMS = {
    "filters[isActive][$eq]": "true",
    "pagination[pageSize]": 10000,
    "fields[0]": "id",
    "fields[1]": "fullname",
    "fields[2]": "slug",
    "fields[3]": "cmp",
    "fields[4]": "url_image",
    "fields[5]": "documentId",
}

# Headers para que parezca navegador real
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/18.6 Safari/605.1.15"
    ),
    "Accept": "*/*",
    "Referer": "https://clinicainternacional.com.pe/staff-medico/",
}


def fetch_doctors():
    """Descarga el listado base de doctores."""
    resp = requests.get(LIST_API_URL, params=BASE_PARAMS, headers=HEADERS, timeout=30, verify=False)
    resp.raise_for_status()
    data = resp.json()
    doctors = data.get("data", [])
    print(f"Encontrados {len(doctors)} doctores en el listado general")
    return doctors


def fetch_doctor_detail_by_slug(slug: str) -> dict:
    """
    Llama al detalle del doctor usando el slug con populate profundo.
    Captura todos los campos disponibles incluyendo nested relations.
    """
    if not slug:
        return {}

    # Use populate=* to get all nested data
    # We'll extract only the fields we need from sede (title, slug, address, phone, codigo_sede)
    # and ignore nested relations like SEO, images, especialidads
    params = {
        "filters[slug][$eq]": slug,
        "populate": "*",
        "pagination[pageSize]": 1,
    }

    try:
        resp = requests.get(DETAIL_API_URL, params=params, headers=HEADERS, timeout=30, verify=False)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("data", [])
        if not items:
            return {}

        # En tu JSON, los campos vienen directamente en el objeto (no hay .attributes)
        doc = items[0]

        # --- Campos simples del doctor ---
        medical_code = doc.get("medicalCode", "")
        expertise = doc.get("expertise", "")
        is_active = doc.get("isActive", "")
        created_at = doc.get("createdAt", "")
        updated_at = doc.get("updatedAt", "")
        published_at = doc.get("publishedAt", "")

        # --- Especialidades (vienen en cada item de "schedule" bajo "especialidad") ---
        specialties = set()

        # --- Sedes, modalidad y horarios ---
        sedes_titles = set()
        sedes_slugs = set()
        modalities = set()
        schedule_slots = []  # texto tipo "Lima - Lunes 14:00–19:00"

        schedule_list = doc.get("schedule") or []
        for sched in schedule_list:
            # especialidad
            esp = sched.get("especialidad") or {}
            esp_title = (esp.get("title") or "").strip()
            if esp_title:
                specialties.add(esp_title)

            # sedes dentro de este bloque de horario
            for sede_item in sched.get("sedes") or []:
                sede = sede_item.get("sede") or {}
                sede_title = (sede.get("title") or "").strip()
                sede_slug = (sede.get("slug") or "").strip()

                if sede_title:
                    sedes_titles.add(sede_title)
                if sede_slug:
                    sedes_slugs.add(sede_slug)

                # tipo de atención
                tipo = sede_item.get("tipo_de_atencion") or {}
                tipo_title = (tipo.get("Title") or tipo.get("title") or "").strip()
                if tipo_title:
                    modalities.add(tipo_title)

                # días y horarios
                for day in sede_item.get("days") or []:
                    day_name = (day.get("day") or "").strip()
                    start = (day.get("start_time") or "").strip()
                    end = (day.get("end_time") or "").strip()
                    if sede_title and day_name and start and end:
                        schedule_slots.append(
                            f"{sede_title} - {day_name} {start}–{end}"
                        )

        # --- Educación ---
        education = doc.get("education") or {}
        edu_content = education.get("content") or []

        education_titles = set()
        education_places = set()
        education_dates = set()
        education_summary_items = []

        for item in edu_content:
            t = (item.get("title") or "").strip()
            p = (item.get("place") or "").strip()
            d = (item.get("date") or "").strip()

            if t:
                education_titles.add(t)
            if p:
                education_places.add(p)
            if d:
                education_dates.add(d)

            # Build summary with date if available
            parts = []
            if t:
                parts.append(t)
            if p:
                parts.append(f"({p})")
            if d:
                parts.append(f"[{d}]")
            
            if parts:
                education_summary_items.append(" ".join(parts))
        
        # --- Certificación, Premios, Posts ---
        certification = doc.get("certification")
        awards = doc.get("awards")
        posts = doc.get("posts")
        
        certification_text = ""
        if certification:
            # Handle certification structure (could be object or array)
            if isinstance(certification, dict):
                cert_title = certification.get("title", "")
                cert_content = certification.get("content", [])
                if cert_title:
                    certification_text = cert_title
                elif cert_content:
                    certification_text = str(cert_content)
            elif isinstance(certification, list) and certification:
                certification_text = ", ".join([str(c) for c in certification])
        
        awards_text = ""
        if awards:
            if isinstance(awards, dict):
                awards_title = awards.get("title", "")
                awards_content = awards.get("content", [])
                if awards_title:
                    awards_text = awards_title
                elif awards_content:
                    awards_text = ", ".join([str(a) for a in awards_content])
            elif isinstance(awards, list) and awards:
                awards_text = ", ".join([str(a) for a in awards])
        
        posts_text = ""
        if posts:
            if isinstance(posts, dict):
                posts_title = posts.get("title", "")
                posts_content = posts.get("content", [])
                if posts_title:
                    posts_text = posts_title
                elif posts_content:
                    posts_text = ", ".join([str(p) for p in posts_content])
            elif isinstance(posts, list) and posts:
                posts_text = ", ".join([str(p) for p in posts])

        return {
            "medicalCode": medical_code,
            "expertise": expertise,
            "isActive": is_active,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "publishedAt": published_at,
            "specialties": ", ".join(sorted(specialties)) if specialties else "",
            "sedes": ", ".join(sorted(sedes_titles)) if sedes_titles else "",
            "sedes_slugs": ", ".join(sorted(sedes_slugs)) if sedes_slugs else "",
            "modalities": ", ".join(sorted(modalities)) if modalities else "",
            "schedule_summary": " | ".join(schedule_slots) if schedule_slots else "",
            "education_titles": ", ".join(sorted(education_titles)) if education_titles else "",
            "education_places": ", ".join(sorted(education_places)) if education_places else "",
            "education_dates": ", ".join(sorted(education_dates)) if education_dates else "",
            "education_summary": " | ".join(education_summary_items) if education_summary_items else "",
            "certification": certification_text,
            "awards": awards_text,
            "posts": posts_text,
        }

    except Exception as e:
        print(f"[WARN] Error al traer detalle para slug={slug}: {e}")
        return {}


def save_to_csv(doctors, filename="internacional.csv"):
    # Columnas del CSV
    fieldnames = [
        # básicos del listado
        "id",
        "documentId",
        "fullname",
        "slug",
        "cmp",
        "url_image",
        "profile_url",
        # extras del detalle
        "medicalCode",
        "expertise",
        "isActive",
        "createdAt",
        "updatedAt",
        "publishedAt",
        "specialties",
        "sedes",
        "sedes_slugs",
        "modalities",
        "schedule_summary",
        "education_titles",
        "education_places",
        "education_dates",
        "education_summary",
        "certification",
        "awards",
        "posts",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for i, d in enumerate(doctors, start=1):
            slug = d.get("slug", "")
            profile_url = (
                f"https://clinicainternacional.com.pe/staff-medico/{slug}/"
                if slug else ""
            )

            # Llamada al detalle por cada doctor
            extra = fetch_doctor_detail_by_slug(slug)
            time.sleep(0.2)  # un pequeño delay para no bombardear el servidor

            row = {
                "id": d.get("id", ""),
                "documentId": d.get("documentId", ""),
                "fullname": d.get("fullname", ""),
                "slug": slug,
                "cmp": d.get("cmp", ""),
                "url_image": d.get("url_image", ""),
                "profile_url": profile_url,
                "medicalCode": extra.get("medicalCode", ""),
                "expertise": extra.get("expertise", ""),
                "isActive": extra.get("isActive", ""),
                "createdAt": extra.get("createdAt", ""),
                "updatedAt": extra.get("updatedAt", ""),
                "publishedAt": extra.get("publishedAt", ""),
                "specialties": extra.get("specialties", ""),
                "sedes": extra.get("sedes", ""),
                "sedes_slugs": extra.get("sedes_slugs", ""),
                "modalities": extra.get("modalities", ""),
                "schedule_summary": extra.get("schedule_summary", ""),
                "education_titles": extra.get("education_titles", ""),
                "education_places": extra.get("education_places", ""),
                "education_dates": extra.get("education_dates", ""),
                "education_summary": extra.get("education_summary", ""),
                "certification": extra.get("certification", ""),
                "awards": extra.get("awards", ""),
                "posts": extra.get("posts", ""),
            }

            writer.writerow(row)

            if i % 50 == 0:
                print(f"Procesados {i} doctores...")

    print(f"✅ CSV generado: {filename}")


def main():
    doctors = fetch_doctors()
    save_to_csv(doctors)


if __name__ == "__main__":
    main()