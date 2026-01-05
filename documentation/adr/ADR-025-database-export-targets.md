# ADR-025: Database-Export Make-Targets

**Status:** Accepted
**Datum:** 2026-01-05
**Entscheider:** Gernot Starke

## Kontext

Für die Dokumentation und Analyse der Datenbankstruktur wird ein ER-Diagramm benötigt. Dazu muss die SQLite-Datenbank aus der Entwicklungsumgebung (Docker) bzw. aus der Produktion (Turso) exportiert werden können.

**Anforderung:** Export der Datenbank für externe Modellierungs-Tools (DBeaver, SchemaSpy, dbdiagram.io).

## Entscheidung

Wir fügen zwei neue Make-Targets hinzu:

```makefile
make web-db-export-local   # Exportiert lokale SQLite aus Docker
make web-db-export-turso   # Exportiert Turso-Produktionsdatenbank
```

**Implementierung:**
- Exports landen in `web/backend/exports/` mit Zeitstempel
- Lokaler Export: `.db` Datei (direkte Kopie via `docker compose cp`)
- Turso Export: `.sql` Datei (SQL-Dump via `turso db shell`)
- Verzeichnis ist in `.gitignore` (keine versehentlichen Commits)

## Konsequenzen

### Positiv ✅
- Schneller Zugriff auf Datenbank für Analyse
- Konsistente Export-Methode für alle Entwickler
- Zeitstempel verhindern Überschreiben von Exports
- Integration ins bestehende Makefile-Interface (siehe ADR-010)

### Negativ ⚠️
- Turso-Export benötigt `turso` CLI
- Entwickler müssen bei Turso-Export authentifiziert sein (`turso auth login`)

## Referenzen

- [ADR-010: Makefile als Build-Interface](ADR-010-makefile-build-interface.md)
- [ADR-015: Turso Database](ADR-015-turso-database.md)
