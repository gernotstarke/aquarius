# ADR-021: Client-seitige Suche für Architektur-Dokumentation

**Status:** Akzeptiert
**Datum:** 2026-01-01
**Entscheider:** Architektur-Team

## Kontext

Die wachsende Anzahl von ADRs und Architektur-Dokumenten macht es für Benutzer schwierig, gezielt Informationen zu finden. Da die Dokumentation als statische Website mit Jekyll generiert wird, benötigen wir eine Suchfunktion, die ohne serverseitige Logik auskommt.

## Entscheidung

Wir verwenden **Lunr.js** für eine rein client-seitige Volltextsuche innerhalb der Architektur-Dokumentation.

## Begründung

- **Keine Infrastruktur:** Benötigt keine externen Dienste oder Datenbanken.
- **Offline-fähig:** Da der Index lokal geladen wird, funktioniert die Suche auch offline (PWA-Fokus).
- **Einfache Integration:** Der Suchindex (`search.json`) wird während des Jekyll-Builds automatisch generiert.
- **Datenschutz:** Suchanfragen verlassen niemals den Browser des Benutzers.

## Konsequenzen

### Positiv
- Schneller Zugriff auf ADRs und technische Konzepte.
- Einfache Wartung, da Teil des statischen Builds.
- Keine zusätzlichen Kosten für Suchdienste.

### Negativ
- Die Größe des Suchindex wächst mit der Menge der Dokumentation (Initial-Download).
- Suche ist auf die Inhalte beschränkt, die im Index enthalten sind.

## Technische Details

Der Index wird über ein Jekyll-Liquid-Template in `docs/search.json` erstellt. Die Suchlogik wird in `docs/assets/js/arch-search.js` implementiert und nutzt Lunr.js zur Indizierung im Browser.
