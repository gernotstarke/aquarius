# ADR-027: Admin Bootstrap-Strategie

**Status:** Accepted
**Datum:** 2026-01-05
**Entscheider:** Gernot Starke

## Kontext

Der Admin-Panel-Zugang benötigt einen initialen ROOT-User. Entwicklung und Produktion haben unterschiedliche Sicherheitsanforderungen.

## Entscheidung

Wir verwenden **zwei separate Make-Targets** für unterschiedliche Umgebungen:

### Entwicklung: `make db-seed`
- Verwendet Default-Credentials (`admin` / `admin`)
- Oder: Env-Variable `INITIAL_ADMIN_PASSWORD`
- Schnelle Iteration ohne Prompts
- Zeigt Warnung bei Default-Passwort

### Produktion: `make db-init-admin`
- **Interaktiv**: Fragt Username/Passwort ab
- **Sicher**: Min. 12 Zeichen, Bestätigung erforderlich
- **Idempotent**: Erstellt neuen User oder aktualisiert existierenden
- Verwendet `getpass` (keine Passwort-Anzeige im Terminal)

## Workflows

**Entwicklung (lokal):**
```bash
cd web
make db-seed  # Erstellt admin/admin + Testdaten
```

**Produktion (erstmaliges Setup):**
```bash
cd web
make db-reset        # Erstellt Datenbank-Schema
make db-init-admin   # Interaktive Admin-Erstellung
# → Login → 2FA-Setup (wenn implementiert)
```

**Produktion (Passwort-Reset):**
```bash
cd web
make db-init-admin   # Aktualisiert bestehendes Passwort
```

## Konsequenzen

### Positiv ✅
- **Dev**: Schnelle Iteration ohne manuelle Eingaben
- **Prod**: Keine Default-Passwörter, sichere Initialisierung
- **Konsistent**: Klare Trennung zwischen dev/prod
- **Recovery**: `db-init-admin` funktioniert als Passwort-Reset

### Negativ ⚠️
- Entwickler müssen unterschiedliche Targets kennen
- Produktions-Setup erfordert Terminal-Zugang

## Sicherheit

- Passwörter werden **nur als bcrypt-Hash** gespeichert (`hashed_password`)
- `getpass`-Modul verhindert Terminal-Echo
- 12-Zeichen-Minimum erzwingt starke Passwörter
- 2FA wird nach erstem Login verpflichtend (zukünftig)

## Referenzen

- [ADR-026: Verbände als Konstanten](ADR-026-verbaende-als-konstanten.md)
- `/web/Makefile` - Implementierung der Targets
- `/web/backend/app/auth.py` - Passwort-Hashing (bcrypt)
