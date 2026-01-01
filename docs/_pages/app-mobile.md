---
permalink: /app/mobile/
title: "Mobile App Simulator"
layout: single
toc: true
---

# Mobile App & Simulator

Die mobile Anwendung ("Execution App") ist für die Kampfrichter und Punktrichter am Beckenrand optimiert. Sie ist als React Native App (via Expo) implementiert.

## Simulator starten

Um die App lokal im Simulator (iOS/Android) oder im Web-Simulator zu testen:

1.  Stellen Sie sicher, dass Sie im Projekt-Root sind.
2.  Starten Sie den Entwicklungsserver:
    ```bash
    cd mobile
    npm start
    ```
3.  Drücken Sie im Terminal:
    - `i` für iOS Simulator (benötigt Xcode)
    - `a` für Android Emulator (benötigt Android Studio)
    - `w` für Web-Vorschau

## Verbindung zum Backend

Die Mobile App versucht standardmäßig, sich mit dem lokalen Backend unter `http://localhost:8000` zu verbinden.
Stellen Sie sicher, dass das Backend läuft (`make dev` im Web-Ordner).

Für echte Geräte im gleichen WLAN müssen Sie die API-URL in der App-Konfiguration anpassen (IP-Adresse Ihres Rechners statt localhost).
