# ADR-036: Passwortschutz für Architektur-Dokumentation

**Status:** Accepted
**Datum:** 2026-01-22
**Kontext:** Veröffentlichung der Dokumentation als GitHub Pages
**Entscheider:** Gernot Starke

---

## Kontext und Problem

Aquarius ist primär eine **Fallstudie für Softwarearchitektur-Trainings** (z.B. iSAQB).
Die Architekturdokumentation enthält "Lösungen" und Hintergründe, die Teilnehmende von Trainings idealerweise erst im Laufe der Übungen erarbeiten oder sehen sollen.

Wäre die Dokumentation öffentlich auf GitHub Pages gehostet, so wären diese Informationen für jedermann (inklusive Trainingsteilnehmer vor dem Training) frei zugänglich.

**Anforderungen:**
1.  **Hürde:** Der Zugriff auf spezifische Bereiche (z.B. `/architecture/*`, `/challenges/*`) soll (etwas) erschwert werden.
2.  **Einfachheit:** Keine komplexe Server-Side-Authentication (da GitHub Pages statisch ist).
3.  **Keine Hochsicherheit:** Es geht nicht um den Schutz von Geschäftsgeheimnissen oder persönlichen Daten, sondern um didaktische Spoiler-Vermeidung. Ein technisch versierter Nutzer kann den Schutz umgehen (Client-Side), das ist akzeptabel.
4.  **Konfigurierbarkeit:** Das Passwort muss leicht änderbar sein.

---

## Entscheidung

Wir implementieren einen **Client-seitigen Passwortschutz** via JavaScript für sensitive Bereiche der Dokumentation.

### Technische Umsetzung

1.  **Layout-basiert:** Ein spezielles Jekyll-Layout (`protected`) prüft beim Laden, ob ein valides Session-Token (im `sessionStorage`) vorhanden ist.
2.  **Client-Side Hashing:**
    - Das korrekte Passwort wird als **SHA-256 Hash** in der `_config.yml` hinterlegt (`protected_password_hash`).
    - Bei Eingabe wird das Passwort des Nutzers gehasht und mit dem hinterlegten Hash verglichen.
    - Es wird **kein Klartext-Passwort** im Quellcode gespeichert.
3.  **Obfuskation:** Das JavaScript, das die Prüfung vornimmt, wird minifiziert und leicht obfuskiert, um triviales "Nachlesen" im Browser-Debugger zu erschweren (aber nicht unmöglich zu machen).

### Konfiguration

Ein Hash des Passwortes wird in der zentralen Konfigurationsdatei `docs/_config.yml` verwaltet:

```yaml
# docs/_config.yml
protected_password_hash: "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" # Beispiel-Hash
```

Ein `Makefile`-Target unterstützt das Generieren neuer Hashes:

```bash
make protect-hash PASSWORD=neuesPasswort123
```

Standardmäßig ist das Passwort auf `training2026` gesetzt (Stand Jan 2026).

---

## Konsequenzen

### Positiv

- **Spoiler-Schutz:** Teilnehmer können nicht "aus Versehen" die Lösungen sehen.
- **Hosting-Unabhängigkeit:** Funktioniert auf jedem statischen Webserver (GitHub Pages, Netlify, lokal).
- **Keine Backend-Kosten:** Keine Datenbank oder Auth-Server notwendig.

### Negativ

- **Keine echte Sicherheit:** Wer JavaScript deaktiviert oder den Quellcode analysiert, kann den Hashwert des Passwortes auslesen.
- **UX:** Nutzer müssen ein Passwort eingeben (Session bleibt aber erhalten).

### Sicherheitshinweis

Diese Lösung bietet **keinen kryptographischen Schutz**. 
Für sensible Daten (Credentials) ist dieser Ansatz **nicht geeignet** und darf dafür nicht verwendet werden. 
Für den didaktischen Zweck (Spoiler-Schutz) ist er jedoch adäquat und verhältnismäßig.
