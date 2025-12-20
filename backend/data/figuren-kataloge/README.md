# Figurenkatalog

Dieses Verzeichnis enthält die offiziellen Figurenkataloge für verschiedene Saisons.

## Dateistruktur

Die JSON-Dateien folgen diesem Namensschema:
```
figuren-v{VERSION}-saison-{JAHR}.json
```

Beispiel: `figuren-v1.0-saison-2024.json`

## JSON-Schema

```json
{
  "version": "1.0",           // Katalog-Version
  "saison": "2024/2025",      // Saison-Zeitraum
  "erstellt_am": "2024-12-20", // Erstellungsdatum
  "beschreibung": "...",      // Beschreibung des Katalogs
  "figuren": [
    {
      "name": "Ballettbein",                    // Figurenname
      "kategorie": "Ballettbein",                // Kategorie
      "beschreibung": "...",                     // Beschreibung der Figur
      "schwierigkeitsgrad": 12,                  // 10-20 (wird als 1.0-2.0 angezeigt)
      "min_alter": 8,                            // Mindestalter in Jahren
      "bild": "figuren/ballettbein.png"         // Relativer Pfad zum Bild
    }
  ]
}
```

## Bildpfade

Die Bildpfade in `bild` sind relativ zu `backend/static/`.

Beispiel:
- JSON: `"bild": "figuren/ballettbein.png"`
- Tatsächlicher Pfad: `backend/static/figuren/ballettbein.png`

## Neue Version erstellen

1. Kopieren Sie die aktuelle JSON-Datei
2. Erhöhen Sie die Versionsnummer im Dateinamen
3. Aktualisieren Sie `version` und `erstellt_am` in der JSON-Datei
4. Nehmen Sie die gewünschten Änderungen vor
5. Aktualisieren Sie `seed_db.py`, um die neue Version zu verwenden

## Verwendung

Die Datei wird von `seed_db.py` beim Database-Seeding verwendet.

Um eine bestimmte Version zu verwenden, passen Sie in `seed_db.py` den Pfad an:
```python
FIGUREN_KATALOG = "data/figuren-kataloge/figuren-v1.0-saison-2024.json"
```
