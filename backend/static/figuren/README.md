# Figurenbilder

Dieses Verzeichnis enthält die Bilder für alle Kunstschwimm-Figuren.

## Verzeichnisstruktur

```
figuren/
├── README.md          # Diese Datei
├── .gitignore         # Git-Konfiguration
└── images/            # PNG/JPG Bilder hier ablegen
    ├── ballettbein.png
    ├── vertikale.png
    └── ...
```

## Dateiformat

- **Empfohlenes Format**: PNG mit transparentem Hintergrund
- **Alternative**: JPG für fotografische Bilder
- **Auflösung**: Mindestens 512x512 Pixel, ideal 1024x1024 Pixel
- **Dateigröße**: Max. 500 KB pro Bild (für schnelle Ladezeiten)

## Namenskonvention

Die Dateinamen sollten dem Muster folgen:
```
{figur-name-kleinbuchstaben-mit-bindestrichen}.png
```

Beispiele:
- `ballettbein.png`
- `ballettbein-beidbeinig.png`
- `vertikale-spagat.png`
- `flamingo-vertikale.png`

## Verwendung

Die Bilder werden über die Figuren-API bereitgestellt und in der Frontend-UI angezeigt.

Der Pfad wird in der Datenbank als `figuren/images/{dateiname}` gespeichert und im Frontend über die statische Datei-Route aufgerufen.

## Platzhalter

Wenn für eine Figur noch kein Bild vorhanden ist, wird automatisch ein Platzhalter-Bild angezeigt.

## Bilder hinzufügen

1. Legen Sie Ihre gezeichneten Bilder in das `images/` Unterverzeichnis
2. Achten Sie auf die korrekte Namenskonvention
3. Führen Sie `make db-import-figures FILE=data/figuren-kataloge/figuren-v1.0-saison-2024.json` aus
   (Das Script prüft automatisch, ob Bilder vorhanden sind)

## Pfad-Beispiel

- **Lokaler Pfad**: `backend/static/figuren/images/ballettbein.png`
- **Container-Pfad**: `/app/static/figuren/images/ballettbein.png`
- **In Datenbank**: `figuren/images/ballettbein.png`
- **API-URL**: `http://localhost:8000/static/figuren/images/ballettbein.png`

