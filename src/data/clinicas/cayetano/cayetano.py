import requests
import json
import csv

BASE_URL = "https://www.cmch.pe"
LIST_PAGE_URL = BASE_URL + "/Contenido/Doctores"
API_DOCTORES_URL = BASE_URL + "/api/ApiCredentials/api/getSearchMedicosUnit"


def init_session():
    """
    Crea una sesión de requests y visita la página de doctores
    para cargar cookies / headers necesarios.
    """
    s = requests.Session()
    # User-Agent decente para evitar bloqueos tontos
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/129.0.0.0 Safari/537.36"
    })
    # Carga inicial de la página (cookies, etc.)
    r = s.get(LIST_PAGE_URL, timeout=15)
    r.raise_for_status()
    return s


def get_all_doctors(session: requests.Session):
    """
    Llama a la API /api/ApiCredentials/api/getSearchMedicosUnit
    sin filtros (sede/especialidad/nombre) para obtener todo el staff.
    """
    payload = {
        "sede": "",
        "especialidad": "",
        "nombreMedico": ""
    }

    r = session.post(
        API_DOCTORES_URL,
        json=payload,
        timeout=30,
        headers={
            "Content-Type": "application/json",
            "Referer": LIST_PAGE_URL
        }
    )
    r.raise_for_status()

    # A veces la API devuelve un string JSON, a veces ya es JSON
    try:
        data = r.json()
    except ValueError:
        data = json.loads(r.text)

    if isinstance(data, dict):
        # Si fuera un dict, aquí puedes ajustar según la estructura real
        # p.ej. data = data["data"] o similar
        print("⚠️ La respuesta vino como dict, revisa la estructura:", data.keys())
        return []

    return data


def save_to_csv(doctores, filename="medicos_cayetano_heredia.csv"):
    """
    Guarda la lista de médicos en un CSV.
    """
    # Deduplicar por IdMedico, por si se repite en varias sedes
    por_id = {}
    for m in doctores:
        por_id[m.get("IdMedico")] = m

    medicos_unicos = list(por_id.values())
    print(f"Médicos únicos por IdMedico: {len(medicos_unicos)}")

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([
            "IdMedico",
            "NombreMedico",
            "Especialidad",
            "IdEspecialidad",
            "CMP",
            "Sedes",
            "UrlFoto"
        ])

        for m in medicos_unicos:
            detalle = m.get("Detalle") or []
            sedes = ", ".join(
                d.get("Sede") for d in detalle if d.get("Sede")
            )

            writer.writerow([
                m.get("IdMedico"),
                m.get("NombreMedico", ""),
                m.get("Especialidad", ""),
                m.get("IdEspecialidad", ""),
                m.get("CMP", ""),
                sedes,
                m.get("UrlFoto", "")
            ])

    print(f"✅ CSV generado: {filename}")


def main():
    session = init_session()
    doctores = get_all_doctors(session)
    print(f"Total de médicos devueltos por la API: {len(doctores)}")
    save_to_csv(doctores)


if __name__ == "__main__":
    main()