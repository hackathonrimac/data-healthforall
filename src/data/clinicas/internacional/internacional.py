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
    Llama al detalle del doctor usando el slug y populate=*.
    Estructura basada en el JSON que enviaste.
    """
    if not slug:
        return {}

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
        education_summary_items = []

        for item in edu_content:
            t = (item.get("title") or "").strip()
            p = (item.get("place") or "").strip()

            if t:
                education_titles.add(t)
            if p:
                education_places.add(p)

            if t and p:
                education_summary_items.append(f"{t} ({p})")
            elif t:
                education_summary_items.append(t)
            elif p:
                education_summary_items.append(p)

        return {
            "medicalCode": medical_code,
            "expertise": expertise,
            "isActive": is_active,
            "createdAt": created_at,
            "updatedAt": updated_at,
            "specialties": ", ".join(sorted(specialties)) if specialties else "",
            "sedes": ", ".join(sorted(sedes_titles)) if sedes_titles else "",
            "sedes_slugs": ", ".join(sorted(sedes_slugs)) if sedes_slugs else "",
            "modalities": ", ".join(sorted(modalities)) if modalities else "",
            "schedule_summary": " | ".join(schedule_slots) if schedule_slots else "",
            "education_titles": ", ".join(sorted(education_titles)) if education_titles else "",
            "education_places": ", ".join(sorted(education_places)) if education_places else "",
            "education_summary": " | ".join(education_summary_items) if education_summary_items else "",
        }

    except Exception as e:
        print(f"[WARN] Error al traer detalle para slug={slug}: {e}")
        return {}


def save_to_csv(doctors, filename="clinicainternacional_doctores_detallado.csv"):
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
        "specialties",
        "sedes",
        "sedes_slugs",
        "modalities",
        "schedule_summary",
        "education_titles",
        "education_places",
        "education_summary",
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
                "specialties": extra.get("specialties", ""),
                "sedes": extra.get("sedes", ""),
                "sedes_slugs": extra.get("sedes_slugs", ""),
                "modalities": extra.get("modalities", ""),
                "schedule_summary": extra.get("schedule_summary", ""),
                "education_titles": extra.get("education_titles", ""),
                "education_places": extra.get("education_places", ""),
                "education_summary": extra.get("education_summary", ""),
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