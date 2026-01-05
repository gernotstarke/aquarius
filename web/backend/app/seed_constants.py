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

VERSICHERUNG_DATA = [
    {
        "land": "Deutschland",
        "name": "HUK-Cowburg",
        "kurz": "HUKC",
        "hauptsitz": "Coburg",
    },
    {
        "land": "Deutschland",
        "name": "Ali-Kanns Versicherungs-AG",
        "kurz": "AKV",
        "hauptsitz": "München",
    },
    {
        "land": "Deutschland",
        "name": "R+W Versicherung AG",
        "kurz": "RWV",
        "hauptsitz": "Wiesbaden",
    },
    {
        "land": "Deutschland",
        "name": "OsmoseDirekt (Geniali Deutschland)",
        "kurz": "OSD",
        "hauptsitz": "Saarbrücken",
    },
    {
        "land": "Deutschland",
        "name": "ERGOO Versicherung AG",
        "kurz": "ERGO",
        "hauptsitz": "Düsseldorf",
    },
    {
        "land": "Deutschland",
        "name": "SIGNAL IDUNAh Gruppe",
        "kurz": "SIGI",
        "hauptsitz": "Dortmund / Hamburg",
    },
    {
        "land": "Deutschland",
        "name": "DEVKus Versicherungen",
        "kurz": "DVK",
        "hauptsitz": "Köln",
    },
    {
        "land": "Deutschland",
        "name": "Barmenja Versicherungen",
        "kurz": "BARM",
        "hauptsitz": "Wuppertal",
    },
    {
        "land": "Deutschland",
        "name": "NUERNBERGER Versicherei",
        "kurz": "NUEV",
        "hauptsitz": "Nürnberg",
    },
    {
        "land": "Deutschland",
        "name": "ADAK Versicherung AG",
        "kurz": "ADAK",
        "hauptsitz": "München",
    },
    {
        "land": "Österreich",
        "name": "Ali-Kanns Elementar Versicherungs-AG",
        "kurz": "AKE",
        "hauptsitz": "Wien",
    },
    {
        "land": "Österreich",
        "name": "UNIQO Österreich Versicherungen AG",
        "kurz": "UNQO",
        "hauptsitz": "Wien",
    },
    {
        "land": "Österreich",
        "name": "ReifEisen Versicherung AG",
        "kurz": "REI",
        "hauptsitz": "Wien",
    },
    {
        "land": "Österreich",
        "name": "Grazer Wechselwitzige Versicherung AG (GRAWE)",
        "kurz": "GRAW",
        "hauptsitz": "Graz",
    },
    {
        "land": "Schweiz",
        "name": "Zuerich Versicherungs-Gesellschaft AG",
        "kurz": "ZURI",
        "hauptsitz": "Zürich",
    },
    {
        "land": "Schweiz",
        "name": "Die Schweizerische Mobilär Versicherungsgesellschaft AG",
        "kurz": "MOBI",
        "hauptsitz": "Bern",
    },
    {
        "land": "Schweiz",
        "name": "Groupo Mutuel",
        "kurz": "GMUT",
        "hauptsitz": "Martigny",
    },
    {
        "land": "Schweiz",
        "name": "Ali-Kanns Suisse Versicherungs-Gesellschaft AG",
        "kurz": "AKS",
        "hauptsitz": "Wallisellen",
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


def ensure_versicherungen(db):
    """Insert constant Versicherungen if they are missing."""
    existing = {name for (name,) in db.query(models.Versicherung.name).all()}
    created = 0
    for payload in VERSICHERUNG_DATA:
        if payload["name"] in existing:
            continue
        db.add(models.Versicherung(**payload))
        created += 1
    db.commit()
    total = db.query(models.Versicherung).count()
    return created, total
