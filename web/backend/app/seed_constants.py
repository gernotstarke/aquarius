"""Seed data for constant reference entities."""
from app import models

VERBAND_DATA = [
    {
        "land": "Deutschland",
        "name": "Bundesverband Kunst- und Figurenschwimmen Deutschland e.V.",
        "ort": "Kassel",
    },
    {
        "land": "Deutschland",
        "name": "Bayerischer Fachverband für Kunst- und Figurenschwimmen e.V.",
        "ort": "Regensburg",
    },
    {
        "land": "Deutschland",
        "name": "Landesverband Kunstschwimmen Nordrhein-Westfalen e.V.",
        "ort": "Dortmund",
    },
    {
        "land": "Deutschland",
        "name": "Hessischer Verband für Figuren- und Kunstschwimmen",
        "ort": "Gießen",
    },
    {
        "land": "Deutschland",
        "name": "Norddeutsche Arbeitsgemeinschaft Nachwuchs-Kunstschwimmen",
        "ort": "Lüneburg",
    },
    {
        "land": "Österreich",
        "name": "Österreichischer Fachverband für Kunst- und Figurenschwimmen",
        "ort": "Wien",
    },
    {
        "land": "Österreich",
        "name": "Landesverband Kunstschwimmen Kärnten",
        "ort": "Klagenfurt am Wörthersee",
    },
    {
        "land": "Österreich",
        "name": "Steirischer Nachwuchsverband Kunst- und Figurenschwimmen",
        "ort": "Leoben",
    },
    {
        "land": "Österreich",
        "name": "Fachverband Kunstschwimmen Oberösterreich",
        "ort": "Wels",
    },
    {
        "land": "Schweiz",
        "name": "Schweizerischer Fachverband Kunst- und Figurenschwimmen",
        "ort": "Ittigen",
    },
    {
        "land": "Schweiz",
        "name": "Kantonalverband Kunstschwimmen Zürich",
        "ort": "Zürich",
    },
    {
        "land": "Schweiz",
        "name": "Zentralschweizer Verband für Kunst- und Figurenschwimmen",
        "ort": "Zug",
    },
    {
        "land": "Schweiz",
        "name": "Ostschweizer Nachwuchsverband Kunstschwimmen",
        "ort": "Rapperswil-Jona",
    },
]


def ensure_verbaende(db):
    """Insert constant Verbände if they are missing."""
    existing = {name for (name,) in db.query(models.Verband.name).all()}
    for payload in VERBAND_DATA:
        if payload["name"] in existing:
            continue
        db.add(models.Verband(**payload))
    db.commit()
