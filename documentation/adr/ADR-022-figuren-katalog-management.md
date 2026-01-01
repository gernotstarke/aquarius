# ADR-022: Verwaltung von Figurenkatalogen und Bildern

**Status:** Accepted
**Datum:** 2026-01-01
**Entscheider:** Gernot Starke

## Kontext
Das System muss einen Katalog von Schwimmfiguren verwalten, der Metadaten (Schwierigkeit, Beschreibung) und Bilder enthält. Dieser Katalog ändert sich saisonal. Es wird eine einfache, wartbare Lösung benötigt, um diese Stammdaten zu pflegen und Bilder effizient bereitzustellen.

## Entscheidung
Wir verwenden einen dateibasierten Ansatz für die Verwaltung von Stammdaten:

1.  **JSON als Source of Truth:** Der Figurenkatalog wird in versionierten JSON-Dateien (z.B. `backend/data/figuren-kataloge/`) gepflegt.
2.  **Dateisystem für Bilder:** Bilder werden als statische Dateien in `backend/static/figuren/` abgelegt und nicht als BLOBs in der Datenbank gespeichert.
3.  **Seeding-Prozess:** Ein Python-Skript (`seed_db.py`) importiert die Daten aus dem JSON und die Bildpfade in die Datenbank.

## Konsequenzen
*   **Positiv:** Einfache Versionierung der Daten via Git. Performante Auslieferung der Bilder. Geringe Datenbankgröße.
*   **Negativ:** Änderungen erfordern einen Deployment/Seed-Schritt. Referenzielle Integrität zwischen JSON und Bildern wird nur beim Seeding geprüft.

## Vorgehen: Figurenbilder hinzufügen

### Schritt 1: Bilder vorbereiten

Ihre gezeichneten Bilder sollten:
- **Format**: PNG mit transparentem Hintergrund (empfohlen) oder JPG
- **Auflösung**: Mindestens 512x512 Pixel, ideal 1024x1024 Pixel
- **Dateigröße**: Max. 500 KB pro Bild
- **Dateiname**: Kleinbuchstaben mit Bindestrichen (z.B. `ballettbein.png`)

### Schritt 2: Bilder in Verzeichnis legen

Kopieren Sie Ihre Bilder nach:
```
backend/static/figuren/
```

Beispiel:
```bash
cp meine-zeichnungen/ballettbein.png backend/static/figuren/
cp meine-zeichnungen/vertikale.png backend/static/figuren/
```

### Schritt 3: Datenbank neu seeden

Führen Sie im Backend-Container das Seeding-Script aus:

```bash
# Container starten (falls noch nicht gestartet)
docker-compose up -d

# Seed-Script ausführen
docker-compose exec backend python seed_db.py
```

Das Script:
- Lädt den JSON-Katalog
- Prüft, welche Bilder vorhanden sind
- Zeigt Statistiken über gefundene/fehlende Bilder
- Importiert alle Figuren in die Datenbank

Ausgabe:
```
🎯 Creating figuren from JSON catalog...
   ℹ️  Katalog geladen: Version 1.0, Saison 2024/2025
   ⚠️  Bild nicht gefunden: figuren/ballettbein.png
   ✓ Created 26 Figuren
   ✓ 5 Bilder gefunden, 21 fehlen noch
```

## Troubleshooting

### "Bild nicht gefunden" beim Seeding

Das ist normal und kein Fehler. Das Script prüft, ob Bilder vorhanden sind:
- ⚠️ Bild nicht gefunden → Figur wird ohne Bild erstellt
- ✓ Bild gefunden → Bildpfad wird in DB gespeichert

Sie können Bilder später hinzufügen und erneut seeden.


### JSON-Fehler beim Seeding

Prüfen Sie die JSON-Syntax:
```bash
# JSON validieren
cat backend/data/figuren-kataloge/figuren-v1.0-saison-2024.json | python -m json.tool
```
