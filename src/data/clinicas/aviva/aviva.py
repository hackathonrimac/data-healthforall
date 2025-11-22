import requests
import csv
import time

BASE_URL = "https://apibooking.aviva.pe/api/v1/professionals/byName/all"

CENTERS = {
    1: "Los Olivos",
    2: "Lima Centro",
    3: "San Martín de Porres"
}

def fetch_page(center_id, page_number, records=48):
    params = {
        "centerId": center_id,
        "professional": "",
        "letter": "",
        "basicServiceId": "",
        "records": records,
        "pageNumber": page_number,
    }
    resp = requests.get(BASE_URL, params=params)
    resp.raise_for_status()
    return resp.json()

def scrape_center(center_id, center_name, records=48, sleep_seconds=0.3):
    print(f"\n===== Scrapeando {center_name} (centerId={center_id}) =====")

    first = fetch_page(center_id, 1, records)
    data_block = first.get("data", {})
    total_pages = data_block.get("pages", 1)
    total_count = data_block.get("count", 0)

    print(f"{total_count} médicos, {total_pages} páginas")
    all_rows = []

    for page in range(1, total_pages + 1):
        print(f"  -> Página {page}/{total_pages}")
        json_data = fetch_page(center_id, page, records)

        detalle = json_data.get("data", {}).get("detalle", [])
        if not detalle:
            print("    (sin detalle)")
            continue

        for doc in detalle:
            name = (doc.get("name") or "").strip()
            surname1 = (doc.get("surname1") or "").strip()
            surname2 = (doc.get("surname2") or "").strip()

            full_name = " ".join([x for x in [name, surname1, surname2] if x])

            all_rows.append({
                "centerId": center_id,
                "centerName": center_name,
                "page": page,
                "professionalId": doc.get("professionalId"),
                "fullName": full_name,
                "name": name,
                "surname1": surname1,
                "surname2": surname2,
                "rne": doc.get("rne"),
                "cmp": doc.get("cmp"),
                "basicServiceId": doc.get("basicServiceId"),
                "basicService": doc.get("basicService"),
                "provissionId": doc.get("provissionId"),
                "serviceId": doc.get("serviceId"),
                "photo": doc.get("photo"),
            })

        time.sleep(sleep_seconds)

    return all_rows


def main():
    all_doctors = []

    for cid, cname in CENTERS.items():
        rows = scrape_center(cid, cname)
        all_doctors.extend(rows)

    print(f"\nTOTAL MÉDICOS EN LAS 3 SEDES: {len(all_doctors)}")

    filename = "aviva_todas_sedes_doctores.csv"
    fieldnames = [
        "centerId", "centerName", "page",
        "professionalId", "fullName", "name", "surname1", "surname2",
        "rne", "cmp", "basicServiceId", "basicService",
        "provissionId", "serviceId", "photo"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_doctors)

    print(f"\nArchivo guardado como: {filename}")


if __name__ == "__main__":
    main()