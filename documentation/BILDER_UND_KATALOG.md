# Figurenbilder und Katalog - Anleitung

Diese Datei erklärt, wie Sie Figurenbilder hinzufügen und den Figurenkatalog verwalten.

## Verzeichnisstruktur

```
backend/
├── data/
│   └── figuren-kataloge/
│       ├── README.md
│       └── figuren-v1.0-saison-2024.json  # JSON-Katalog
└── static/
    └── figuren/
        ├── README.md
        ├── .gitignore
        └── [Ihre Bilder hier]  # z.B. ballettbein.png
```

## Figurenbilder hinzufügen

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

## Figurenkatalog bearbeiten

### JSON-Katalog Struktur

Die Datei `backend/data/figuren-kataloge/figuren-v1.0-saison-2024.json` enthält alle Figuren:

```json
{
  "version": "1.0",
  "saison": "2024/2025",
  "erstellt_am": "2024-12-20",
  "beschreibung": "Offizieller Figurenkatalog",
  "figuren": [
    {
      "name": "Ballettbein",
      "kategorie": "Ballettbein",
      "beschreibung": "Ein Bein senkrecht gestreckt...",
      "schwierigkeitsgrad": 12,
      "min_alter": 8,
      "bild": "figuren/ballettbein.png"
    }
  ]
}
```

### Katalog bearbeiten

1. Öffnen Sie die JSON-Datei in einem Editor
2. Fügen Sie neue Figuren hinzu oder ändern Sie bestehende
3. Speichern Sie die Datei
4. Führen Sie `seed_db.py` erneut aus

### Neue Version erstellen

Für eine neue Saison oder größere Änderungen:

1. Kopieren Sie die aktuelle JSON-Datei
2. Benennen Sie sie um (z.B. `figuren-v2.0-saison-2025.json`)
3. Aktualisieren Sie `version`, `saison` und `erstellt_am`
4. In `seed_db.py` ändern Sie:
   ```python
   FIGUREN_KATALOG = "data/figuren-kataloge/figuren-v2.0-saison-2025.json"
   ```

## Startnummer anzeigen

Nach dem Seeding sollten die Startnummern in der UI sichtbar sein:
- In der **Anmeldungsliste**: Badge `#1`, `#2`, etc.
- Im **Wettkampf-Detail**: In der Anmeldungen-Tab

Falls nicht sichtbar:
1. Stellen Sie sicher, dass die Datenbank neu geseedet wurde
2. Laden Sie das Frontend neu (Ctrl+F5)
3. Prüfen Sie die Browser-Konsole auf Fehler

## Figuren zu Wettkämpfen zuordnen

Im **Wettkampf-Detail** gibt es einen **"Figuren"**-Tab:

1. Navigieren Sie zu einem Wettkampf
2. Klicken Sie auf den Tab "Figuren"
3. Sehen Sie die zugeordneten Figuren
4. Fügen Sie Figuren aus der "Verfügbare Figuren"-Liste hinzu
5. Entfernen Sie Figuren bei Bedarf

Dies vereinfacht die Anmeldung erheblich, da Kinder nur aus den für den Wettkampf zugelassenen Figuren auswählen können.

## Troubleshooting

### "Bild nicht gefunden" beim Seeding

Das ist normal und kein Fehler. Das Script prüft, ob Bilder vorhanden sind:
- ⚠️ Bild nicht gefunden → Figur wird ohne Bild erstellt
- ✓ Bild gefunden → Bildpfad wird in DB gespeichert

Sie können Bilder später hinzufügen und erneut seeden.

### Startnummer wird nicht angezeigt

1. Prüfen Sie, ob die Datenbank neu geseedet wurde
2. Starten Sie Backend und Frontend neu:
   ```bash
   docker-compose restart
   ```

### JSON-Fehler beim Seeding

Prüfen Sie die JSON-Syntax:
```bash
# JSON validieren
cat backend/data/figuren-kataloge/figuren-v1.0-saison-2024.json | python -m json.tool
```

Bei Fehlern: Korrigieren Sie fehlende Kommas, Klammern, etc.
