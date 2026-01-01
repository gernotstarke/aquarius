# ADR-023: Client-Side Status Indicators in Documentation

**Status:** Accepted
**Datum:** 2025-12-31
**Entscheider:** Dokumentations-Team
**Kontext:** Die Dokumentations-Website (Jekyll) verlinkt auf die Live-Anwendungen (Web-App, Admin UI). Benutzer sollen visuelles Feedback erhalten, ob die Ziel-Anwendung aktuell erreichbar ist (insbesondere wichtig für lokales Development vs. Production).

---

## Entscheidung

Wir implementieren einen **Client-Side Image-Load Check** ("Favicon Hack"), um die Verfügbarkeit der Web-Applikation direkt in den Dokumentations-Kacheln anzuzeigen.

### Funktionsweise

1.  **Indikator**: Ein farbiger Punkt (`.status-indicator`) wird per CSS in die Navigations-Kachel eingebettet.
2.  **Logik (JavaScript)**:
    *   Ein Script auf der Dokumentationsseite versucht, ein statisches Asset der Ziel-Anwendung zu laden (z.B. `/aquarius-logo.png`).
    *   **Erfolg (`onload`)**: Der Indikator wird grün (`.status-online`).
    *   **Fehler (`onerror`)**: Der Indikator wird rot/grau (`.status-offline`).
3.  **Environment-Detection**: Das Script prüft `window.location.hostname`.
    *   Bei `localhost` prüft es `http://localhost:5173` (Vite Dev Server).
    *   In Production prüft es die konfigurierte Production-URL (`https://aquarius.arc42.org`).
4.  **Intervall**: Der Check wird alle 10 Sekunden wiederholt.

### Alternativen

*   **Backend Health-Check API**: Würde CORS-Header (Cross-Origin Resource Sharing) erfordern, da die Doku oft auf einer anderen Domain/Port läuft als die App. Wäre komplexer zu konfigurieren.
*   **Server-Side Ping**: Nicht möglich, da die Dokumentation eine statische Seite (GitHub Pages / Jekyll) ist.

## Konsequenzen

### Positiv
*   **Kein Backend-Code nötig**: Funktioniert rein im Browser.
*   **CORS-Freundlich**: Das Laden von Bildern (`<img>`) ist im Web weniger strikt reguliert als AJAX-Requests (`fetch`).
*   **Sofortiges Feedback**: Entwickler sehen sofort, ob sie `make dev` vergessen haben.

### Negativ
*   **Kein "Deep" Check**: Prüft nur, ob der Webserver statische Dateien ausliefert, nicht ob die Datenbank verbunden ist oder die API funktioniert.
*   **Traffic**: Erzeugt alle 10 Sekunden einen Request pro offenem Tab (allerdings sehr klein und browser-gecached, wobei wir Cache-Busting nutzen müssen, um echte Checks zu erzwingen).

## Implementierung

Code-Snippet in `docs/_pages/app.md`:

```javascript
const img = new Image();
img.onload = function() { setStatus('green'); };
img.onerror = function() { setStatus('red'); };
img.src = targetUrl + "/aquarius-logo.png?t=" + new Date().getTime();
```
