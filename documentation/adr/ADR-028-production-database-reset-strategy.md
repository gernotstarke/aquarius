# ADR-028: Production Database Reset Strategy

**Status:** Accepted
**Datum:** 2026-01-06
**Entscheider:** Entwicklungsteam
**Bezieht sich auf:** [ADR-015: Turso Database](ADR-015-turso-database.md), [ADR-027: Admin Bootstrap-Strategie](ADR-027-admin-bootstrap-strategie.md)

---

## Kontext

Die Aquarius-Anwendung läuft auf fly.io mit einer Turso Cloud-Datenbank. Während der Entwicklung und bei Schema-Änderungen ist es notwendig, die Produktionsdatenbank zurückzusetzen und mit initialisierten Daten neu zu befüllen.

**Herausforderungen:**
- Produktionsdatenbank liegt in Turso Cloud (nicht lokal)
- Anwendung läuft in fly.io Container (kein direkter Dateisystem-Zugriff)
- Schema-Änderungen erfordern oft vollständigen Datenbank-Reset
- Seed-Daten müssen konsistent mit lokalem Development sein

**Anforderungen:**
- Sicherer und kontrollierter Reset der Produktionsdatenbank
- Wiederverwendung von bestehendem `seed_db.py` Script
- Minimaler Aufwand für Entwickler
- Keine Notwendigkeit, neue Turso-Datenbank zu erstellen (Tokens bleiben gültig)

## Entscheidung

Wir verwenden **fly.io SSH + seed_db.py** als primäre Strategie für Produktions-Datenbank-Resets.

### Durchführung

```bash
# 1. SSH in den fly.io Container
flyctl ssh console

# 2. Im Container: Datenbank zurücksetzen und neu befüllen
python seed_db.py

# 3. Container verlassen
exit
```

**Optionale Schritte (wenn Admin-User angepasst werden soll):**
```bash
flyctl ssh console
python init_admin.py
exit
```

## Begründung

### Warum Option 1: fly.io SSH + seed_db.py?

#### Pro ✅
- **Wiederverwendung**: Nutzt bestehendes, getestetes `seed_db.py` Script
- **Konsistenz**: Identische Daten wie in lokaler Entwicklung
- **Einfachheit**: Keine zusätzliche Infrastruktur oder Tools benötigt
- **Sicher**: Läuft direkt im Produktions-Container mit korrekten Credentials
- **Atomisch**: `seed_db.py` führt `reset_database()` → `seed_data()` in einem Durchlauf aus
- **Kein Token-Management**: Turso-Auth-Token bleiben gültig (keine fly.io secrets update nötig)
- **Reproduzierbar**: Gleiche Seed-Daten in dev/staging/prod

#### Contra ⚠️
- Erfordert `flyctl` CLI und Login
- Produktions-Downtime während des Resets (kurz, ~10-30 Sekunden)
- Terminal-Zugang erforderlich (kein Web-Interface)

### Alternativen (nicht gewählt)

#### Alternative 2: Turso-Datenbank neu erstellen

```bash
turso db destroy aquarius
turso db create aquarius --location fra
turso db tokens create aquarius --expiration none
flyctl secrets set DATABASE_URL='libsql://...'
flyctl deploy
```

**Contra:**
- ❌ Viel mehr Schritte
- ❌ Neue Auth-Tokens erforderlich
- ❌ `flyctl secrets` Update + Re-Deploy (langsamer)
- ❌ Höheres Fehlerrisiko (mehrere manuelle Schritte)

**Wann sinnvoll:**
- Datenbank ist korrumpiert
- Turso-Region soll gewechselt werden
- Komplett neues Setup erforderlich

#### Alternative 3: SQL-Migration Scripts

```bash
flyctl ssh console -C "python -m alembic upgrade head"
```

**Contra:**
- ❌ Funktioniert nur für Schema-Updates, nicht für kompletten Reset
- ❌ Seed-Daten müssen separat eingefügt werden
- ❌ Migrations-History muss gepflegt werden

**Wann sinnvoll:**
- Produktionsdaten sollen **erhalten** bleiben
- Nur Schema-Änderungen notwendig (zukünftig, wenn echte Produktionsdaten existieren)

## Konsequenzen

### Positiv ✅
- **Developer Experience**: Ein einfacher Befehl (`flyctl ssh console` + `python seed_db.py`)
- **Wartbarkeit**: `seed_db.py` bleibt Single Source of Truth für Initialdaten
- **Schnelligkeit**: Reset dauert nur ~30 Sekunden
- **Testbarkeit**: Lokale Tests mit `make db-seed` haben identische Daten wie Produktion

### Negativ ⚠️
- **Produktionsdaten gehen verloren**: Nur während Early Development akzeptabel
- **Manueller Prozess**: Kein Automation (aber für seltene Operation akzeptabel)

### Risiko-Mitigation

**Problem:** Versehentlicher Reset mit Datenverlust

**Mitigation (wenn Produktionsdaten wichtig werden):**
1. Vor jedem Reset: `make db-export-turso` (Backup erstellen, siehe ADR-025)
2. `seed_db.py` fragt Bestätigung ab:
   ```python
   if os.getenv("FLY_APP_NAME"):  # Läuft auf fly.io
       confirm = input("⚠️  Production DB Reset! Continue? [yes/NO]: ")
       if confirm != "yes":
           sys.exit(1)
   ```
3. Später: Migration zu Alembic für Schema-Updates ohne Datenverlust

## Workflows

### Entwicklung (lokal)
```bash
cd web
make db-seed  # Verwendet docker compose exec
```

### Produktion (fly.io)
```bash
# Option A: SSH + manueller Befehl (empfohlen für volle Kontrolle)
flyctl ssh console
python seed_db.py
exit

# Option B: One-liner (schneller, aber weniger sichtbar)
flyctl ssh console -C "python seed_db.py"
```

### Produktion-Reset mit Admin-Setup
```bash
flyctl ssh console
python seed_db.py      # Reset + Seed mit Default-Admin
python init_admin.py   # Interaktiv: Sicheres Admin-Passwort setzen
exit
```

## Zukunft: Migration zu Alembic

Wenn Aquarius echte Produktionsdaten hat, muss diese Strategie abgelöst werden durch:

1. **Schema-Änderungen**: Alembic Migrations (siehe ADR-007)
2. **Daten-Migrationen**: Custom Python Scripts
3. **Seed-Daten**: Nur für neue Installationen, nicht für Updates

**Zeitpunkt:** Wenn die erste echte Veranstaltung in Produktion stattfindet.

## Referenzen

- [ADR-007: Alembic Migrations](ADR-007-alembic-migrations.md)
- [ADR-015: Turso Database](ADR-015-turso-database.md)
- [ADR-025: Database-Export Targets](ADR-025-database-export-targets.md)
- [ADR-027: Admin Bootstrap-Strategie](ADR-027-admin-bootstrap-strategie.md)
- `/web/backend/seed_db.py` - Implementierung
- `/web/Makefile` - `db-seed` Target
