"""Seed data for constant reference entities."""
from app import models

VERBAND_DATA = [
    {
        "land": "Deutschland",
        "name": "Bundesverband Kunst- und Figurenschwimmen Deutschland e.V.",
        "abkuerzung": "BKFD",
        "ort": "Kassel",
    },
    {
        "land": "Deutschland",
        "name": "Bayerischer Fachverband für Kunst- und Figurenschwimmen e.V.",
        "abkuerzung": "BFVKF",
        "ort": "Regensburg",
    },
    {
        "land": "Deutschland",
        "name": "Landesverband Kunstschwimmen Nordrhein-Westfalen e.V.",
        "abkuerzung": "LKNW",
        "ort": "Dortmund",
    },
    {
        "land": "Deutschland",
        "name": "Hessischer Verband für Figuren- und Kunstschwimmen",
        "abkuerzung": "HVFK",
        "ort": "Gießen",
    },
    {
        "land": "Deutschland",
        "name": "Norddeutsche Arbeitsgemeinschaft Nachwuchs-Kunstschwimmen",
        "abkuerzung": "NANK",
        "ort": "Lüneburg",
    },
    {
        "land": "Österreich",
        "name": "Österreichischer Fachverband für Kunst- und Figurenschwimmen",
        "abkuerzung": "OFKF",
        "ort": "Wien",
    },
    {
        "land": "Österreich",
        "name": "Landesverband Kunstschwimmen Kärnten",
        "abkuerzung": "LSKK",
        "ort": "Klagenfurt am Wörthersee",
    },
    {
        "land": "Österreich",
        "name": "Steirischer Nachwuchsverband Kunst- und Figurenschwimmen",
        "abkuerzung": "SNKF",
        "ort": "Leoben",
    },
    {
        "land": "Österreich",
        "name": "Fachverband Kunstschwimmen Oberösterreich",
        "abkuerzung": "FKO",
        "ort": "Wels",
    },
    {
        "land": "Schweiz",
        "name": "Schweizerischer Fachverband Kunst- und Figurenschwimmen",
        "abkuerzung": "SFKF",
        "ort": "Ittigen",
    },
    {
        "land": "Schweiz",
        "name": "Kantonalverband Kunstschwimmen Zürich",
        "abkuerzung": "KKZ",
        "ort": "Zürich",
    },
    {
        "land": "Schweiz",
        "name": "Zentralschweizer Verband für Kunst- und Figurenschwimmen",
        "abkuerzung": "ZVKF",
        "ort": "Zug",
    },
    {
        "land": "Schweiz",
        "name": "Ostschweizer Nachwuchsverband Kunstschwimmen",
        "abkuerzung": "ONK",
        "ort": "Rapperswil-Jona",
    },
]


def ensure_verbaende(db):
    """Insert constant Verbände if they are missing."""
    existing = {name for (name,) in db.query(models.Verband.name).all()}
    created = 0
    for payload in VERBAND_DATA:
        if payload["name"] in existing:
            continue
        db.add(models.Verband(**payload))
        created += 1
    db.commit()
    total = db.query(models.Verband).count()
    return created, total
