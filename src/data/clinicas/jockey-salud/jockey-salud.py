import requests
import csv

BASE_URL = "https://citasenlinea.jockeysalud.com.pe/api/v1/doctors"
OUTPUT_CSV = "jockeysalud_staff.csv"

# Headers required by the API (from browser network inspection)
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Authorization": "TSTCbj7mQO2xEOuwEK08RajQS1OxndfY",
    "Origin": "https://www.jockeysalud.com.pe",
    "Referer": "https://www.jockeysalud.com.pe/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15",
}


def get_doctors():
    all_doctors = []
    page = 1

    while True:
        params = {
            "page": page,
        }

        print(f"Fetching page {page}...")
        r = requests.get(BASE_URL, params=params, headers=HEADERS)
        r.raise_for_status()

        data = r.json()

        # muchos APIs tipo Laravel devuelven algo así:
        # {
        #   "data": [...],
        #   "meta": {...},
        #   "links": {...}
        # }
        doctors = data.get("data", None)

        # si no hay clave "data" y el JSON es directamente una lista:
        if doctors is None:
            if isinstance(data, list):
                doctors = data
            else:
                print("⚠ No 'data' key and response is not a list. Got keys:", data.keys())
                break

        if not doctors:
            print("No more doctors, stopping.")
            break

        # debug: ver las keys de un doctor para saber cómo mapear
        if page == 1:
            print("Example doctor keys:", doctors[0].keys())

        all_doctors.extend(doctors)

        # intentar leer info de paginación si existe
        meta = data.get("meta") or {}
        last_page = meta.get("last_page")
        current_page = meta.get("current_page", page)

        if last_page:
            if current_page >= last_page:
                print("Reached last_page from meta, stopping.")
                break
            page += 1
        else:
            # si no hay meta/last_page, avanzamos hasta que la API nos devuelva lista vacía
            page += 1

    return all_doctors


def save_csv(doctors):
    # ajusta estas claves según lo que veas en Example doctor keys
    fieldnames = ["cmp", "nombre", "especialidad", "foto"]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(fieldnames)

        for d in doctors:
            # Based on the API response format:
            # - cmp_code: CMP number
            # - full_name: doctor name
            # - specialty: specialty name
            # - image: photo URL
            cmp_val = d.get("cmp_code") or d.get("cmp") or d.get("cmp_number")
            nombre = d.get("full_name") or d.get("name") or d.get("doctor_name")
            especialidad = (
                d.get("specialty")
                or d.get("speciality")
                or d.get("especialidad")
            )
            foto = d.get("image") or d.get("avatar") or d.get("photo")

            w.writerow([cmp_val, nombre, especialidad, foto])

    print(f"Saved → {OUTPUT_CSV}")


if __name__ == "__main__":
    docs = get_doctors()
    print(f"Found {len(docs)} doctors")
    save_csv(docs)